# Reto de Consolidación - Agencia del Olimpo
# Doris Mosquera Lozano - doris.mosquera@sofka.com.co
# DMosqueraLSofka

# main.py — Servidor FastAPI (NO tiene clases de dominio ni SQL crudo)
# AUDITORÍA: Este archivo NO usa print(). Todo registro pasa por logger.

import logging
import requests
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from agente import reconstruir_agente
from db import (
    crear_tablas,
    registrar_agente,
    despertar_agente,
    listar_agentes,
    actualizar_energia_agente,
    enviar_mensaje,
    leer_mensajes,
    crear_mision,
    obtener_mision,
    listar_misiones_agente,
    completar_mision_db,
    fallar_mision_db,
)
from config import AGENCIA_API_KEY, EXTERNAL_API_URL

# AUDITORÍA - Configuración del logging:
# Elegí nivel INFO porque quiero registrar eventos normales de operación
# (agentes creados, misiones completadas) además de warnings y errores.
# El formato incluye fecha, nivel y mensaje para facilitar la auditoría.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Crear tablas al iniciar el servidor
crear_tablas()
logger.info("Tablas de la base de datos verificadas/creadas.")

# Modelos Pydantic: definen la forma de los datos que el servidor acepta


class AgenteRequest(BaseModel):
    nombre: str
    rol: str
    energia: int


class MensajeRequest(BaseModel):
    remitente: str
    destinatario: str
    contenido: str


class MisionRequest(BaseModel):
    titulo: str
    descripcion: str
    agente_asignado: str
    energia_requerida: int
    prioridad: str = "media"
    recompensa: int = 0


# Aplicación FastAPI
app = FastAPI(
    title="Agencia del Olimpo",
    description="API para gestionar agentes, mensajes y misiones del Olimpo",
)

# AUDITORÍA - Dependencia verificar_api_key:
# Decidí proteger solo los endpoints de escritura (POST) porque son los que
# modifican datos. Los GET son de lectura y los dejé públicos para que
# cualquier programa pueda consultar el estado de la agencia sin credenciales.
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


def verificar_api_key(api_key: str = Depends(api_key_header)):
    """Verifica que el header X-API-KEY sea válido."""
    if api_key is None:
        logger.warning("Intento de acceso SIN header X-API-KEY. Acceso denegado.")
        raise HTTPException(status_code=401, detail="Falta el header X-API-KEY")
    if api_key != AGENCIA_API_KEY:
        logger.warning(f"Intento de acceso con API key INVALIDA: '{api_key[:4]}***'. Acceso denegado.")
        raise HTTPException(status_code=401, detail="API key inválida")
    return api_key


# Endpoints de S5 (conservados)

@app.get("/")
def inicio():
    return {"status": "online", "mensaje": "Bienvenido a la Agencia del Olimpo"}


@app.get("/agentes/")
def obtener_todos_los_agentes():
    logger.info("Consultando lista de todos los agentes.")
    return listar_agentes()


@app.get("/agente/{nombre}")
def obtener_agente(nombre: str):
    agente = despertar_agente(nombre)
    if agente is None:
        logger.warning(f"Agente '{nombre}' no encontrado en la base de datos.")
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    logger.info(f"Agente '{nombre}' consultado exitosamente.")
    return agente


@app.post("/agentes/")
def crear_agente(agente: AgenteRequest, api_key: str = Depends(verificar_api_key)):
    resultado = registrar_agente(agente.nombre, agente.rol, agente.energia)
    if "Error" in resultado:
        logger.warning(f"Intento de registrar agente duplicado: '{agente.nombre}'.")
        raise HTTPException(status_code=409, detail=resultado)
    logger.info(f"Agente '{agente.nombre}' registrado (rol={agente.rol}, energia={agente.energia}).")
    return {"mensaje": resultado}


@app.post("/mensajes/")
def crear_mensaje(mensaje: MensajeRequest, api_key: str = Depends(verificar_api_key)):
    resultado = enviar_mensaje(mensaje.remitente, mensaje.destinatario, mensaje.contenido)
    logger.info(f"Mensaje enviado de '{mensaje.remitente}' a '{mensaje.destinatario}'.")
    return {"mensaje": resultado}


@app.get("/mensajes/{nombre}")
def obtener_mensajes(nombre: str):
    logger.info(f"Consultando bandeja de mensajes de '{nombre}'.")
    return leer_mensajes(nombre)


# Endpoints NUEVOS del reto

@app.post("/misiones/")
def endpoint_crear_mision(mision: MisionRequest, api_key: str = Depends(verificar_api_key)):
    # Verificar que el agente asignado exista
    agente = despertar_agente(mision.agente_asignado)
    if agente is None:
        logger.warning(f"Misión rechazada: agente '{mision.agente_asignado}' no existe.")
        raise HTTPException(
            status_code=404,
            detail=f"Agente '{mision.agente_asignado}' no encontrado. No se puede asignar la misión."
        )
    mision_id = crear_mision(
        mision.titulo, mision.descripcion, mision.agente_asignado,
        mision.energia_requerida, mision.prioridad, mision.recompensa
    )
    logger.info(f"Misión #{mision_id} '{mision.titulo}' creada y asignada a '{mision.agente_asignado}'.")
    return {"mensaje": f"Misión #{mision_id} creada", "id": mision_id}


@app.get("/misiones/{mision_id}")
def endpoint_obtener_mision(mision_id: int):
    mision = obtener_mision(mision_id)
    if mision is None:
        logger.warning(f"Misión #{mision_id} no encontrada.")
        raise HTTPException(status_code=404, detail=f"Misión #{mision_id} no encontrada")
    logger.info(f"Misión #{mision_id} consultada.")
    return mision


@app.get("/agente/{nombre}/misiones")
def endpoint_misiones_agente(nombre: str):
    agente = despertar_agente(nombre)
    if agente is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    misiones = listar_misiones_agente(nombre)
    logger.info(f"Listando {len(misiones)} misiones del agente '{nombre}'.")
    return misiones


@app.post("/misiones/{mision_id}/completar")
def endpoint_completar_mision(mision_id: int, api_key: str = Depends(verificar_api_key)):
    # 1. Obtener la misión
    mision = obtener_mision(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Misión #{mision_id} no encontrada")

    if mision["estado"] == "completada":
        raise HTTPException(status_code=400, detail=f"Misión #{mision_id} ya está completada")

    # 2. Despertar al agente y reconstruir la clase correcta (S4)
    datos_agente = despertar_agente(mision["agente_asignado"])
    if datos_agente is None:
        raise HTTPException(status_code=404, detail=f"Agente '{mision['agente_asignado']}' no encontrado")

    agente = reconstruir_agente(datos_agente)

    # 3. Descontar energía usando el método de la clase
    exito = agente.descontar_energia(mision["energia_requerida"])
    if not exito:
        logger.warning(
            f"Agente '{agente.nombre}' no tiene suficiente energía "
            f"({agente.energia}) para misión #{mision_id} (requiere {mision['energia_requerida']})."
        )
        raise HTTPException(
            status_code=400,
            detail=f"Agente '{agente.nombre}' no tiene suficiente energía ({agente.energia}). "
                   f"La misión requiere {mision['energia_requerida']}."
        )

    # 4. Dar recompensa si la misión tiene
    if mision["recompensa"] > 0:
        agente.recibir_recompensa(mision["recompensa"])

    # 5. Persistir el nuevo estado del agente y la misión
    actualizar_energia_agente(agente.nombre, agente.energia)
    completar_mision_db(mision_id)

    logger.info(
        f"Misión #{mision_id} completada por '{agente.nombre}'. "
        f"Energía restante: {agente.energia}. Recompensa: +{mision['recompensa']}."
    )
    return {
        "mensaje": f"Misión #{mision_id} completada por {agente.nombre}",
        "energia_gastada": mision["energia_requerida"],
        "recompensa_recibida": mision["recompensa"],
        "energia_actual": agente.energia,
        "tipo_agente": type(agente).__name__
    }


@app.post("/misiones/{mision_id}/fallar")
def endpoint_fallar_mision(mision_id: int, api_key: str = Depends(verificar_api_key)):
    mision = obtener_mision(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Mision #{mision_id} no encontrada")
    if mision["estado"] in ("completada", "fallida"):
        raise HTTPException(status_code=400, detail=f"Mision #{mision_id} ya esta {mision['estado']}")
    resultado = fallar_mision_db(mision_id)
    if resultado:
        logger.info(f"Mision #{mision_id} marcada como FALLIDA.")
    return {"mensaje": f"Mision #{mision_id} marcada como fallida", "estado": "fallida"}


# AUDITORÍA - Endpoint GET /briefing/{nombre}:
# Elegí la API "Useless Facts" porque devuelve datos curiosos aleatorios sin
# necesitar autenticación. Los datos son tan random que sirven como "código de
# confusión": la Agencia los transmite en abierto y los Titanes no logran
# descifrar qué significan. Mi plan de contingencia si falla: retorno un mensaje
# de fallback pero el endpoint NUNCA falla por culpa de un tercero.
@app.get("/briefing/{nombre}")
def briefing(nombre: str):
    # 1. Datos locales del agente
    datos_agente = despertar_agente(nombre)
    if datos_agente is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")

    agente = reconstruir_agente(datos_agente)
    misiones = listar_misiones_agente(nombre)

    # Estadísticas locales
    total_misiones = len(misiones)
    completadas = len([m for m in misiones if m["estado"] == "completada"])
    pendientes = len([m for m in misiones if m["estado"] == "pendiente"])
    fallidas = len([m for m in misiones if m["estado"] == "fallida"])

    # 2. Código de confusión: dato aleatorio de la API externa
    # Los Titanes interceptan estos mensajes pero NO logran descifrarlos.
    codigo_confusion = "Transmision interceptada. Contenido ilegible."
    fuente = EXTERNAL_API_URL
    try:
        respuesta = requests.get(EXTERNAL_API_URL, timeout=5)
        if respuesta.status_code == 200:
            data = respuesta.json()
            codigo_confusion = data.get("text", str(data))
            logger.info(f"Codigo de confusion generado para briefing de '{nombre}'.")
        else:
            logger.warning(f"API externa respondio con codigo {respuesta.status_code}.")
    except requests.exceptions.Timeout:
        logger.warning("API externa: timeout despues de 5 segundos.")
        codigo_confusion = "Canal de confusion temporalmente fuera de servicio (timeout)"
    except requests.exceptions.ConnectionError:
        logger.error("API externa: sin conexion.")
        codigo_confusion = "Canal de confusion desconectado. Los Titanes podrian estar bloqueando la senal."
    except Exception as e:
        logger.error(f"API externa: error inesperado - {e}")
        codigo_confusion = "Error en el canal de confusion."

    # 3. Combinar todo en un briefing
    logger.info(f"Briefing generado para agente '{nombre}'.")
    return {
        "agente": agente.to_dict(),
        "resumen_misiones": {
            "total": total_misiones,
            "completadas": completadas,
            "pendientes": pendientes,
            "fallidas": fallidas
        },
        "codigo_de_confusion": {
            "mensaje": codigo_confusion,
            "proposito": "Dato transmitido en abierto para confundir a los Titanes. Tan aleatorio que el enemigo no puede descifrarlo.",
            "fuente": fuente
        }
    }


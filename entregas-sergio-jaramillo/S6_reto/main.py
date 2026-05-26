## Creado por: Sergio Jaramillo (SergiJaramilloL)
# -----------------------------------------------------------#
# main.py — Servidor FastAPI de la Agencia de Agentes
# -----------------------------------------------------------#
# Este archivo define la aplicación FastAPI y todos sus endpoints.
# No contiene clases de dominio ni queries SQL en crudo:
# importa desde agente.py y db.py para mantener responsabilidades separadas.
#
# Para ejecutar:
#   cd S6_reto
#   uvicorn main:app --reload
# -----------------------------------------------------------#

import logging
import requests as http_client
from typing import Optional
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel

from agente import PseudoAgente, AgenteAdmin
from db import (
    crear_tablas, registrar_agente, despertar_agente, actualizar_energia_agente,
    listar_agentes, enviar_mensaje, leer_mensajes,
    crear_mision, obtener_mision, listar_misiones_agente, marcar_mision_completada,
)
from config import AGENCIA_API_KEY, EXTERNAL_API_URL

# =====================
# CONFIGURACIÓN DE LOGGING
# =====================
# Elegí INFO como nivel base porque quiero ver el flujo normal del sistema (agentes creados,
# misiones completadas) sin inundarlo de ruido de debug. WARNING se reserva para situaciones
# inesperadas pero recuperables (API externa caída), y ERROR para fallos reales que necesitan
# atención. El formato incluye fecha, nivel y mensaje: suficiente para auditar sin ser verboso.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Se crean las tablas al iniciar el servidor para garantizar que la DB existe
# antes de recibir cualquier petición.
crear_tablas()
logger.info("Tablas de la base de datos verificadas.")

# =====================
# APLICACIÓN FASTAPI
# =====================
app = FastAPI(
    title="Agencia de Agentes",
    description="API para gestionar agentes, misiones y mensajes de la Agencia.",
)


# =====================
# MODELOS PYDANTIC
# =====================

class AgenteRequest(BaseModel):
    nombre: str
    rol: str
    energia: int = 100


class MensajeRequest(BaseModel):
    remitente: str
    destinatario: str
    contenido: str


class MisionRequest(BaseModel):
    titulo: str
    descripcion: str = ""
    agente_asignado: str
    estado: str = "pendiente"
    energia_requerida: int
    prioridad: int = 1
    recompensa: int = 0


# =====================
# DEPENDENCIA: AUTENTICACIÓN CON API KEY
# =====================
# Decidí proteger solo los endpoints de escritura (POST /agentes/, POST /misiones/,
# POST /misiones/{id}/completar) porque son los que modifican el estado de la Agencia.
# Los GETs son de solo lectura: no exponen secretos ni modifican datos, así que
# dejarlos libres facilita la consulta desde herramientas externas sin fricción.
# La key viaja en el header X-API-KEY, no en la URL, para que no quede en logs de proxy.
def verificar_api_key(x_api_key: Optional[str] = Header(default=None)) -> None:
    """
    Dependencia FastAPI que valida el header X-API-KEY contra la clave configurada en .env.
    Si la clave falta o no coincide, retorna 401 antes de ejecutar el endpoint.
    """
    if x_api_key is None or x_api_key != AGENCIA_API_KEY:
        logger.warning("Intento de acceso con API key inválida o ausente.")
        raise HTTPException(status_code=401, detail="API key inválida o ausente.")


# =====================
# ENDPOINTS: ESTADO Y AGENTES (de S5, conservados)
# =====================

@app.get("/")
def inicio():
    logger.info("GET / — verificación de estado.")
    return {"status": "online", "mensaje": "Bienvenido a la Agencia de Agentes"}


@app.get("/agentes/")
def obtener_todos_los_agentes():
    logger.info("GET /agentes/ — listando todos los agentes.")
    return listar_agentes()


@app.get("/agente/{nombre}")
def obtener_agente(nombre: str):
    datos = despertar_agente(nombre)
    if datos is None:
        logger.warning("GET /agente/%s — agente no encontrado.", nombre)
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado.")
    logger.info("GET /agente/%s — agente encontrado.", nombre)
    return datos


@app.post("/agentes/", dependencies=[Depends(verificar_api_key)])
def crear_agente(agente: AgenteRequest):
    resultado = registrar_agente(agente.nombre, agente.rol, agente.energia)
    if "Error" in resultado:
        logger.error("POST /agentes/ — error al registrar '%s': %s", agente.nombre, resultado)
        raise HTTPException(status_code=409, detail=resultado)
    logger.info("POST /agentes/ — agente '%s' registrado.", agente.nombre)
    return {"mensaje": resultado}


# =====================
# ENDPOINTS: MENSAJES (de S5, conservados)
# =====================

@app.post("/mensajes/")
def crear_mensaje(mensaje: MensajeRequest):
    resultado = enviar_mensaje(mensaje.remitente, mensaje.destinatario, mensaje.contenido)
    logger.info("POST /mensajes/ — mensaje de '%s' a '%s'.", mensaje.remitente, mensaje.destinatario)
    return {"mensaje": resultado}


@app.get("/mensajes/{nombre}")
def obtener_mensajes(nombre: str):
    logger.info("GET /mensajes/%s — leyendo bandeja.", nombre)
    return leer_mensajes(nombre)


# =====================
# ENDPOINTS: MISIONES (nuevos del reto)
# =====================

@app.post("/misiones/", dependencies=[Depends(verificar_api_key)])
def crear_nueva_mision(mision: MisionRequest):
    # Verifica que el agente asignado exista antes de crear la misión.
    if despertar_agente(mision.agente_asignado) is None:
        logger.warning("POST /misiones/ — agente '%s' no encontrado.", mision.agente_asignado)
        raise HTTPException(status_code=404, detail=f"Agente '{mision.agente_asignado}' no encontrado.")
    nuevo_id = crear_mision(
        mision.titulo, mision.descripcion, mision.agente_asignado,
        mision.estado, mision.energia_requerida, mision.prioridad, mision.recompensa,
    )
    logger.info("POST /misiones/ — misión '%s' creada con id=%d.", mision.titulo, nuevo_id)
    return {"mensaje": f"Misión '{mision.titulo}' creada.", "id": nuevo_id}


@app.get("/misiones/{mision_id}")
def obtener_una_mision(mision_id: int):
    datos = obtener_mision(mision_id)
    if datos is None:
        logger.warning("GET /misiones/%d — misión no encontrada.", mision_id)
        raise HTTPException(status_code=404, detail=f"Misión id={mision_id} no encontrada.")
    logger.info("GET /misiones/%d — misión encontrada.", mision_id)
    return datos


@app.get("/agente/{nombre}/misiones")
def obtener_misiones_de_agente(nombre: str):
    if despertar_agente(nombre) is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado.")
    misiones = listar_misiones_agente(nombre)
    logger.info("GET /agente/%s/misiones — %d misiones encontradas.", nombre, len(misiones))
    return misiones


@app.post("/misiones/{mision_id}/completar", dependencies=[Depends(verificar_api_key)])
def completar_mision(mision_id: int):
    # Paso 1: obtener los datos de la misión.
    datos_mision = obtener_mision(mision_id)
    if datos_mision is None:
        raise HTTPException(status_code=404, detail=f"Misión id={mision_id} no encontrada.")
    if datos_mision["estado"] == "completada":
        raise HTTPException(status_code=409, detail="La misión ya fue completada anteriormente.")

    # Paso 2: despertar el agente asignado desde la DB y reconstruir su clase según el rol.
    # Esto cumple el requisito R2: la instancia correcta decide cómo se descuenta la energía.
    nombre_agente = datos_mision["agente_asignado"]
    datos_agente = despertar_agente(nombre_agente)
    if datos_agente is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre_agente}' no encontrado.")

    # Si el rol es "admin" se instancia AgenteAdmin; de lo contrario, PseudoAgente.
    # La clase correcta determina el costo real (AgenteAdmin paga la mitad).
    if datos_agente["rol"] == "admin":
        agente = AgenteAdmin(datos_agente["nombre"], datos_agente["energia"])
    else:
        agente = PseudoAgente(datos_agente["nombre"], datos_agente["energia"])

    # Verificación con isinstance para confirmar el tipo reconstruido (criterio de evaluación).
    tipo = "AgenteAdmin" if isinstance(agente, AgenteAdmin) else "PseudoAgente"
    logger.info("Misión %d: agente '%s' reconstruido como %s.", mision_id, nombre_agente, tipo)

    # Paso 3: descontar energía a través del método de la clase y persistir el resultado.
    energia_antes = agente.energia
    nueva_energia = agente.consumir_energia(datos_mision["energia_requerida"])
    actualizar_energia_agente(nombre_agente, nueva_energia)

    # Paso 4: marcar la misión como completada en la DB.
    marcar_mision_completada(mision_id)

    logger.info(
        "POST /misiones/%d/completar — '%s' completada. Energía de '%s': %d → %d.",
        mision_id, datos_mision["titulo"], nombre_agente, energia_antes, nueva_energia,
    )
    return {
        "mensaje": f"Misión '{datos_mision['titulo']}' completada.",
        "agente": nombre_agente,
        "tipo_agente": tipo,
        "energia_antes": energia_antes,
        "energia_ahora": nueva_energia,
    }


# =====================
# ENDPOINT: BRIEFING (datos locales + API externa)
# =====================
# Elegí la API pública https://api.adviceslip.com/advice porque retorna consejos aleatorios
# en formato JSON simple sin necesidad de autenticación. Encaja con la narrativa de agentes:
# cada briefing incluye una "instrucción del día" que orienta al agente antes de su misión.
# Plan de contingencia: si la API externa falla o tarda más de 5 segundos, el briefing
# igual se entrega con un mensaje de fallback — el servidor nunca se cuelga por un tercero.
@app.get("/briefing/{nombre}")
def obtener_briefing(nombre: str):
    datos_agente = despertar_agente(nombre)
    if datos_agente is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado.")

    misiones = listar_misiones_agente(nombre)
    misiones_pendientes = [m for m in misiones if m["estado"] == "pendiente"]

    # Consulta a la API externa con timeout de 5 segundos.
    # Si falla por cualquier razón (timeout, DNS, 5xx), se activa el fallback.
    try:
        respuesta_ext = http_client.get(EXTERNAL_API_URL, timeout=5)
        respuesta_ext.raise_for_status()
        instruccion = respuesta_ext.json()["slip"]["advice"]
        fuente_externa = EXTERNAL_API_URL
        logger.info("GET /briefing/%s — API externa respondió correctamente.", nombre)
    except Exception as e:
        # La API externa falló: usar fallback para no bloquear la respuesta del servidor.
        logger.warning("GET /briefing/%s — API externa no disponible (%s). Usando fallback.", nombre, e)
        instruccion = "Sin instrucción disponible. Opera con criterio propio."
        fuente_externa = "fallback"

    return {
        "agente": datos_agente,
        "misiones_pendientes": len(misiones_pendientes),
        "instruccion_del_dia": instruccion,
        "fuente_externa": fuente_externa,
    }

## Creado por: Sergio Jaramillo (SergiJaramilloL)

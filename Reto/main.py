"""
main.py — Aplicación FastAPI para La Agencia de Agentes

Responsabilidades:
  - Configurar el servidor FastAPI y el sistema de logging
  - Definir la dependencia de autenticación por API key
  - Exponer todos los endpoints (heredados de S5 + nuevos del Reto)
  - Importar clases desde agente.py y funciones desde db.py

Restricción: No hay queries SQL en crudo ni definición de clases de dominio aquí.
"""

import logging
import requests
from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel

from agente import PseudoAgente, AgenteAdmin
from db import (
    crear_tablas,
    registrar_agente,
    despertar_agente,
    listar_agentes,
    actualizar_energia,
    enviar_mensaje,
    leer_mensajes,
    crear_mision,
    obtener_mision,
    listar_misiones_agente,
    actualizar_estado_mision,
)
from config import AGENCIA_API_KEY, EXTERNAL_API_URL

# ---------------------------------------------------------------------------
# Configuración del logger
#
# Por qué estos niveles:
#   INFO    → eventos de negocio normales y esperados (agente creado, misión completada).
#             Permiten auditar la actividad de la Agencia sin ruido.
#   WARNING → situaciones inusuales pero que el sistema maneja (API externa lenta,
#             fallback activado). No rompen el flujo pero merecen atención.
#   ERROR   → fallos reales que requieren intervención (IntegrityError SQL,
#             excepciones inesperadas). El formato con fecha facilita correlacionar
#             eventos en logs de producción.
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Inicializa las tablas al arrancar el servidor
crear_tablas()

app = FastAPI(
    title="La Agencia de Agentes",
    description=(
        "API central para gestión de agentes, mensajes y misiones. "
        "Los endpoints de escritura requieren el header X-API-KEY."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Dependencia de autenticación por API key
#
# Decisión de ingeniería: protejo todos los endpoints de escritura
# (POST /agentes/, POST /mensajes/, POST /misiones/, POST /misiones/{id}/completar)
# porque crean o modifican estado persistente. Los GET quedan libres para
# facilitar la consulta de datos sin fricciones operativas.
# La comparación es directa contra AGENCIA_API_KEY cargada del .env;
# si la variable está vacía, toda petición es rechazada como medida de seguridad.
# ---------------------------------------------------------------------------
def verificar_api_key(
    x_api_key: Annotated[str | None, Header(alias="X-API-KEY")] = None,
) -> None:
    """
    Valida que el header X-API-KEY coincida con AGENCIA_API_KEY del .env.
    Retorna 401 si la key falta, está vacía o no coincide.
    """
    if not x_api_key or not AGENCIA_API_KEY or x_api_key != AGENCIA_API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida")


# ---------------------------------------------------------------------------
# Modelos Pydantic — definen la forma de los datos de entrada
# ---------------------------------------------------------------------------

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
    descripcion: str = ""
    agente_asignado: str
    estado: str = "pendiente"
    energia_requerida: int = 10
    prioridad: str = "media"
    creado_por: str = "sistema"


# ---------------------------------------------------------------------------
# Endpoints heredados de la Semana 5
# ---------------------------------------------------------------------------

@app.get("/", summary="Estado del servidor")
def inicio():
    return {"status": "online", "mensaje": "Bienvenido a La Agencia de Agentes"}


@app.get("/agente/{nombre}", summary="Obtener agente por nombre")
def obtener_agente(nombre: str):
    datos = despertar_agente(nombre)
    if datos is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    return datos


@app.get("/agentes/", summary="Listar todos los agentes")
def obtener_todos_los_agentes():
    return listar_agentes()


@app.post("/agentes/", dependencies=[Depends(verificar_api_key)], summary="Crear agente (protegido)")
def crear_agente(agente: AgenteRequest):
    resultado = registrar_agente(agente.nombre, agente.rol, agente.energia)
    logger.info("Agente creado: %s (rol=%s, energia=%d)", agente.nombre, agente.rol, agente.energia)
    return {"mensaje": resultado}


@app.post("/mensajes/", dependencies=[Depends(verificar_api_key)], summary="Enviar mensaje (protegido)")
def crear_mensaje(mensaje: MensajeRequest):
    resultado = enviar_mensaje(mensaje.remitente, mensaje.destinatario, mensaje.contenido)
    logger.info("Mensaje enviado de '%s' a '%s'", mensaje.remitente, mensaje.destinatario)
    return {"mensaje": resultado}


@app.get("/mensajes/{nombre}", summary="Leer bandeja de un agente")
def obtener_mensajes(nombre: str):
    return leer_mensajes(nombre)


# ---------------------------------------------------------------------------
# Nuevos endpoints de misiones
# ---------------------------------------------------------------------------

@app.post("/misiones/", dependencies=[Depends(verificar_api_key)], summary="Crear misión (protegido)")
def crear_nueva_mision(mision: MisionRequest):
    """
    Crea una nueva misión. Si el agente asignado no existe en la tabla
    agentes, responde 404 antes de insertar el registro.
    """
    agente = despertar_agente(mision.agente_asignado)
    if agente is None:
        raise HTTPException(
            status_code=404,
            detail=f"Agente '{mision.agente_asignado}' no existe en la base de datos",
        )
    mision_id = crear_mision(
        titulo=mision.titulo,
        descripcion=mision.descripcion,
        agente_asignado=mision.agente_asignado,
        estado=mision.estado,
        energia_requerida=mision.energia_requerida,
        prioridad=mision.prioridad,
        creado_por=mision.creado_por,
    )
    logger.info(
        "Misión creada: id=%d, título='%s', agente='%s'",
        mision_id, mision.titulo, mision.agente_asignado,
    )
    return {"mensaje": f"Misión creada con id={mision_id}", "id": mision_id}


@app.get("/misiones/{mision_id}", summary="Obtener misión por id")
def obtener_mision_por_id(mision_id: int):
    mision = obtener_mision(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Misión con id={mision_id} no encontrada")
    return mision


@app.get("/agente/{nombre}/misiones", summary="Listar misiones de un agente")
def misiones_de_agente(nombre: str):
    return listar_misiones_agente(nombre)


@app.post(
    "/misiones/{mision_id}/completar",
    dependencies=[Depends(verificar_api_key)],
    summary="Completar misión (protegido)",
)
def completar_mision(mision_id: int):
    """
    Marca la misión como completada o fallida según la energía disponible
    del agente asignado.

    Flujo de dominio (criterio R2):
      1. Obtiene la misión de la DB.
      2. Despierta el agente desde la DB.
      3. Reconstruye la instancia de dominio correcta según su rol
         (AgenteAdmin si rol=='admin', PseudoAgente en cualquier otro caso).
      4. Deja que la clase decida cuánta energía se consume (ejecutar_mision).
      5. Persiste la nueva energía y el nuevo estado de la misión en la DB.
    """
    mision = obtener_mision(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Misión con id={mision_id} no encontrada")

    datos_agente = despertar_agente(mision["agente_asignado"])
    if datos_agente is None:
        raise HTTPException(
            status_code=404,
            detail=f"Agente '{mision['agente_asignado']}' no encontrado en la base de datos",
        )

    # Reconstruir la instancia correcta según el rol — criterio R2.
    # isinstance(agente, AgenteAdmin) retornará True solo cuando el rol es 'admin'.
    if datos_agente["rol"] == "admin":
        agente: PseudoAgente = AgenteAdmin(
            datos_agente["nombre"], datos_agente["energia"], datos_agente["rol"]
        )
    else:
        agente = PseudoAgente(
            datos_agente["nombre"], datos_agente["energia"], datos_agente["rol"]
        )

    # La clase, no el endpoint, decide cuánto cuesta la misión
    resultado = agente.ejecutar_mision(mision["energia_requerida"])

    if not resultado["exito"]:
        actualizar_estado_mision(mision_id, "fallida")
        logger.warning(
            "Misión %d marcada como fallida: %s", mision_id, resultado["mensaje"]
        )
        return {"estado": "fallida", "detalle": resultado["mensaje"]}

    actualizar_energia(datos_agente["nombre"], resultado["energia_restante"])
    actualizar_estado_mision(mision_id, "completada")
    logger.info(
        "Misión %d completada por '%s'. Energía restante: %d. Tipo: %s",
        mision_id,
        datos_agente["nombre"],
        resultado["energia_restante"],
        "AgenteAdmin" if isinstance(agente, AgenteAdmin) else "PseudoAgente",
    )
    return {
        "estado": "completada",
        "agente": datos_agente["nombre"],
        "tipo_instancia": "AgenteAdmin" if isinstance(agente, AgenteAdmin) else "PseudoAgente",
        "energia_restante": resultado["energia_restante"],
        "detalle": resultado["mensaje"],
    }


# ---------------------------------------------------------------------------
# Endpoint de briefing — combina datos locales con API pública externa
#
# Elegí la API de consejos adviceslip.com (https://api.adviceslip.com/advice)
# porque es pública, sin auth, y retorna JSON limpio. Un "consejo de misión"
# encaja perfectamente con la narrativa de agentes: la Agencia les entrega
# un fragmento de inteligencia externa cada vez que se consulta su briefing.
#
# Plan de contingencia: si la API externa tarda más de 3 segundos o lanza
# cualquier excepción, activo un fallback con mensaje predeterminado. El
# servidor nunca se cuelga esperando a un tercero.
# ---------------------------------------------------------------------------
@app.get("/briefing/{nombre}", summary="Briefing del agente con intel externo")
def briefing_agente(nombre: str):
    """
    Combina datos locales del agente con información traída de una API
    pública externa. Incluye manejo de errores con fallback para garantizar
    que el servidor siempre responda, incluso si la API externa falla.
    """
    datos = despertar_agente(nombre)
    if datos is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")

    intel_externo = None
    try:
        # Timeout de 3 segundos: razonable para no degradar la experiencia
        respuesta = requests.get(EXTERNAL_API_URL, timeout=3)
        respuesta.raise_for_status()
        payload = respuesta.json()
        # adviceslip retorna: {"slip": {"id": N, "advice": "texto..."}}
        intel_externo = payload.get("slip", {}).get("advice", "Sin consejo disponible.")
    except requests.exceptions.Timeout:
        logger.warning("API externa (%s) tardó más de 3s. Activando fallback.", EXTERNAL_API_URL)
        intel_externo = "Mantén la calma y sigue el protocolo de tu última misión."
    except Exception as e:
        logger.error("Error al consultar API externa '%s': %s", EXTERNAL_API_URL, e)
        intel_externo = "Sin intel externo disponible en este momento. Opera con tus últimas instrucciones."

    return {
        "agente": datos,
        "intel_mision": intel_externo,
        "fuente_externa": EXTERNAL_API_URL,
    }

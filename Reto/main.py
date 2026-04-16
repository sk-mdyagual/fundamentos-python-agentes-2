"""
main.py — Servidor FastAPI de la Agencia de Agentes

Expone todos los endpoints de S5 más los nuevos endpoints de misiones
y briefing. Usa autenticación por API Key en los endpoints de escritura
y logging estructurado en lugar de print().

Ejecutar con:
    uvicorn main:app --reload
"""

import logging
import requests
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, field_validator

from agente import AgenteAdmin, despertar_con_clase
from config import API_KEY, EXTERNAL_API_URL
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
    completar_mision,
)

# -----------------------------------------------------------#
# Configuración del logging
# Reemplaza todos los print() por logger.* para tener
# trazabilidad con fecha, nivel y mensaje en cada evento.
# -----------------------------------------------------------#
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agencia de Agentes", version="1.0.0")

# Inicializar tablas al arrancar el servidor
crear_tablas()
logger.info("Base de datos inicializada. Tablas listas.")


# -----------------------------------------------------------#
# Modelos Pydantic
# -----------------------------------------------------------#
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
    energia_requerida: int = 0
    prioridad: str = "media"

    @field_validator("energia_requerida")
    @classmethod
    def energia_no_negativa(cls, v):
        if v < 0:
            raise ValueError("energia_requerida debe ser >= 0")
        return v

    @field_validator("prioridad")
    @classmethod
    def prioridad_valida(cls, v):
        if v not in ("baja", "media", "alta"):
            raise ValueError("prioridad debe ser 'baja', 'media' o 'alta'")
        return v


# -----------------------------------------------------------#
# Dependencia de autenticación con API Key
# Protege los endpoints de escritura sensible comparando
# el header X-API-KEY contra la variable de entorno AGENCIA_API_KEY.
# Retorna 401 si la clave no coincide o no se envía.
# -----------------------------------------------------------#
def verificar_api_key(x_api_key: str = Header(...)):
    if not API_KEY:
        logger.warning("AGENCIA_API_KEY no está configurada en .env — todos los accesos serán rechazados.")
    if x_api_key != API_KEY:
        logger.warning("Intento de acceso con API key inválida.")
        raise HTTPException(status_code=401, detail="API key inválida")


# -----------------------------------------------------------#
# Endpoints heredados de S5
# -----------------------------------------------------------#
@app.get("/")
def status():
    logger.info("GET / — verificación de estado del servidor")
    return {"status": "ok", "mensaje": "La Agencia está operativa."}


@app.get("/agente/{nombre}")
def obtener_agente(nombre: str):
    agente = despertar_agente(nombre)
    if agente is None:
        logger.warning(f"GET /agente/{nombre} — agente no encontrado")
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado.")
    logger.info(f"GET /agente/{nombre} — encontrado")
    return agente


@app.get("/agentes/")
def obtener_todos_los_agentes():
    agentes = listar_agentes()
    logger.info(f"GET /agentes/ — {len(agentes)} agentes listados")
    return agentes


@app.post("/agentes/", status_code=201)
def crear_agente(req: AgenteRequest):
    resultado = registrar_agente(req.nombre, req.rol, req.energia)
    if "ya existe" in resultado:
        logger.warning(f"POST /agentes/ — agente '{req.nombre}' ya existe")
        raise HTTPException(status_code=409, detail=resultado)
    logger.info(f"POST /agentes/ — agente '{req.nombre}' creado")
    return {"mensaje": resultado}


@app.post("/mensajes/", status_code=201)
def crear_mensaje(req: MensajeRequest):
    resultado = enviar_mensaje(req.remitente, req.destinatario, req.contenido)
    logger.info(f"POST /mensajes/ — mensaje de '{req.remitente}' a '{req.destinatario}'")
    return {"mensaje": resultado}


@app.get("/mensajes/{nombre}")
def obtener_mensajes(nombre: str):
    mensajes = leer_mensajes(nombre)
    logger.info(f"GET /mensajes/{nombre} — {len(mensajes)} mensajes")
    return mensajes


# -----------------------------------------------------------#
# Endpoints nuevos: misiones
# -----------------------------------------------------------#
@app.post("/misiones/", status_code=201, dependencies=[Depends(verificar_api_key)])
def nueva_mision(req: MisionRequest):
    agente = despertar_agente(req.agente_asignado)
    if agente is None:
        logger.warning(f"POST /misiones/ — agente '{req.agente_asignado}' no existe")
        raise HTTPException(status_code=404, detail=f"Agente '{req.agente_asignado}' no encontrado.")
    mision_id = crear_mision(
        req.titulo,
        req.descripcion,
        req.agente_asignado,
        req.energia_requerida,
        req.prioridad,
    )
    logger.info(f"POST /misiones/ — misión '{req.titulo}' (id={mision_id}) asignada a '{req.agente_asignado}'")
    return obtener_mision(mision_id)


@app.get("/misiones/{mision_id}")
def obtener_mision_endpoint(mision_id: int):
    mision = obtener_mision(mision_id)
    if mision is None:
        logger.warning(f"GET /misiones/{mision_id} — misión no encontrada")
        raise HTTPException(status_code=404, detail=f"Misión con id={mision_id} no encontrada.")
    logger.info(f"GET /misiones/{mision_id} — encontrada")
    return mision


@app.get("/agente/{nombre}/misiones")
def misiones_de_agente(nombre: str):
    agente = despertar_agente(nombre)
    if agente is None:
        logger.warning(f"GET /agente/{nombre}/misiones — agente no encontrado")
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado.")
    misiones = listar_misiones_agente(nombre)
    logger.info(f"GET /agente/{nombre}/misiones — {len(misiones)} misiones")
    return misiones


@app.post("/misiones/{mision_id}/completar", dependencies=[Depends(verificar_api_key)])
def completar_mision_endpoint(mision_id: int):
    mision = obtener_mision(mision_id)
    if mision is None:
        logger.warning(f"POST /misiones/{mision_id}/completar — misión no encontrada")
        raise HTTPException(status_code=404, detail=f"Misión con id={mision_id} no encontrada.")
    if mision["estado"] == "completada":
        logger.warning(f"POST /misiones/{mision_id}/completar — misión ya completada")
        raise HTTPException(status_code=409, detail="La misión ya está completada.")

    # Descontar energía via instancia de clase (patrón Factory + isinstance)
    agente_dict = despertar_agente(mision["agente_asignado"])
    if agente_dict:
        instancia = despertar_con_clase(agente_dict)
        instancia.tokens -= mision["energia_requerida"]
        nueva_energia = max(0, agente_dict["energia"] - mision["energia_requerida"])
        actualizar_energia(agente_dict["nombre"], nueva_energia)
        es_admin = isinstance(instancia, AgenteAdmin)
        logger.info(
            f"Energía de '{agente_dict['nombre']}' descontada: {agente_dict['energia']} → {nueva_energia} "
            f"(¿AgenteAdmin? {es_admin})"
        )

    mision_actualizada = completar_mision(mision_id)
    logger.info(f"POST /misiones/{mision_id}/completar — misión completada")
    return mision_actualizada


# -----------------------------------------------------------#
# Endpoint de briefing: datos locales + API externa
# Combina información del agente almacenada en SQLite con un
# dato externo obtenido de una API pública (consejo del día).
# Si la API externa falla, responde igualmente con los datos locales.
# -----------------------------------------------------------#
@app.get("/briefing/{nombre}")
def briefing(nombre: str):
    agente = despertar_agente(nombre)
    if agente is None:
        logger.warning(f"GET /briefing/{nombre} — agente no encontrado")
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado.")

    try:
        respuesta = requests.get(EXTERNAL_API_URL, timeout=3)
        respuesta.raise_for_status()
        dato_externo = respuesta.json()
    except Exception as error:
        logger.warning(f"GET /briefing/{nombre} — API externa no disponible: {error}")
        dato_externo = {"mensaje": "sin datos externos disponibles"}

    misiones = listar_misiones_agente(nombre)
    logger.info(f"GET /briefing/{nombre} — briefing generado")
    return {
        "agente": agente,
        "misiones_activas": [m for m in misiones if m["estado"] != "completada"],
        "fuente_externa": EXTERNAL_API_URL,
        "dato_externo": dato_externo,
    }

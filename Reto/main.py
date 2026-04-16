from __future__ import annotations

import logging
from typing import Literal, Optional

import requests
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field, field_validator

from agente import AgenteAdmin, PseudoAgente
from config import settings
from db import (
    actualizar_energia_agente,
    actualizar_estado_mision,
    agente_existe,
    crear_mision,
    crear_tablas,
    despertar_agente,
    enviar_mensaje,
    insertar_datos_semilla,
    leer_mensajes,
    listar_agentes,
    listar_misiones_por_agente,
    obtener_mision,
    registrar_agente,
)

# Uso INFO para cosas normales, WARNING cuando algo sale raro y ERROR si de verdad falla.
# El formato con fecha, nivel y mensaje me sirve para revisar rapido que paso.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("agencia")


class AgenteRequest(BaseModel):
    nombre: str = Field(min_length=1)
    rol: str = Field(min_length=1)
    energia: int = Field(gt=0)


class MensajeRequest(BaseModel):
    remitente: str = Field(min_length=1)
    destinatario: str = Field(min_length=1)
    contenido: str = Field(min_length=1)


class MisionRequest(BaseModel):
    titulo: str = Field(min_length=1)
    descripcion: str = ""
    agente_asignado: str = Field(min_length=1)
    estado: Literal["pendiente", "en_curso", "completada", "fallida"] = "pendiente"
    energia_requerida: int
    prioridad: Literal["baja", "media", "alta"] = "media"
    deadline: Optional[str] = None
    creado_por: str = "sistema"

    @field_validator("energia_requerida")
    @classmethod
    def validar_energia(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("energia_requerida debe ser mayor a cero")
        return value


app = FastAPI(
    title="Agencia de Agentes API",
    description="Reto de consolidacion con FastAPI, SQLite, auth por API key y briefing externo.",
    version="1.0.0",
)


@app.on_event("startup")
def startup_event() -> None:
    crear_tablas()
    insertar_datos_semilla()
    logger.info("Servidor iniciado con tablas listas y datos semilla disponibles")


# Protejo solo los endpoints que cambian datos. Los GET los dejo libres para consultar sin tanta vuelta.
# La idea es que nadie cree o modifique cosas si no manda una X-API-KEY valida.
def verificar_api_key(x_api_key: Optional[str] = Header(default=None, alias="X-API-KEY")) -> None:
    if not x_api_key or x_api_key != settings.api_key:
        logger.warning("Intento de escritura sin API key valida")
        raise HTTPException(status_code=401, detail="API key invalida")


def reconstruir_agente(nombre: str) -> PseudoAgente:
    data = despertar_agente(nombre)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")

    if data["rol"] == "admin":
        agente = AgenteAdmin(nombre=data["nombre"], rol=data["rol"], tokens=data["energia"])
    else:
        agente = PseudoAgente(nombre=data["nombre"], rol=data["rol"], tokens=data["energia"])
    return agente


@app.get("/")
def inicio() -> dict:
    return {"status": "online", "mensaje": "Bienvenido a la Agencia de Agentes"}


@app.get("/agente/{nombre}")
def obtener_agente(nombre: str) -> dict:
    agente = reconstruir_agente(nombre)
    response = {
        "nombre": agente.nombre,
        "rol": agente.rol,
        "energia": agente.tokens,
        "tipo_instancia": agente.__class__.__name__,
        "es_admin_instance": isinstance(agente, AgenteAdmin),
    }
    return response


@app.get("/agentes/")
def obtener_todos_los_agentes() -> list[dict]:
    return listar_agentes()


@app.post("/agentes/", dependencies=[Depends(verificar_api_key)], status_code=201)
def crear_agente(agente: AgenteRequest) -> dict:
    ok = registrar_agente(agente.nombre, agente.rol, agente.energia)
    if not ok:
        logger.warning("No se pudo registrar agente duplicado: %s", agente.nombre)
        raise HTTPException(status_code=409, detail=f"El agente '{agente.nombre}' ya existe")

    logger.info("Agente creado: %s (%s)", agente.nombre, agente.rol)
    return {"mensaje": f"Agente '{agente.nombre}' registrado con exito"}


@app.post("/mensajes/", dependencies=[Depends(verificar_api_key)], status_code=201)
def crear_mensaje(mensaje: MensajeRequest) -> dict:
    if not agente_existe(mensaje.remitente):
        raise HTTPException(status_code=404, detail=f"Remitente '{mensaje.remitente}' no existe")
    if not agente_existe(mensaje.destinatario):
        raise HTTPException(status_code=404, detail=f"Destinatario '{mensaje.destinatario}' no existe")

    resultado = enviar_mensaje(mensaje.remitente, mensaje.destinatario, mensaje.contenido)
    logger.info("Mensaje enviado de %s a %s", mensaje.remitente, mensaje.destinatario)
    return {"mensaje": resultado}


@app.get("/mensajes/{nombre}")
def obtener_mensajes(nombre: str) -> list[dict]:
    if not agente_existe(nombre):
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    return leer_mensajes(nombre)


@app.post("/misiones/", dependencies=[Depends(verificar_api_key)], status_code=201)
def crear_mision_endpoint(mision: MisionRequest) -> dict:
    if not agente_existe(mision.agente_asignado):
        raise HTTPException(
            status_code=404,
            detail=f"El agente asignado '{mision.agente_asignado}' no existe",
        )

    mision_id = crear_mision(
        titulo=mision.titulo,
        descripcion=mision.descripcion,
        agente_asignado=mision.agente_asignado,
        estado=mision.estado,
        energia_requerida=mision.energia_requerida,
        prioridad=mision.prioridad,
        deadline=mision.deadline,
        creado_por=mision.creado_por,
    )
    logger.info("Mision creada: id=%s, agente=%s", mision_id, mision.agente_asignado)
    return {"id": mision_id, "mensaje": "Mision creada"}


@app.get("/misiones/{mision_id}")
def obtener_mision_endpoint(mision_id: int) -> dict:
    mision = obtener_mision(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Mision {mision_id} no encontrada")
    return mision


@app.get("/agente/{nombre}/misiones")
def listar_misiones_agente(nombre: str) -> list[dict]:
    if not agente_existe(nombre):
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    return listar_misiones_por_agente(nombre)


@app.post("/misiones/{mision_id}/completar", dependencies=[Depends(verificar_api_key)])
def completar_mision(mision_id: int) -> dict:
    mision = obtener_mision(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Mision {mision_id} no encontrada")

    agente = reconstruir_agente(mision["agente_asignado"])
    energia_requerida = int(mision["energia_requerida"])

    try:
        energia_restante = agente.completar_mision(energia_requerida)
    except RuntimeError as exc:
        actualizar_estado_mision(mision_id, "fallida")
        logger.warning("Mision %s fallida por energia insuficiente", mision_id)
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    actualizar_estado_mision(mision_id, "completada")
    actualizar_energia_agente(agente.nombre, energia_restante)

    logger.info("Mision %s completada por %s", mision_id, agente.nombre)
    return {
        "mensaje": "Mision completada",
        "mision_id": mision_id,
        "agente": agente.nombre,
        "energia_restante": energia_restante,
        "tipo_instancia": agente.__class__.__name__,
        "es_admin_instance": isinstance(agente, AgenteAdmin),
    }


# Elegi catfact.ninja porque responde facil y no pide login.
# Si se cae o tarda, el endpoint sigue respondiendo con un respaldo local para no frenar la API.
@app.get("/briefing/{nombre}")
def briefing(nombre: str) -> dict:
    agente_data = despertar_agente(nombre)
    if agente_data is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")

    misiones = listar_misiones_por_agente(nombre)
    resumen_estados = {
        "pendiente": 0,
        "en_curso": 0,
        "completada": 0,
        "fallida": 0,
    }
    for mision in misiones:
        estado = mision.get("estado", "pendiente")
        if estado in resumen_estados:
            resumen_estados[estado] += 1

    dato_externo = "Sin dato externo"
    fuente_externa = settings.external_api_url
    contingencia = False

    try:
        response = requests.get(settings.external_api_url, timeout=settings.external_api_timeout)
        response.raise_for_status()
        payload = response.json()
        dato_externo = payload.get("fact") or payload.get("advice") or str(payload)
    except requests.RequestException as exc:
        contingencia = True
        dato_externo = "No fue posible consultar la fuente externa. Se usa briefing local de respaldo."
        logger.warning("Fallo API externa en briefing de %s: %s", nombre, exc)

    return {
        "agente": agente_data,
        "misiones": {
            "total": len(misiones),
            "por_estado": resumen_estados,
        },
        "insight_externo": dato_externo,
        "fuente_externa": fuente_externa,
        "contingencia_activada": contingencia,
    }

# main.py — Servidor FastAPI para Cyber-Mercs Corporation
# AUDITORÍA: Este archivo NO usa print(). Todo registro pasa por logger.
# Cada endpoint de escritura está protegido por API Key vía el header X-API-KEY.

import logging
import random
from contextlib import asynccontextmanager
from typing import Optional

import httpx
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, field_validator

from config import CORP_API_KEY, CRYPTO_API_URL
from agente import instanciar_mercenario, HP_MAX_POR_CLASE
from rng import resolver_evento_autonomo, resolver_evento_d20, reduccion_dano_implantes
from db import (
    crear_tablas,
    hay_mercenarios,
    registrar_merc,
    obtener_merc,
    listar_mercs,
    actualizar_hp,
    actualizar_creditos,
    descontar_creditos_atomico,
    actualizar_estado_vital,
    crear_contrato_db,
    obtener_contrato_db,
    completar_contrato_db,
    fallar_contrato_db,
    guardar_mensaje,
    leer_mensajes,
    agregar_implante,
    listar_implantes,
    obtener_contratos_por_merc,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

CLASES_PERMITIDAS = ["hacker", "tanque", "sniper", "fixer", "novato"]
ESTADOS_PERMITIDOS = ["vivo", "muerto"]
TIPOS_CONTRATO = ["asalto", "infiltracion", "hackeo", "sabotaje", "combate"]


# ──────────────────────────────────────────────────────────────────
# Modelos Pydantic con validadores custom
# ──────────────────────────────────────────────────────────────────

class MercRequest(BaseModel):
    alias: str
    clase_nombre: str = "novato"
    hp: int = 100
    creditos: int = 0

    @field_validator("alias")
    @classmethod
    def alias_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError("El alias no puede estar vacío.")
        return v.strip()

    @field_validator("clase_nombre")
    @classmethod
    def clase_valida(cls, v):
        if v.lower() not in CLASES_PERMITIDAS:
            raise ValueError(f"Clase '{v}' no válida. Opciones: {CLASES_PERMITIDAS}")
        return v.lower()

    @field_validator("hp")
    @classmethod
    def hp_positivo(cls, v):
        if v <= 0:
            raise ValueError("Los HP deben ser mayores a 0.")
        return v


class ContratoRequest(BaseModel):
    titulo: str
    tipo_contrato: str = "sabotaje"
    mercenario_asignado: str
    dano_estimado: int = 20
    pago_base: int = 500

    @field_validator("titulo")
    @classmethod
    def titulo_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError("El título del contrato no puede estar vacío.")
        return v.strip()

    @field_validator("dano_estimado")
    @classmethod
    def dano_no_negativo(cls, v):
        if v < 0:
            raise ValueError("El daño estimado no puede ser negativo.")
        return v

    @field_validator("pago_base")
    @classmethod
    def pago_no_negativo(cls, v):
        if v < 0:
            raise ValueError("El pago base no puede ser negativo.")
        return v


class MensajeRequest(BaseModel):
    remitente: str
    destinatario: str
    contenido: str

    @field_validator("contenido")
    @classmethod
    def contenido_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError("El contenido del mensaje no puede estar vacío.")
        return v.strip()


class EstadoRequest(BaseModel):
    estado_vital: str

    @field_validator("estado_vital")
    @classmethod
    def estado_valido(cls, v):
        if v.lower() not in ESTADOS_PERMITIDOS:
            raise ValueError(f"Estado '{v}' no válido. Opciones: {ESTADOS_PERMITIDOS}")
        return v.lower()


class EjecutarRequest(BaseModel):
    tirada_dado: Optional[int] = None

    @field_validator("tirada_dado")
    @classmethod
    def tirada_en_rango(cls, v):
        if v is not None and (v < 1 or v > 20):
            raise ValueError("La tirada del D20 debe estar entre 1 y 20.")
        return v


class SobornoRequest(BaseModel):
    monto: int

    @field_validator("monto")
    @classmethod
    def monto_positivo(cls, v):
        if v <= 0:
            raise ValueError("El monto del soborno debe ser mayor a 0.")
        return v


# ──────────────────────────────────────────────────────────────────
# Lifespan: crea tablas y siembra solo si la DB está vacía.
# Antes se hacía reset_db() en cada arranque, lo que destruía la
# trazabilidad histórica entre reinicios. Ahora la persistencia es real.
# ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(_app: FastAPI):
    crear_tablas()
    if not hay_mercenarios():
        _insertar_datos_semilla()
        logger.info("DB vacía: datos semilla insertados.")
    else:
        logger.info("DB con datos existentes: se preserva la trazabilidad.")
    yield


def _insertar_datos_semilla():
    """Inserta datos mínimos en la DB. Se ejecuta solo cuando la DB está vacía
    o tras un /reset explícito."""
    registrar_merc("Jinx", "hacker", 100, 0)
    registrar_merc("Vi", "tanque", 200, 100)
    registrar_merc("Silco", "fixer", 90, 5000)

    cid1 = crear_contrato_db("Atraco al Banco Piltover", "asalto", "Vi", 50, 1000)
    completar_contrato_db(cid1)
    cid2 = crear_contrato_db("Infiltración Hextech", "infiltracion", "Jinx", 40, 1500)
    fallar_contrato_db(cid2)
    crear_contrato_db("Sabotaje al Consejo", "sabotaje", "Silco", 30, 2000)

    guardar_mensaje("Silco", "Jinx", "Necesito los datos del mainframe de Piltover antes de medianoche.")
    guardar_mensaje("Jinx", "Vi", "¿Sigues viva, hermanita? Te vi en el último contrato.")
    guardar_mensaje("Vi", "Jinx", "Deja de volarme los objetivos. La próxima vez te cobro.")
    guardar_mensaje("Silco", "Vi", "Buen trabajo en el banco. Tus créditos han sido transferidos.")
    guardar_mensaje("Vi", "Silco", "He terminado el trabajo. No me busques más.")


app = FastAPI(
    title="Cyber-Mercs Corporation",
    description="Plataforma de gestión de mercenarios y contratos en el bajo mundo.",
    version="1.1",
    lifespan=lifespan,
)


# ──────────────────────────────────────────────────────────────────
# Auth: header X-API-KEY obligatorio en endpoints de escritura.
# Los GET son públicos para auditoría externa.
# ──────────────────────────────────────────────────────────────────

def verificar_api_key(x_api_key: str = Header(...)):
    if x_api_key != CORP_API_KEY:
        logger.warning("Intento de acceso denegado (API Key inválida).")
        raise HTTPException(status_code=401, detail="API Key de la corporación inválida.")
    return x_api_key


# ──────────────────────────────────────────────────────────────────
# Multiplicador del Mercado Negro: precio real de BTC vía CoinGecko.
# Async + httpx para no bloquear el event loop bajo carga.
# Si la API falla, fallback a 1.0x (la simulación nunca cae por un tercero).
# ──────────────────────────────────────────────────────────────────

IMPLANTES_DISPONIBLES = [
    "Brazo Biónico de Titanio",
    "Ojo Óptico Kiroshi",
    "Neuro-Enlace Cuántico",
    "Piernas Neumáticas",
    "Subdermal Armor v2",
]


_cache_multiplicador: float | None = None


async def obtener_multiplicador_mercado_negro() -> float:
    """Consulta el precio real del Bitcoin (CoinGecko) y lo cachea por sesión.
    Evita llamar a la API en cada contrato — el precio no cambia en 30 segundos.
    Fallback seguro a 1.0x si la API responde error o se cae la red."""
    global _cache_multiplicador
    if _cache_multiplicador is not None:
        return _cache_multiplicador

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(CRYPTO_API_URL)
            if r.status_code == 200:
                data = r.json()
                precio_btc = float(data["bitcoin"]["usd"])
                multiplicador = 1.0 + (precio_btc / 100000.0)
                _cache_multiplicador = round(multiplicador, 2)
                logger.info(f"BTC = ${precio_btc:,.2f}. Multiplicador: {_cache_multiplicador:.2f}x (cacheado)")
                return _cache_multiplicador
    except Exception as e:
        logger.error(f"Fallo de conexión al Mercado Negro: {e}")

    logger.warning("Usando multiplicador estándar (1.0x).")
    _cache_multiplicador = 1.0
    return 1.0


# ──────────────────────────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────────────────────────

@app.get("/")
def raiz():
    return {"mensaje": "Cyber-Mercs Corporation. Sistema Online."}


@app.delete("/reset")
def resetear_servidor(api_key: str = Depends(verificar_api_key)):
    """Reinicia la base de datos y el caché crypto para una simulación limpia."""
    global _cache_multiplicador
    _cache_multiplicador = None
    from db import reset_db
    reset_db()
    crear_tablas()
    _insertar_datos_semilla()
    logger.info("Base de datos reseteada vía API.")
    return {"mensaje": "Entorno simulado reiniciado con datos semilla."}


@app.post("/mercs/")
def registrar_mercenario(merc: MercRequest, api_key: str = Depends(verificar_api_key)):
    if obtener_merc(merc.alias):
        logger.warning(f"Intento de registrar alias duplicado: '{merc.alias}'.")
        raise HTTPException(status_code=409, detail=f"El alias '{merc.alias}' ya está en el sistema.")

    registrar_merc(merc.alias, merc.clase_nombre, merc.hp, merc.creditos)
    logger.info(f"Mercenario '{merc.alias}' registrado (clase={merc.clase_nombre}, hp={merc.hp}).")
    return {"mensaje": f"Mercenario {merc.alias} ingresado a la red corporativa.", "alias": merc.alias}


@app.get("/mercs/")
def obtener_todos_mercs():
    logger.info("Listando mercenarios activos e inactivos.")
    return listar_mercs()


@app.put("/mercs/{alias}/estado")
def actualizar_estado(alias: str, req: EstadoRequest, api_key: str = Depends(verificar_api_key)):
    if not obtener_merc(alias):
        raise HTTPException(status_code=404, detail="Mercenario no encontrado")
    actualizar_estado_vital(alias, req.estado_vital)
    logger.info(f"Estado de '{alias}' actualizado a {req.estado_vital}")
    return {"mensaje": f"Estado de {alias} actualizado a {req.estado_vital}"}


@app.post("/mercs/{alias}/sobornar")
def sobornar_hunter(alias: str, req: SobornoRequest, api_key: str = Depends(verificar_api_key)):
    """Pago de soborno con descuento ATÓMICO (un solo UPDATE WHERE creditos >= monto).
    Cierra la race condition del read-modify-write anterior."""
    if not obtener_merc(alias):
        raise HTTPException(status_code=404, detail="Mercenario no encontrado")

    if descontar_creditos_atomico(alias, req.monto):
        logger.info(f"'{alias}' pagó un soborno de {req.monto}C.")
        return {"mensaje": "Soborno aceptado. El cazador se retira.", "exito": True}

    logger.warning(f"'{alias}' intentó sobornar pero no tiene fondos suficientes.")
    raise HTTPException(status_code=400, detail="Fondos insuficientes para el soborno.")


@app.post("/contratos/")
def publicar_contrato(c: ContratoRequest, api_key: str = Depends(verificar_api_key)):
    if obtener_merc(c.mercenario_asignado) is None:
        raise HTTPException(status_code=404, detail=f"Mercenario asignado '{c.mercenario_asignado}' no existe.")

    cid = crear_contrato_db(c.titulo, c.tipo_contrato, c.mercenario_asignado, c.dano_estimado, c.pago_base)
    logger.info(f"Contrato #{cid} '{c.titulo}' publicado y asignado a '{c.mercenario_asignado}'.")
    return {"id": cid, "mensaje": "Contrato registrado y encriptado en el servidor."}


@app.post("/contratos/{id}/ejecutar")
async def ejecutar_contrato(id: int, req: Optional[EjecutarRequest] = None, api_key: str = Depends(verificar_api_key)):
    """Ejecuta un contrato usando el motor RNG de rng.py.
    - Modo autónomo (sin dado): distribución ponderada por afinidad clase/contrato.
    - Modo D20 (con dado): umbrales dinámicos por afinidad.
    - HP bajo degrada la afinidad (herido = más riesgo).
    - Implantes dan efectos mecánicos (reducción de daño, salvar de desastre)."""
    contrato = obtener_contrato_db(id)
    if contrato is None:
        raise HTTPException(status_code=404, detail="Contrato no encontrado.")
    if contrato["estado"] != "pendiente":
        raise HTTPException(status_code=400, detail=f"Contrato ya está {contrato['estado']}.")

    alias = contrato["mercenario_asignado"]
    merc_data = obtener_merc(alias)
    if not merc_data or merc_data["estado_vital"] == "muerto":
        fallar_contrato_db(id)
        raise HTTPException(status_code=400, detail=f"El mercenario '{alias}' está muerto o no disponible.")

    mercenario = instanciar_mercenario(merc_data)
    clase = merc_data["clase_nombre"]
    tipo = contrato["tipo_contrato"]
    hp_max = HP_MAX_POR_CLASE.get(clase, 100)

    # Inventario de implantes del merc (para efectos mecánicos)
    inv = [i["nombre_implante"] for i in listar_implantes(alias)]

    # ── Resolver evento con el nuevo motor RNG ──
    if req and req.tirada_dado is not None:
        evento = resolver_evento_d20(req.tirada_dado, clase, tipo, merc_data["hp"], hp_max, inv)
    else:
        evento = resolver_evento_autonomo(clase, tipo, merc_data["hp"], hp_max, inv)

    # ── Calcular daño ──
    dano_base = contrato["dano_estimado"]
    dano_real = int(dano_base * evento.multiplicador_dano)

    # Reducción fija por implantes (Brazo Biónico, Subdermal Armor)
    dano_real = max(0, dano_real - reduccion_dano_implantes(tipo, inv))

    # La clase sigue modificando el daño vía POO (Hacker /2 en hackeo, Tanque -10 en combate)
    sobrevive = mercenario.recibir_dano(dano_real, tipo)
    hp_consumido = merc_data["hp"] - mercenario.hp

    actualizar_hp(alias, mercenario.hp)

    # ── Muerte ──
    if not sobrevive:
        actualizar_estado_vital(alias, "muerto")
        fallar_contrato_db(id)
        logger.warning(f"'{alias}' murió ejecutando el contrato #{id}. Evento: {evento.nombre}")
        return {
            "mensaje": "Mercenario caído en combate.",
            "estado_vital": "muerto",
            "hp_actual": 0,
            "hp_gastado": hp_consumido,
            "evento": evento.nombre,
        }

    # ── Misión fallida (Desastre Absoluto) ──
    if evento.mision_fallida:
        fallar_contrato_db(id)
        logger.warning(f"'{alias}' falló el contrato #{id}. Evento: {evento.nombre}")
        return {
            "mensaje": "Misión Fracasada.",
            "exito_mision": False,
            "evento": evento.nombre,
            "hp_gastado": hp_consumido,
            "hp_actual": mercenario.hp,
        }

    # ── Pago con crypto ──
    multiplicador_crypto = await obtener_multiplicador_mercado_negro()
    pago_final = int(contrato["pago_base"] * multiplicador_crypto * evento.multiplicador_pago)

    mercenario.cobrar_pago(pago_final)
    actualizar_creditos(alias, mercenario.creditos)
    completar_contrato_db(id)

    # ── Loot de implantes ──
    implante_obtenido = None
    if evento.implante_garantizado:
        chance_implante = 1.0
    elif evento.implante_boost:
        chance_implante = 0.9
    else:
        chance_implante = 0.6

    if random.random() < chance_implante:
        ya_posee = {i["nombre_implante"] for i in listar_implantes(alias)}
        candidatos = [i for i in IMPLANTES_DISPONIBLES if i not in ya_posee]
        if candidatos:
            implante_obtenido = random.choice(candidatos)
            agregar_implante(alias, implante_obtenido)

    logger.info(
        f"Contrato #{id} completado por '{alias}'. Evento: {evento.nombre}. "
        f"HP: {mercenario.hp}. Pago: {pago_final}C (x{multiplicador_crypto})"
    )

    return {
        "mensaje": "Contrato ejecutado exitosamente",
        "evento": evento.nombre,
        "hp_gastado": hp_consumido,
        "hp_actual": mercenario.hp,
        "pago_recibido": pago_final,
        "multiplicador_mercado": multiplicador_crypto,
        "multiplicador_pago_evento": evento.multiplicador_pago,
        "implante_obtenido": implante_obtenido,
    }


@app.post("/contratos/{id}/fallar")
def fallar_contrato(id: int, api_key: str = Depends(verificar_api_key)):
    if not obtener_contrato_db(id):
        raise HTTPException(status_code=404, detail="Contrato no encontrado")
    fallar_contrato_db(id)
    logger.info(f"Contrato #{id} marcado como FALLIDA.")
    return {"mensaje": "Contrato abortado", "estado": "fallido"}


@app.post("/comunicaciones/")
def enviar_mensaje(msg: MensajeRequest, api_key: str = Depends(verificar_api_key)):
    guardar_mensaje(msg.remitente, msg.destinatario, msg.contenido)
    logger.info(f"Comunicación encriptada de '{msg.remitente}' a '{msg.destinatario}'.")
    return {"mensaje": "Comunicación encriptada enviada exitosamente."}


@app.get("/comunicaciones/{alias}")
def obtener_mensajes(alias: str):
    logger.info(f"Desencriptando bandeja de mensajes de '{alias}'.")
    return leer_mensajes(alias)


@app.get("/implantes/{alias}")
def inventario_implantes(alias: str):
    return listar_implantes(alias)


@app.get("/contratos/mercenario/{alias}")
def contratos_por_mercenario(alias: str):
    return obtener_contratos_por_merc(alias)

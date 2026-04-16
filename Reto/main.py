"""
main.py — Servidor FastAPI para la Agencia de Agentes

Este módulo define la API REST que expone las operaciones de la Agencia.
Importa las clases de dominio (agente.py) y las funciones de persistencia (db.py).

NO define clases de dominio ni queries SQL en crudo aquí.
"""

import logging
import requests
from typing import Optional
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field

# Importaciones locales
from config import AGENCIA_API_KEY, EXTERNAL_API_URL
import db
from agente import PseudoAgente, AgenteAdmin, reconstruir_agente


# ===================================================================
# CONFIGURACIÓN DEL LOGGING
# ===================================================================
# Justificación de niveles:
# - INFO: eventos normales del ciclo de vida (agente creado, misión completada)
# - WARNING: situaciones anómalas pero no críticas (API externa lenta, fallback activado)
# - ERROR: fallos que impiden completar una operación (integridad SQL, validaciones)
#
# Formato: [timestamp] [nivel] mensaje
# Nivel por defecto: INFO (para producción, cambiar a WARNING)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ===================================================================
# INICIALIZACIÓN DE LA BASE DE DATOS
# ===================================================================
# Crear tablas al iniciar el servidor (idempotente)
db.crear_tablas()
logger.info("Base de datos inicializada. Tablas verificadas: agentes, mensajes, misiones.")


# ===================================================================
# MODELOS PYDANTIC (validación de entrada/salida)
# ===================================================================

class AgenteRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    rol: str = Field(..., min_length=1, max_length=20)
    energia: int = Field(..., ge=0, le=1000)


class MensajeRequest(BaseModel):
    remitente: str
    destinatario: str
    contenido: str


class MisionRequest(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None
    agente_asignado: str
    energia_requerida: int = Field(..., gt=0)
    prioridad: str = Field(default="media")
    recompensa: int = Field(default=0)
    creado_por: str = Field(default="sistema")


# ===================================================================
# AUTENTICACIÓN CON API KEY (Salto de complejidad 5.1)
# ===================================================================
# Decisión de ingeniería: Proteger TODOS los endpoints de escritura (POST, PUT, DELETE).
# Los GET quedan libres porque son de solo lectura y facilitan la
# integración de otros sistemas sin necesidad de autenticación.
# 
# Justificación: en una API pública, los datos pueden leerse sin riesgo,
# pero solo operadores autorizados deben poder modificar el estado del sistema.
async def verificar_api_key(x_api_key: str = Header(..., alias="X-API-KEY")) -> str:
    """
    Dependencia de FastAPI que verifica el header X-API-KEY.
    Si no coincide con la configurada, lanza HTTPException 401.
    Retorna la key si es válida (para logging u otros usos).
    """
    if x_api_key != AGENCIA_API_KEY:
        logger.warning(f"Intento de acceso con API key inválida: {x_api_key[:10]}...")
        raise HTTPException(status_code=401, detail="API key inválida o ausente")
    return x_api_key


# ===================================================================
# APLICACIÓN FASTAPI
# ===================================================================
app = FastAPI(
    title="🏛️ Agencia de Agentes",
    description="Sistema de gestión de agentes, misiones y mensajes con persistencia SQLite",
    version="1.0.0"
)


# ===================================================================
# ENDPOINTS BASE (reutilizados de Semana 5)
# ===================================================================

@app.get("/")
async def raiz():
    """Endpoint de verificación: el servidor está vivo."""
    logger.info("Endpoint raíz consultado - servidor operativo")
    return {
        "mensaje": "Bienvenido a la Agencia de Agentes",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/agentes/")
async def obtener_agentes():
    """Lista todos los agentes registrados."""
    agentes = db.listar_agentes()
    logger.info(f"Listado de agentes solicitado. Total: {len(agentes)}")
    return {"agentes": agentes, "total": len(agentes)}


@app.get("/agente/{nombre}")
async def obtener_agente(nombre: str):
    """Obtiene información de un agente por nombre."""
    datos = db.despertar_agente(nombre)
    if datos is None:
        logger.warning(f"Intento de acceso a agente inexistente: {nombre}")
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    
    logger.info(f"Información del agente '{nombre}' consultada")
    return datos


@app.post("/agentes/", dependencies=[Depends(verificar_api_key)])
async def crear_agente(agente: AgenteRequest):
    """Crea un nuevo agente (requiere autenticación)."""
    resultado = db.registrar_agente(agente.nombre, agente.rol, agente.energia)
    
    if "Error" in resultado:
        logger.error(f"Fallo al crear agente '{agente.nombre}': ya existe")
        raise HTTPException(status_code=409, detail=resultado)
    
    logger.info(f"Agente '{agente.nombre}' creado exitosamente (rol: {agente.rol}, energía: {agente.energia})")
    return {"mensaje": resultado, "agente": agente.dict()}


# ===================================================================
# ENDPOINTS DE MENSAJES (reutilizados de Semana 5)
# ===================================================================

@app.post("/mensajes/", dependencies=[Depends(verificar_api_key)])
async def crear_mensaje(mensaje: MensajeRequest):
    """Envía un mensaje entre agentes (requiere autenticación)."""
    # Verificar que ambos agentes existen
    remitente_existe = db.despertar_agente(mensaje.remitente)
    destinatario_existe = db.despertar_agente(mensaje.destinatario)
    
    if not remitente_existe:
        logger.error(f"Intento de enviar mensaje desde agente inexistente: {mensaje.remitente}")
        raise HTTPException(status_code=404, detail=f"Remitente '{mensaje.remitente}' no existe")
    
    if not destinatario_existe:
        logger.error(f"Intento de enviar mensaje a agente inexistente: {mensaje.destinatario}")
        raise HTTPException(status_code=404, detail=f"Destinatario '{mensaje.destinatario}' no existe")
    
    resultado = db.enviar_mensaje(mensaje.remitente, mensaje.destinatario, mensaje.contenido)
    logger.info(f"Mensaje enviado de '{mensaje.remitente}' a '{mensaje.destinatario}'")
    return {"mensaje": resultado}


@app.get("/mensajes/{nombre}")
async def obtener_mensajes(nombre: str):
    """Lee la bandeja de mensajes de un agente."""
    # Verificar que el agente existe
    agente_existe = db.despertar_agente(nombre)
    if not agente_existe:
        logger.warning(f"Consulta de mensajes para agente inexistente: {nombre}")
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    
    mensajes = db.leer_mensajes(nombre)
    logger.info(f"Bandeja de '{nombre}' consultada. Total mensajes: {len(mensajes)}")
    return {"agente": nombre, "mensajes": mensajes, "total": len(mensajes)}


# ===================================================================
# ENDPOINTS DE MISIONES (NUEVOS para el reto)
# ===================================================================

@app.post("/misiones/", dependencies=[Depends(verificar_api_key)])
async def crear_mision(mision: MisionRequest):
    """
    Crea una nueva misión (requiere autenticación).
    Valida que el agente asignado exista.
    """
    # Verificar que el agente existe
    agente_existe = db.despertar_agente(mision.agente_asignado)
    if not agente_existe:
        logger.error(f"Intento de crear misión para agente inexistente: {mision.agente_asignado}")
        raise HTTPException(
            status_code=404,
            detail=f"Agente '{mision.agente_asignado}' no existe"
        )
    
    # Crear la misión
    mision_id = db.crear_mision(
        titulo=mision.titulo,
        descripcion=mision.descripcion,
        agente_asignado=mision.agente_asignado,
        energia_requerida=mision.energia_requerida,
        prioridad=mision.prioridad,
        recompensa=mision.recompensa,
        creado_por=mision.creado_por
    )
    
    logger.info(f"Misión #{mision_id} '{mision.titulo}' creada y asignada a '{mision.agente_asignado}'")
    return {
        "mensaje": f"Misión creada exitosamente",
        "mision_id": mision_id,
        "mision": mision.dict()
    }


@app.get("/misiones/{id}")
async def obtener_mision(id: int):
    """Obtiene una misión por su ID."""
    mision = db.obtener_mision(id)
    if mision is None:
        logger.warning(f"Consulta de misión inexistente: #{id}")
        raise HTTPException(status_code=404, detail=f"Misión #{id} no encontrada")
    
    logger.info(f"Misión #{id} consultada")
    return mision


@app.get("/agente/{nombre}/misiones")
async def obtener_misiones_agente(nombre: str):
    """Lista todas las misiones asignadas a un agente."""
    # Verificar que el agente existe
    agente_existe = db.despertar_agente(nombre)
    if not agente_existe:
        logger.warning(f"Consulta de misiones para agente inexistente: {nombre}")
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    
    misiones = db.listar_misiones_agente(nombre)
    logger.info(f"Misiones del agente '{nombre}' consultadas. Total: {len(misiones)}")
    return {
        "agente": nombre,
        "misiones": misiones,
        "total": len(misiones)
    }


@app.post("/misiones/{id}/completar", dependencies=[Depends(verificar_api_key)])
async def completar_mision_endpoint(id: int):
    """
    Completa una misión (requiere autenticación).
    AQUÍ SE USA LA CLASE DE DOMINIO (Requerimiento R2):
    - Despierta el agente desde la DB
    - Reconstruye la instancia correcta (PseudoAgente o AgenteAdmin)
    - Descuenta energía a través del método de la clase
    - Persiste el nuevo estado del agente
    """
    # Obtener la misión
    mision = db.obtener_mision(id)
    if mision is None:
        logger.error(f"Intento de completar misión inexistente: #{id}")
        raise HTTPException(status_code=404, detail=f"Misión #{id} no encontrada")
    
    # Verificar que no esté ya completada
    if mision["estado"] == "completada":
        logger.warning(f"Intento de completar misión ya completada: #{id}")
        raise HTTPException(status_code=400, detail=f"Misión #{id} ya está completada")
    
    # Despertar al agente asignado
    datos_agente = db.despertar_agente(mision["agente_asignado"])
    if datos_agente is None:
        logger.error(f"Agente asignado a misión #{id} no existe: {mision['agente_asignado']}")
        raise HTTPException(
            status_code=404,
            detail=f"Agente '{mision['agente_asignado']}' no encontrado"
        )
    
    # RECONSTRUIR LA CLASE (R2: aquí es donde importa la herencia)
    agente = reconstruir_agente(datos_agente)
    
    # Verificar tipo de instancia (para logging)
    tipo_agente = "AgenteAdmin" if isinstance(agente, AgenteAdmin) else "PseudoAgente"
    logger.info(f"Completando misión #{id} con agente '{agente.nombre}' (tipo: {tipo_agente})")
    
    # Descontar energía usando el método de la clase
    energia_suficiente = agente.consumir_energia(mision["energia_requerida"])
    
    if not energia_suficiente and not isinstance(agente, AgenteAdmin):
        logger.warning(f"Agente '{agente.nombre}' sin energía suficiente para misión #{id}")
        raise HTTPException(
            status_code=400,
            detail=f"Agente '{agente.nombre}' no tiene energía suficiente (actual: {agente.energia}, requerida: {mision['energia_requerida']})"
        )
    
    # Actualizar energía en la base de datos
    db.actualizar_energia_agente(agente.nombre, agente.energia)
    
    # Marcar misión como completada
    exito = db.completar_mision(id)
    if not exito:
        logger.error(f"Fallo al marcar misión #{id} como completada en la DB")
        raise HTTPException(status_code=500, detail="Error al completar la misión")
    
    logger.info(f"Misión #{id} completada exitosamente. Energía restante de '{agente.nombre}': {agente.energia}")
    
    return {
        "mensaje": f"Misión #{id} completada exitosamente",
        "agente": agente.nombre,
        "energia_restante": agente.energia,
        "tipo_agente": tipo_agente
    }


# ===================================================================
# ENDPOINT BRIEFING con API EXTERNA (Salto de complejidad 5.2)
# ===================================================================
# API elegida: Advice Slip API (https://api.adviceslip.com)
# Por qué: Proporciona consejos aleatorios en formato JSON sin autenticación.
# Encaja con la narrativa porque los agentes necesitan "sabiduría externa"
# antes de iniciar sus misiones. Añade al briefing un consejo motivacional.
#
# Plan de contingencia: Si la API falla o tarda más de 3 segundos,
# el endpoint responde con un mensaje de fallback y continúa operando.
# NO bloqueamos la respuesta por culpa de un servicio externo.
@app.get("/briefing/{nombre}")
async def obtener_briefing(nombre: str):
    """
    Genera un briefing del agente combinando:
    - Datos locales (nombre, rol, energía, misiones)
    - Consejo motivacional de una API externa (Advice Slip API)
    
    Si la API externa falla, se proporciona un mensaje de contingencia.
    """
    # Obtener datos locales del agente
    datos_agente = db.despertar_agente(nombre)
    if datos_agente is None:
        logger.warning(f"Consulta de briefing para agente inexistente: {nombre}")
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    
    # Obtener misiones del agente
    misiones = db.listar_misiones_agente(nombre)
    misiones_pendientes = [m for m in misiones if m["estado"] == "pendiente"]
    
    # Intentar obtener un consejo de la API externa
    consejo_externo = None
    fuente_externa = "Advice Slip API"
    
    try:
        logger.info(f"Solicitando consejo externo para briefing de '{nombre}'...")
        response = requests.get(EXTERNAL_API_URL, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            consejo_externo = data.get("slip", {}).get("advice", "Stay focused on your mission.")
            logger.info(f"Consejo externo obtenido para '{nombre}': {consejo_externo[:50]}...")
        else:
            logger.warning(f"API externa respondió con status {response.status_code}. Usando fallback.")
            consejo_externo = "The best advice is to stay committed to your goals."
    
    except requests.Timeout:
        logger.warning(f"Timeout al consultar API externa para '{nombre}'. Usando fallback.")
        consejo_externo = "Even in silence, wisdom can be found within."
    
    except Exception as e:
        logger.error(f"Error al consultar API externa para '{nombre}': {str(e)}. Usando fallback.")
        consejo_externo = "When external sources fail, rely on your inner strength."
    
    # Construir el briefing completo
    briefing = {
        "agente": datos_agente,
        "misiones_totales": len(misiones),
        "misiones_pendientes": len(misiones_pendientes),
        "proximas_misiones": misiones_pendientes[:3],  # Mostrar máximo 3
        "consejo_del_dia": consejo_externo,
        "fuente_externa": fuente_externa,
        "timestamp": db.datetime.datetime.now().isoformat()
    }
    
    logger.info(f"Briefing generado para '{nombre}' con {len(misiones)} misiones registradas")
    return briefing


# ===================================================================
# MENSAJE DE INICIO DEL SERVIDOR
# ===================================================================
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("🏛️  AGENCIA DE AGENTES - SERVIDOR INICIADO")
    logger.info("=" * 60)
    logger.info("Documentación interactiva: http://localhost:8000/docs")
    logger.info("=" * 60)

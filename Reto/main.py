import logging
from fastapi import FastAPI, HTTPException, Path, Depends, Header
import requests

from db import (
    crear_tablas,
    registrar_agente,
    despertar_agente,
    enviar_mensaje,
    leer_mensajes,
    listar_agentes,
    registrar_mision,
    obtener_mision,
    listar_misiones_agente,
    actualizar_estado_mision,
    actualizar_energia_agente,
)
from agente import AgenteAdmin, PseudoAgente
from dto import AgenteRequest, AgenteResponse, MensajeRequest, MisionRequest, BriefingAgent
from config import AGENCIA_API_KEY, EXTERNAL_API_URL, LOG_LEVEL, EXTERNAL_API_TIMEOUT

#Utilice los niveles de loggin warning, error e info porque me permiten hacer seguimiento del sistema durante el funcionamiento real tanto en casos exitosos, errores o en escenarios no ideales pero esperados 
#y asi poder enteneder el comporamiento del sistema
#Me pareción util el formato que incluia fecha y hora de registro de log, nivel de mensaje y el nombre del archivo desde donde se registro el log para mayor trazabilidad
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s [%(levelname)s]: %(name)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p',
    handlers=[
        logging.StreamHandler(), 
    ]
)
logger = logging.getLogger(__name__)

crear_tablas()

app = FastAPI(
    title="Sistema de Agentes",
    description="API para gestionar agentes y mensajes",
)

#Decidi proteger todos los ednpoints tipo POST y libre los tipo GET ya que los endpoints
#tipo POST permiten la modificacion de la base de datos y la información del sistema, lo que puede afectar
#su funcionamiento si la persona no esta autorizada. En cuanto a dejar libre los GET permite a usuarios no registrados identificar si algun agente existente puede ser de utilidad
async def verificar_api_key(x_api_key: str = Header(...)):
    """
    Verifica que el header X-API-KEY coincida con AGENCIA_API_KEY.
    Si no es válido, devuelve 401 Unauthorized.
    """
    if x_api_key != AGENCIA_API_KEY:
        logger.warning("Intento de acceso sin API key válida. Key recibida: %s...", x_api_key[:5])
        raise HTTPException(status_code=401, detail="API key inválida")
    return True

@app.get("/")
def inicio():
    logger.info("Endpoint GET / - Estado del sistema consultado")
    return {"status": "online", "mensaje": "Bienvenido al sistema de agentes"}


@app.get("/agente/{nombre}")
def obtener_agente(nombre: str):
    agente_entity = despertar_agente(nombre)
    if agente_entity is None:
        logger.warning("Intento de acceso a agente inexistente: %s", nombre)
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    agente: PseudoAgente
    if agente_entity["rol"] == "admin":
        agente = AgenteAdmin(agente_entity["nombre"],  agente_entity["energia"])
    else:
        agente = PseudoAgente(agente_entity["nombre"],  agente_entity["energia"])
    logger.info("El Agente %s despertado es del tipo Admin: %s", agente.name, isinstance(agente, AgenteAdmin))
    return AgenteResponse(name=agente.name, tokens=agente.tokens)


@app.get("/agentes/")
def obtener_todos_los_agentes():
    agentes = listar_agentes()
    logger.info("Se listaron %s agentes", len(agentes))
    return agentes

@app.post("/agentes/")
def crear_agente(agente: AgenteRequest, _ = Depends(verificar_api_key)):
    logger.info("POST /agentes/ - Creando nuevo agente: %s (rol: %s)", agente.nombre, agente.rol)
    resultado = registrar_agente(agente.nombre, agente.rol, agente.energia)
    return {"mensaje": resultado}



@app.post("/mensajes/")
def crear_mensaje(mensaje: MensajeRequest, _ = Depends(verificar_api_key)):
    logger.info("POST /mensajes/ - Nuevo mensaje de %s a %s", mensaje.remitente, mensaje.destinatario)
    resultado = enviar_mensaje(mensaje.remitente, mensaje.destinatario, mensaje.contenido)
    return {"mensaje": resultado}

@app.get("/mensajes/{nombre}")
def obtener_mensajes(nombre: str):
    mensajes = leer_mensajes(nombre)
    logger.info("Se leyeron %s mensajes de %s", len(mensajes) if mensajes else 0, nombre)
    return mensajes

@app.post("/misiones/")
def crear_mision(mision: MisionRequest, _ = Depends(verificar_api_key)):
    logger.info("POST /misiones/ - Creando misión '%s' para agente %s", mision.titulo, mision.agente_asignado)
    resultado = registrar_mision(mision.titulo, mision.descripcion, mision.agente_asignado,
                                  mision.tiempo_estimado, mision.energia_requerida)
    if resultado is None:
        logger.warning("Intento de crear misión para agente inexistente: %s", mision.agente_asignado)
        raise HTTPException(status_code=404, detail=f"Agente '{mision.agente_asignado}' no encontrado")
    return {"mensaje": resultado}


@app.get("/misiones/{id}")
def obtener_mision_por_id(mision_id: int):
    mision = obtener_mision(mision_id)
    if mision is None:
        logger.warning("Intento de acceso a misión inexistente: %s", mision_id)
        raise HTTPException(status_code=404, detail=f"Mision '{mision_id}' no encontrada")
    return mision


@app.get("/agente/{nombre}/misiones")
def obtener_misiones_de_agente(nombre: str):
    agente = despertar_agente(nombre)
    if agente is None:
        logger.warning("Intento de acceso a misiones de agente inexistente: %s", nombre)
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    misiones = listar_misiones_agente(nombre)
    logger.info("Se listaron %s misiones de %s", len(misiones) if misiones else 0, nombre)
    return misiones


@app.post("/misiones/{id}/completar")
def completar_mision(mision_id: int = Path(..., alias="id"), _ = Depends(verificar_api_key)):
    logger.info("POST /misiones/%s/completar - Marcando misión como completada", mision_id)
    mision = obtener_mision(mision_id)
    if mision is None:
        logger.warning("Intento de completar misión inexistente: %s", mision_id)
        raise HTTPException(status_code=404, detail=f"Mision '{mision_id}' no encontrada")

    nombre_agente = mision["agente_asignado"]
    agente_entity = despertar_agente(nombre_agente)
    if agente_entity is None:
        logger.error("Intento de completar misión con agente inexistente: %s", nombre_agente)
        raise HTTPException(status_code=404, detail=f"Agente '{nombre_agente}' no encontrado")

    agente: PseudoAgente
    if agente_entity["rol"] == "admin":
        agente = AgenteAdmin(agente_entity["nombre"], agente_entity["energia"])
    else:
        agente = PseudoAgente(agente_entity["nombre"], agente_entity["energia"])

    energia_requerida = mision["energia_requerida"]
    agente.consume_energy(energia_requerida)

    actualizar_energia_agente(agente.name, agente.tokens)
    actualizar_estado_mision(mision_id, "completada")

    return {
        "mensaje": f"Mision '{mision_id}' completada por '{agente.name}'",
        "energia_actual": agente.tokens,
        "tipo_agente": type(agente).__name__,
    }


#Escogi la API externa API SWAPI: The Star Wars API para obtener nombre de planetas de la pelicula.
#En caso que falle se lanzara el error 504 al cliente indicando que falló un dependencia externa y no mi servicio interno 
@app.get("/briefing/{nombre}", response_model=BriefingAgent)
def briefing_agente(nombre: str):
    """
    Endpoint que obtiene información del agente y su planeta de nacimiento desde SWAPI.
    El planet_id se calcula contando las letras del nombre del agente.
    """
    # Calcular planet_id contando las letras del nombre del agente
    planet_id = len(nombre)
    logger.info("GET /briefing/%s - Generando briefing con planeta %s (basado en letras del nombre)", nombre, planet_id)
    
    agente = despertar_agente(nombre)
    if agente is None:
        logger.warning("Intento de briefing de agente inexistente: %s", nombre)
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    
    # Intentar obtener datos del planeta desde SWAPI
    lugar_nacimiento = None
    try:
        swapi_url = f"{EXTERNAL_API_URL}/{planet_id}/"
        response = requests.get(swapi_url, timeout=EXTERNAL_API_TIMEOUT)
        response.raise_for_status()
        planeta = response.json()
        lugar_nacimiento = planeta.get("name", "Desconocido")
        logger.info("Planeta obtenido exitosamente desde SWAPI para briefing de %s", nombre)
    except requests.exceptions.Timeout:
        logger.warning("Timeout al consultar SWAPI (>%ss) para planeta %s", EXTERNAL_API_TIMEOUT, planet_id)
        raise HTTPException(status_code=504, detail="API externa (SWAPI) no respondió en tiempo")
    except requests.exceptions.RequestException as e:
        logger.warning("Error conectando a SWAPI para planeta %s: %s", planet_id, str(e))
        raise HTTPException(status_code=504, detail="No se pudo contactar con API externa (SWAPI)")
    except Exception as e:
        logger.error("Error inesperado al procesar datos de SWAPI: %s", str(e))
        raise HTTPException(status_code=504, detail="Error al procesar datos de SWAPI")

    # Construir respuesta con datos del agente y planeta
    briefing = BriefingAgent(
        nombre=agente["nombre"],
        rol=agente["rol"],
        energia=agente["energia"],
        lugar_nacimiento=lugar_nacimiento
    )
    
    logger.info("Briefing completado para %s desde planeta %s", nombre, lugar_nacimiento)
    return briefing


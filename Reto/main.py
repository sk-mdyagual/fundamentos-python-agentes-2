from fastapi import FastAPI, HTTPException, Depends, Header
import logging
from contextlib import asynccontextmanager
from db import *
from config import API_KEY

"""Este archivo define toda la API. Maneja autenticación, endpoints, logging y conecta la lógica de negocio con la base de datos.
También integra una API externa para la información del agente."""



"""Configuré logging en nivel INFO para ver lo importante sin llenar la consola de mensajes.
   Incluí fecha, nivel y mensaje para poder entender fácilmente qué está pasando en el sistema.
"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
  
    crear_tablas()
    logger.info("Base de datos inicializada")

    yield  

    #Muestra el mensaje al cerrar la app
    logger.info("Cerrando aplicación")


app = FastAPI(
    title="Sistema de Agentes",
    description="API para gestionar agentes y mensajes",
    lifespan=lifespan
)



""" Decidí proteger los endpoints donde se crean o modifican datos para evitar accesos no autorizados.
 Dejé los GET libres porque solo consultan información y no afectan el sistema."""

def verificar_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida")

@app.get("/")
def inicio():
    return {"mensaje": "API de reto activo"}

@app.get("/agente/{nombre}")
def obtener_agente(nombre: str):
    agente = despertar_agente(nombre)
    if agente is None:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    return {
        "nombre": agente.nombre,
        "energia": agente.energia
    }

@app.get("/agentes/")
def obtener_todos_los_agentes():
    return listar_agentes()

@app.post("/agentes/", dependencies=[Depends(verificar_api_key)])
def crear_agente(nombre: str, rol: str, energia: int):
    logger.info(f"Creando agente: {nombre}")
    return {"mensaje": registrar_agente(nombre, rol, energia)}

@app.post("/mensajes/", dependencies=[Depends(verificar_api_key)])
def crear_mensaje(remitente: str, destinatario: str, contenido: str):
    logger.info(f"Mensaje de {remitente} a {destinatario}")
    return {"mensaje": enviar_mensaje(remitente, destinatario, contenido)}

@app.get("/mensajes/{nombre}")
def obtener_mensajes(nombre: str):
    return leer_mensajes(nombre)

@app.post("/misiones/{id}/completar", dependencies=[Depends(verificar_api_key)])
def completar_mision_endpoint(id: int):
    resultado = completar_mision(id)

    if resultado is None:
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    nombre_agente, energia = resultado

    agente = despertar_agente(nombre_agente)

    agente.energia -= energia
    actualizar_energia(nombre_agente, agente.energia)

    logger.info(f"Misión {id} completada por {nombre_agente}")

    return {
        "mensaje": "Misión completada",
        "energia_restante": agente.energia
    }


@app.post("/misiones/", dependencies=[Depends(verificar_api_key)])
def crear_mision_endpoint(titulo: str, descripcion: str, agente: str, energia: int):
    logger.info(f"Creando misión para {agente}")

    if despertar_agente(agente) is None:
        raise HTTPException(status_code=404, detail="Agente no existe")

    return {"mensaje": crear_mision(titulo, descripcion, agente, energia)}


@app.get("/misiones/{id}")
def obtener_mision_endpoint(id: int):
    mision = obtener_mision(id)

    if mision is None:
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    return mision


@app.get("/agente/{nombre}/misiones")
def listar_misiones(nombre: str):
    return listar_misiones_agente(nombre)


import requests
from config import EXTERNAL_API



""" Para el briefing usé una API pública que da consejos, para simular información externa del agente.
    Si la API falla o no responde, devuelvo un mensaje simple para que el sistema no se caiga."""

@app.get("/briefing/{nombre}")
def briefing(nombre: str):
    agente = despertar_agente(nombre)

    if agente is None:
        raise HTTPException(status_code=404, detail="Agente no encontrado")

    try:
        response = requests.get(EXTERNAL_API, timeout=3)
        data = response.json()
        consejo = data["slip"]["advice"]
    except:
        logger.warning("API externa falló")
        consejo = "No hay información externa disponible"

    return {
        "nombre": agente.nombre,
        "energia": agente.energia,
        "consejo": consejo,
        "fuente_externa": "Advice API"
    }
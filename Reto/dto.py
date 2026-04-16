from pydantic import BaseModel

class AgenteRequest(BaseModel):
    nombre: str
    rol: str
    energia: int


class MensajeRequest(BaseModel):
    remitente: str
    destinatario: str
    contenido: str

class AgenteResponse(BaseModel):
    name: str
    tokens: int


class MisionRequest(BaseModel):
    titulo: str
    descripcion: str
    agente_asignado: str
    tiempo_estimado:int
    energia_requerida: int


class BriefingAgent(BaseModel):
    nombre: str
    rol: str
    energia: int
    lugar_nacimiento: str


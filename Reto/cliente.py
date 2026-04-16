
import requests

"""Este script simula un cliente que consume la API. 
Primero valida que el servidor esté activo, 
luego crea un agente, 
le asigna una misión, 
la completa, 
consulta información externa con el briefing y finalmente envía y consulta mensajes entre agentes.”"""


#URL base donde está corriendo el servidor FastAPI
BASE_URL = "http://localhost:8000"

"""API KEY para autenticarse en los endpoints protegidos y debe ser la misma que se configuro en el archivo .env"""
headers = {"X-API-KEY": "12345"}


if __name__ == "__main__":

    print("\n 1. Verificando servidor...")
    r = requests.get(f"{BASE_URL}/")
    print(r.json())

    print("\n 2. Creando agente...")
    agente = {
        "nombre": "Orion",
        "rol": "admin",
        "energia": 100
    }
    r = requests.post(f"{BASE_URL}/agentes/", params=agente, headers=headers)
    print(r.json())

    print("\n 3. Creando misión...")
    mision = {
        "titulo": "Rescate",
        "descripcion": "Salvar datos críticos",
        "agente": "Orion",
        "energia": 20
    }
    r = requests.post(f"{BASE_URL}/misiones/", params=mision, headers=headers)
    print(r.json())

    print("\n 4. Consultando misiones del agente...")
    r = requests.get(f"{BASE_URL}/agente/Orion/misiones")
    print(r.json())

    print("\n 5. Completando misión ID 1...")
    r = requests.post(f"{BASE_URL}/misiones/1/completar", headers=headers)
    print(r.json())

    print("\n 6. Consultando briefing...")
    r = requests.get(f"{BASE_URL}/briefing/Orion")
    print(r.json())

    print("\n 7. Enviando mensaje...")
    mensaje = {
        "remitente": "Orion",
        "destinatario": "Atlas",
        "contenido": "Misión completada con éxito"
    }
    r = requests.post(f"{BASE_URL}/mensajes/", params=mensaje, headers=headers)
    print(r.json())

    print("\n 8. Bandeja de Atlas...")
    r = requests.get(f"{BASE_URL}/mensajes/Atlas")
    print(r.json())
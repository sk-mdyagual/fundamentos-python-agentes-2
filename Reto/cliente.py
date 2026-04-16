"""
cliente.py — Script de demostración del flujo completo de la Agencia

Ejecuta todos los endpoints en secuencia sin intervención manual.
Lee la API key desde la variable de entorno AGENCIA_API_KEY.

Pre-requisitos:
    1. Crear el archivo .env con AGENCIA_API_KEY=tu_clave
    2. Tener el servidor corriendo: uvicorn main:app --reload
    3. Ejecutar: python cliente.py
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

BASE_URL = "http://localhost:8000"
HEADERS = {"X-API-KEY": os.environ.get("AGENCIA_API_KEY", "")}


def imprimir_resultado(titulo: str, respuesta: requests.Response):
    estado = respuesta.status_code
    simbolo = "OK" if estado < 400 else "ERROR"
    print(f"\n[{simbolo}] {titulo} — HTTP {estado}")
    try:
        print(respuesta.json())
    except Exception:
        print(respuesta.text)


def main():
    print("=" * 60)
    print("  DEMOSTRACIÓN: Agencia de Agentes")
    print("=" * 60)

    # 1. Verificar servidor activo
    try:
        r = requests.get(f"{BASE_URL}/", timeout=3)
        imprimir_resultado("GET / (estado del servidor)", r)
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] No se puede conectar al servidor.")
        print("Asegúrate de correr: uvicorn main:app --reload")
        sys.exit(1)

    # 2. Crear agente admin "Atlas"
    r = requests.post(
        f"{BASE_URL}/agentes/",
        json={"nombre": "Atlas", "rol": "admin", "energia": 200},
        headers=HEADERS,
    )
    imprimir_resultado("POST /agentes/ — crear Atlas (admin)", r)

    # 3. Crear agente invitado "Lyra"
    r = requests.post(
        f"{BASE_URL}/agentes/",
        json={"nombre": "Lyra", "rol": "invitado", "energia": 100},
        headers=HEADERS,
    )
    imprimir_resultado("POST /agentes/ — crear Lyra (invitado)", r)

    # 4. Crear agente "Nova"
    r = requests.post(
        f"{BASE_URL}/agentes/",
        json={"nombre": "Nova", "rol": "cientifica", "energia": 150},
        headers=HEADERS,
    )
    imprimir_resultado("POST /agentes/ — crear Nova (cientifica)", r)

    # 5. Listar agentes
    r = requests.get(f"{BASE_URL}/agentes/")
    imprimir_resultado("GET /agentes/ — listar todos", r)

    # 6. Crear misión sin API key (debe dar 401)
    r = requests.post(
        f"{BASE_URL}/misiones/",
        json={"titulo": "Infiltración", "agente_asignado": "Atlas", "energia_requerida": 30},
    )
    imprimir_resultado("POST /misiones/ SIN API key (debe ser 401)", r)

    # 7. Crear misión con API key
    r = requests.post(
        f"{BASE_URL}/misiones/",
        json={
            "titulo": "Infiltración Sector 7",
            "descripcion": "Acceder al archivo secreto del sector 7.",
            "agente_asignado": "Atlas",
            "energia_requerida": 30,
            "prioridad": "alta",
        },
        headers=HEADERS,
    )
    imprimir_resultado("POST /misiones/ — crear misión para Atlas", r)
    mision_id = r.json().get("id") if r.status_code == 201 else None

    # 8. Crear segunda misión para Atlas
    r = requests.post(
        f"{BASE_URL}/misiones/",
        json={
            "titulo": "Reconocimiento Norte",
            "descripcion": "Explorar el perímetro norte.",
            "agente_asignado": "Atlas",
            "energia_requerida": 20,
            "prioridad": "media",
        },
        headers=HEADERS,
    )
    imprimir_resultado("POST /misiones/ — segunda misión para Atlas", r)

    # 9. Crear misión para Nova
    r = requests.post(
        f"{BASE_URL}/misiones/",
        json={
            "titulo": "Análisis de Artefacto",
            "descripcion": "Estudiar el artefacto recuperado.",
            "agente_asignado": "Nova",
            "energia_requerida": 40,
            "prioridad": "baja",
        },
        headers=HEADERS,
    )
    imprimir_resultado("POST /misiones/ — misión para Nova", r)

    # 10. Completar primera misión
    if mision_id:
        r = requests.post(f"{BASE_URL}/misiones/{mision_id}/completar", headers=HEADERS)
        imprimir_resultado(f"POST /misiones/{mision_id}/completar", r)

    # 11. Consultar misiones de Atlas
    r = requests.get(f"{BASE_URL}/agente/Atlas/misiones")
    imprimir_resultado("GET /agente/Atlas/misiones", r)

    # 12. Consultar briefing de Atlas (datos locales + API externa)
    r = requests.get(f"{BASE_URL}/briefing/Atlas")
    imprimir_resultado("GET /briefing/Atlas — briefing completo", r)

    # 13. Enviar mensajes
    r = requests.post(
        f"{BASE_URL}/mensajes/",
        json={"remitente": "Atlas", "destinatario": "Lyra", "contenido": "Misión completada. Perimetro asegurado."},
    )
    imprimir_resultado("POST /mensajes/ — Atlas → Lyra", r)

    r = requests.post(
        f"{BASE_URL}/mensajes/",
        json={"remitente": "Nova", "destinatario": "Lyra", "contenido": "Enviaré el reporte esta tarde."},
    )
    imprimir_resultado("POST /mensajes/ — Nova → Lyra", r)

    r = requests.post(
        f"{BASE_URL}/mensajes/",
        json={"remitente": "Atlas", "destinatario": "Nova", "contenido": "Necesito análisis urgente del artefacto."},
    )
    imprimir_resultado("POST /mensajes/ — Atlas → Nova", r)

    # 14. Leer bandeja de Lyra
    r = requests.get(f"{BASE_URL}/mensajes/Lyra")
    imprimir_resultado("GET /mensajes/Lyra — bandeja de entrada", r)

    # 15. Estado final de Atlas
    r = requests.get(f"{BASE_URL}/agente/Atlas")
    imprimir_resultado("GET /agente/Atlas — estado final (energía descontada)", r)

    print("\n" + "=" * 60)
    print("  DEMOSTRACIÓN COMPLETADA")
    print("  Visita http://localhost:8000/docs para explorar la API")
    print("=" * 60)


if __name__ == "__main__":
    main()

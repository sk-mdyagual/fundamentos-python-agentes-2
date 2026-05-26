"""
cliente.py — Guión de demostración end-to-end para La Agencia de Agentes

Ejecuta sin intervención manual un circuito completo:
  1. Verifica que el servidor está vivo (GET /)
  2. Crea un agente con autenticación (POST /agentes/)
  3. Crea una misión asignada a ese agente (POST /misiones/)
  4. Completa la misión (POST /misiones/{id}/completar)
  5. Consulta el briefing del agente (GET /briefing/{nombre})
  6. Envía un mensaje entre agentes y lee la bandeja

Prerequisito: el servidor debe estar corriendo antes de ejecutar este script.
  uvicorn main:app --reload   (desde la carpeta Reto/)
"""

import sys
import os
import requests
from dotenv import load_dotenv

# Carga el .env para obtener la API key sin hardcodearla aquí
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

BASE_URL = "http://localhost:8000"
API_KEY = os.getenv("AGENCIA_API_KEY", "")
HEADERS_AUTH = {"X-API-KEY": API_KEY}


def separador(n: int, titulo: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  PASO {n}: {titulo}")
    print(f"{'=' * 60}")


def verificar_ok(respuesta: requests.Response, descripcion: str) -> dict:
    """Imprime el resultado y aborta si el código HTTP indica error."""
    if respuesta.status_code not in (200, 201):
        print(f"[ERROR] {descripcion}")
        print(f"        Status: {respuesta.status_code}")
        print(f"        Body  : {respuesta.text}")
        sys.exit(1)
    data = respuesta.json()
    print(f"[OK]    {descripcion}")
    print(f"        Respuesta: {data}")
    return data


# ---------------------------------------------------------------------------
# PASO 1 — Verificar que el servidor está online
# ---------------------------------------------------------------------------
separador(1, "Verificar que el servidor está online")
r = requests.get(f"{BASE_URL}/")
verificar_ok(r, "GET /")


# ---------------------------------------------------------------------------
# PASO 2 — Crear el agente 'Orion' con autenticación
# ---------------------------------------------------------------------------
separador(2, "Crear agente 'Orion'")
r = requests.post(
    f"{BASE_URL}/agentes/",
    json={"nombre": "Orion", "rol": "explorador", "energia": 100},
    headers=HEADERS_AUTH,
)
verificar_ok(r, "POST /agentes/")


# ---------------------------------------------------------------------------
# PASO 3 — Crear misión asignada a 'Orion'
# ---------------------------------------------------------------------------
separador(3, "Crear misión 'Reconocimiento Zona Alpha'")
r = requests.post(
    f"{BASE_URL}/misiones/",
    json={
        "titulo": "Reconocimiento Zona Alpha",
        "descripcion": "Explorar el perímetro norte e informar hallazgos.",
        "agente_asignado": "Orion",
        "estado": "pendiente",
        "energia_requerida": 20,
        "prioridad": "alta",
        "creado_por": "cliente.py",
    },
    headers=HEADERS_AUTH,
)
data_mision = verificar_ok(r, "POST /misiones/")
mision_id = data_mision["id"]


# ---------------------------------------------------------------------------
# PASO 4 — Completar la misión
# ---------------------------------------------------------------------------
separador(4, f"Completar misión id={mision_id}")
r = requests.post(
    f"{BASE_URL}/misiones/{mision_id}/completar",
    headers=HEADERS_AUTH,
)
verificar_ok(r, f"POST /misiones/{mision_id}/completar")


# ---------------------------------------------------------------------------
# PASO 5 — Consultar el briefing del agente
# ---------------------------------------------------------------------------
separador(5, "Briefing del agente 'Orion'")
r = requests.get(f"{BASE_URL}/briefing/Orion")
briefing = verificar_ok(r, "GET /briefing/Orion")
print()
print(f"  Agente       : {briefing['agente']}")
print(f"  Intel misión : {briefing['intel_mision']}")
print(f"  Fuente       : {briefing['fuente_externa']}")


# ---------------------------------------------------------------------------
# PASO 6 — Enviar mensaje entre agentes y leer la bandeja
# ---------------------------------------------------------------------------
separador(6, "Enviar mensaje de 'Orion' a 'Base' y leer bandeja")
r = requests.post(
    f"{BASE_URL}/mensajes/",
    json={
        "remitente": "Orion",
        "destinatario": "Base",
        "contenido": "Zona Alpha despejada. Sin anomalías detectadas. Retorno en 10 minutos.",
    },
    headers=HEADERS_AUTH,
)
verificar_ok(r, "POST /mensajes/")

print()
print("  [Bandeja de 'Base']")
r = requests.get(f"{BASE_URL}/mensajes/Base")
mensajes = r.json()
if not mensajes:
    print("  (sin mensajes)")
for m in mensajes:
    print(f"    De: {m['remitente']} | {m['contenido']} | {m['timestamp']}")


# ---------------------------------------------------------------------------
# RESUMEN FINAL
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("  CIRCUITO COMPLETO EJECUTADO SIN ERRORES")
print("  Todos los pasos del flujo end-to-end pasaron correctamente.")
print("=" * 60)
print()

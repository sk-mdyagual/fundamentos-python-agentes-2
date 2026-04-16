from __future__ import annotations

import requests

from config import settings

BASE_URL = "http://localhost:8000"
HEADERS = {"X-API-KEY": settings.api_key}


def run_demo() -> None:
    print("1) Verificando servidor...")
    r = requests.get(f"{BASE_URL}/", timeout=5)
    print(r.status_code, r.json())

    print("\n2) Creando agente de demo...")
    agente_payload = {"nombre": "Hermes", "rol": "operativo", "energia": 95}
    r = requests.post(f"{BASE_URL}/agentes/", json=agente_payload, headers=HEADERS, timeout=5)
    print(r.status_code, r.json())

    print("\n3) Creando mision para Hermes...")
    mision_payload = {
        "titulo": "Recolectar telemetria",
        "descripcion": "Levantar señales del sector sur.",
        "agente_asignado": "Hermes",
        "estado": "pendiente",
        "energia_requerida": 12,
        "prioridad": "media",
        "creado_por": "cliente_demo",
    }
    r = requests.post(f"{BASE_URL}/misiones/", json=mision_payload, headers=HEADERS, timeout=5)
    print(r.status_code, r.json())
    mision_id = r.json().get("id")

    print("\n4) Completando mision...")
    r = requests.post(
        f"{BASE_URL}/misiones/{mision_id}/completar",
        headers=HEADERS,
        timeout=5,
    )
    print(r.status_code, r.json())

    print("\n5) Consultando briefing de Hermes...")
    r = requests.get(f"{BASE_URL}/briefing/Hermes", timeout=10)
    print(r.status_code)
    print(r.json())

    print("\n6) Enviando mensaje y leyendo bandeja...")
    msg_payload = {
        "remitente": "Hermes",
        "destinatario": "Atlas",
        "contenido": "Mision completada. Envio reporte final.",
    }
    r = requests.post(f"{BASE_URL}/mensajes/", json=msg_payload, headers=HEADERS, timeout=5)
    print(r.status_code, r.json())

    r = requests.get(f"{BASE_URL}/mensajes/Atlas", timeout=5)
    inbox = r.json()
    print(f"Bandeja Atlas ({len(inbox)} mensajes)")
    for msg in inbox[-5:]:
        print(f"- [{msg['timestamp']}] {msg['remitente']}: {msg['contenido']}")


if __name__ == "__main__":
    run_demo()

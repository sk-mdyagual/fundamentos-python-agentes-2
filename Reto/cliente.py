import requests
from config import AGENCIA_API_KEY, SERVER_HOST

TIMEOUT = 10


# Crear una sesión con headers por defecto
session = requests.Session()
session.headers.update({
    "X-API-KEY": AGENCIA_API_KEY
})

def request_json(method: str, endpoint: str, payload: dict | None = None) -> tuple[int, dict | list]:
    response = session.request(method, f"{SERVER_HOST}{endpoint}", json=payload, timeout=TIMEOUT)
    try:
        parsed_body = response.json()
    except ValueError:
        parsed_body = {"raw": response.text}
    return response.status_code, parsed_body


def print_step(title: str) -> None:
    print(f"\n=== {title} ===")


if __name__ == "__main__":
    agente_principal = {"nombre": "Orion", "rol": "estratega", "energia": 120}
    agente_destino = {"nombre": "Atlas", "rol": "operativo", "energia": 100}

    print_step("Paso 1 - Validar servicio")
    status, body = request_json("GET", "/")
    print(f"GET / -> {status}")
    print(body)

    if status != 200:
        raise SystemExit("No se pudo validar que el servidor este activo.")

    print_step("Paso 2 - Crear agentes")
    status, body = request_json("POST", "/agentes/", agente_principal)
    print(f"POST /agentes/ (Orion) -> {status}")
    if status == 404:
        raise SystemExit("No se pudo crear la mision.")
    else:
        print(body)

    status, body = request_json("POST", "/agentes/", agente_destino)
    print(f"POST /agentes/ (Atlas) -> {status}")
    print(body)

    print_step("Paso 3 - Crear mision")
    mision_payload = {
        "titulo": "Infiltrar Nodo Delta",
        "descripcion": "Recolectar inteligencia de comunicaciones.",
        "agente_asignado": agente_principal["nombre"],
        "tiempo_estimado": 3,
        "energia_requerida": 25,
    }
    status, body = request_json("POST", "/misiones/", mision_payload)
    print(f"POST /misiones/ -> {status}")
    print(body)

    if status != 200:
        raise SystemExit("No se pudo crear la mision.")

    status, body = request_json("GET", f"/agente/{agente_principal['nombre']}/misiones")
    print(f"GET /agente/{agente_principal['nombre']}/misiones -> {status}")
    if status != 200 or not isinstance(body, list) or len(body) == 0:
        raise SystemExit("No se pudo recuperar la mision para completar.")

    mision_id = body[-1]["id"]
    print(f"Mision seleccionada para completar: {mision_id}")

 
    print_step("Paso 4 - Completar mision")
    status, body = request_json("POST", f"/misiones/{mision_id}/completar")
    print(f"POST /misiones/{mision_id}/completar -> {status}")
    print(body)

    print_step("Paso 5 - Briefing")
    status, body = request_json("GET", f"/briefing/{agente_principal['nombre']}")
    print(f"GET /briefing/{agente_principal['nombre']} -> {status}")
    print(body)


    print_step("Paso 6 - Mensajeria")
    mensaje_payload = {
        "remitente": agente_principal["nombre"],
        "destinatario": agente_destino["nombre"],
        "contenido": "Mision completada. Solicito extraccion segura.",
    }
    status, body = request_json("POST", "/mensajes/", mensaje_payload)
    print(f"POST /mensajes/ -> {status}")
    print(body)

    status, body = request_json("GET", f"/mensajes/{agente_destino['nombre']}")
    print(f"GET /mensajes/{agente_destino['nombre']} -> {status}")
    if isinstance(body, list):
        print(f"Mensajes recibidos por {agente_destino['nombre']}: {len(body)}")
        for msg in body:
            print(f"[{msg['timestamp']}] {msg['remitente']} -> {msg['contenido']}")
    else:
        print(body)


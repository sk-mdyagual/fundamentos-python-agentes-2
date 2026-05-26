## Creado por: Sergio Jaramillo (SergiJaramilloL)
# -----------------------------------------------------------#
# cliente.py — Guion de demostración end-to-end
# -----------------------------------------------------------#
# Este script consume la API de la Agencia por HTTP usando
# la librería `requests`. Ejecuta el flujo completo sin
# intervención manual y verifica que el circuito funcione.
#
# Requisitos:
#   1. El servidor debe estar corriendo en otra terminal:
#         uvicorn main:app --reload
#   2. El archivo .env debe tener AGENCIA_API_KEY configurada.
#   3. Ejecutar desde la carpeta S6_reto/:
#         python cliente.py
# -----------------------------------------------------------#

import requests
import sys

BASE_URL = "http://localhost:8000"

# Se lee la API key desde el archivo .env a través de config.py
# para no hardcodear la clave en este script.
from config import AGENCIA_API_KEY

# El header de autenticación se construye una sola vez y se reutiliza
# en todas las peticiones protegidas.
HEADERS_AUTH = {"X-API-KEY": AGENCIA_API_KEY}


def separador(titulo: str) -> None:
    """Imprime un separador visual para facilitar la lectura del guion."""
    print(f"\n{'=' * 55}")
    print(f"  {titulo}")
    print('=' * 55)


def verificar_ok(respuesta: requests.Response, contexto: str) -> dict:
    """Verifica que una respuesta HTTP sea exitosa, imprime el resultado y lo retorna."""
    print(f"  [{respuesta.status_code}] {contexto}")
    if respuesta.status_code not in (200, 201):
        print(f"  [Error] Respuesta inesperada: {respuesta.text}")
        sys.exit(1)
    datos = respuesta.json()
    print(f"  Respuesta: {datos}")
    return datos


# =====================
# PASO 1: Verificar que el servidor está vivo
# =====================
separador("PASO 1: Verificar servidor")
r = requests.get(f"{BASE_URL}/")
verificar_ok(r, "GET /")


# =====================
# PASO 2: Crear agentes con autenticación
# =====================
separador("PASO 2: Crear agentes (POST /agentes/)")

agentes_semilla = [
    {"nombre": "Atlas",  "rol": "explorador", "energia": 120},
    {"nombre": "Nova",   "rol": "cientifica",  "energia": 150},
    {"nombre": "Omega",  "rol": "admin",        "energia": 200},
]

for datos in agentes_semilla:
    r = requests.post(f"{BASE_URL}/agentes/", json=datos, headers=HEADERS_AUTH)
    # Si el agente ya existe (409) lo ignoramos para que el script sea idempotente.
    if r.status_code == 409:
        print(f"  [409] Agente '{datos['nombre']}' ya existía — continuando.")
    else:
        verificar_ok(r, f"POST /agentes/ — {datos['nombre']}")


# =====================
# PASO 3: Verificar rechazo de API key inválida (401)
# =====================
separador("PASO 3: Verificar 401 con key inválida")
r = requests.post(
    f"{BASE_URL}/agentes/",
    json={"nombre": "Fantasma", "rol": "espía", "energia": 50},
    headers={"X-API-KEY": "clave-incorrecta"},
)
print(f"  [{r.status_code}] POST /agentes/ sin key válida → esperado 401")
assert r.status_code == 401, f"Se esperaba 401, se recibió {r.status_code}"
print(f"  Respuesta: {r.json()}")
print("  [OK] La protección con API key funciona correctamente.")


# =====================
# PASO 4: Crear misiones con autenticación
# =====================
separador("PASO 4: Crear misiones (POST /misiones/)")

misiones_semilla = [
    {
        "titulo": "Exploración Cueva Norte",
        "descripcion": "Reconocer el terreno y documentar hallazgos.",
        "agente_asignado": "Atlas",
        "estado": "pendiente",
        "energia_requerida": 20,
        "prioridad": 3,
        "recompensa": 10,
    },
    {
        "titulo": "Análisis de muestras",
        "descripcion": "Procesar las muestras del sector 7 en laboratorio.",
        "agente_asignado": "Nova",
        "estado": "en_curso",
        "energia_requerida": 30,
        "prioridad": 5,
        "recompensa": 15,
    },
    {
        "titulo": "Auditoría de sistemas",
        "descripcion": "Revisar logs de acceso del último ciclo operativo.",
        "agente_asignado": "Omega",
        "estado": "pendiente",
        "energia_requerida": 40,
        "prioridad": 4,
        "recompensa": 20,
    },
]

ids_misiones = []
for mision in misiones_semilla:
    r = requests.post(f"{BASE_URL}/misiones/", json=mision, headers=HEADERS_AUTH)
    datos = verificar_ok(r, f"POST /misiones/ — {mision['titulo']}")
    ids_misiones.append(datos["id"])

id_mision_atlas = ids_misiones[0]
id_mision_omega = ids_misiones[2]


# =====================
# PASO 5: Completar una misión con autenticación
# =====================
separador(f"PASO 5: Completar misión id={id_mision_atlas} (Atlas)")
r = requests.post(f"{BASE_URL}/misiones/{id_mision_atlas}/completar", headers=HEADERS_AUTH)
verificar_ok(r, f"POST /misiones/{id_mision_atlas}/completar")

# Completar la misión de Omega (admin): debe pagar la mitad de la energía.
separador(f"PASO 6: Completar misión id={id_mision_omega} (Omega — AgenteAdmin)")
r = requests.post(f"{BASE_URL}/misiones/{id_mision_omega}/completar", headers=HEADERS_AUTH)
datos_completar = verificar_ok(r, f"POST /misiones/{id_mision_omega}/completar")
print(f"  Tipo de agente reconstruido: {datos_completar.get('tipo_agente')}")


# =====================
# PASO 7: Consultar el briefing del agente
# =====================
separador("PASO 7: Briefing de Atlas (GET /briefing/Atlas)")
r = requests.get(f"{BASE_URL}/briefing/Atlas")
datos_briefing = verificar_ok(r, "GET /briefing/Atlas")
print(f"  Instrucción del día: {datos_briefing.get('instruccion_del_dia')}")
print(f"  Fuente externa: {datos_briefing.get('fuente_externa')}")


# =====================
# PASO 8: Mensajes entre agentes + lectura de bandeja
# =====================
separador("PASO 8: Enviar mensajes y leer bandeja")

mensajes_semilla = [
    {"remitente": "Atlas",  "destinatario": "Nova",  "contenido": "Encontré estructuras extrañas en la cueva norte."},
    {"remitente": "Nova",   "destinatario": "Atlas", "contenido": "Enviaré un drone de análisis mañana."},
    {"remitente": "Omega",  "destinatario": "Nova",  "contenido": "Prioridad máxima en el análisis de muestras."},
    {"remitente": "Atlas",  "destinatario": "Omega", "contenido": "Misión completada. Esperando nuevas órdenes."},
    {"remitente": "Nova",   "destinatario": "Omega", "contenido": "Resultados preliminares listos para revisión."},
]

for msg in mensajes_semilla:
    r = requests.post(f"{BASE_URL}/mensajes/", json=msg)
    print(f"  [{r.status_code}] {msg['remitente']} → {msg['destinatario']}: {msg['contenido'][:40]}...")

# Leer bandeja de Nova.
r = requests.get(f"{BASE_URL}/mensajes/Nova")
mensajes_nova = r.json()
print(f"\n  Bandeja de Nova ({len(mensajes_nova)} mensajes):")
for msg in mensajes_nova:
    print(f"    [{msg['timestamp']}] {msg['remitente']}: {msg['contenido']}")


# =====================
# RESUMEN FINAL
# =====================
separador("RESUMEN FINAL")
r = requests.get(f"{BASE_URL}/agentes/")
agentes = r.json()
print("  Agentes registrados:")
for ag in agentes:
    print(f"    {ag['nombre']} | rol: {ag['rol']} | energía: {ag['energia']}")

r = requests.get(f"{BASE_URL}/agente/Atlas/misiones")
print(f"\n  Misiones de Atlas: {len(r.json())} total")

print("\n[Sistema] Guion de demostración completado exitosamente.")

## Creado por: Sergio Jaramillo (SergiJaramilloL)

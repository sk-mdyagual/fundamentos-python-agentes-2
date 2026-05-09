# config.py — Carga de variables de entorno para Cyber-Mercs
# Los secretos viven en el archivo .env (que NO se sube a git).
# Este módulo los lee con python-dotenv y los expone como constantes.

import os
from dotenv import load_dotenv

load_dotenv()

# CORP_API_KEY: SIN fallback — si falta, el servidor debe fallar ruidoso.
# Razón: un fallback hardcodeado es la misma key que se usaría en .env,
# lo que convierte el "secreto" en público si alguien olvida configurar.
CORP_API_KEY = os.environ.get("CORP_API_KEY")
if not CORP_API_KEY:
    raise RuntimeError(
        "CORP_API_KEY no está configurada. "
        "Copia .env.example como .env y define la variable antes de arrancar."
    )

# CoinGecko reemplaza a CoinDesk (deprecada en 2024).
# El endpoint público no requiere autenticación.
CRYPTO_API_URL = os.getenv(
    "CRYPTO_API_URL",
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
)

DB_PATH = os.getenv("DB_PATH", "mercenarios.db")
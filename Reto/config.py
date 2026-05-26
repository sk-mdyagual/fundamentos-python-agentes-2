"""
config.py — Carga de variables de entorno para La Agencia de Agentes

Lee el archivo .env usando python-dotenv y expone las variables
necesarias para la aplicación. Si no existe el .env, las variables
pueden venir del entorno del sistema operativo (útil en producción).

Variables requeridas (definir en .env):
  AGENCIA_API_KEY   → llave maestra para endpoints protegidos
  EXTERNAL_API_URL  → URL de la API pública externa para el briefing
"""

import os
from dotenv import load_dotenv

# Carga el archivo .env desde la misma carpeta que este módulo.
# Si el archivo no existe, load_dotenv no lanza error: simplemente no hace nada.
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

AGENCIA_API_KEY: str = os.getenv("AGENCIA_API_KEY", "")
EXTERNAL_API_URL: str = os.getenv(
    "EXTERNAL_API_URL",
    "https://api.adviceslip.com/advice",
)

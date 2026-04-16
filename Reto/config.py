"""
config.py — Carga de variables de entorno para la Agencia

Lee el archivo .env (NO versionado) con python-dotenv y expone
las variables como constantes importables desde cualquier módulo.

El archivo .env.example (sí versionado) documenta las variables
disponibles sin revelar valores reales.
"""

from dotenv import load_dotenv
import os

# Carga las variables del archivo .env ubicado en la misma carpeta
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

# Clave de autenticación para los endpoints protegidos de la Agencia
API_KEY: str = os.environ.get("AGENCIA_API_KEY", "")

# URL base de la API externa para el endpoint /briefing
EXTERNAL_API_URL: str = os.environ.get(
    "EXTERNAL_API_URL", "https://api.adviceslip.com/advice"
)

"""
config.py — Gestión de variables de entorno

Este módulo carga las variables de configuración desde el archivo .env
y las expone al resto de la aplicación de forma segura.

NUNCA almacenes secretos en el código fuente. Usa variables de entorno.
"""

import os
from dotenv import load_dotenv

# Carga las variables del archivo .env (si existe)
load_dotenv()

# Variables de configuración de la Agencia
AGENCIA_API_KEY = os.getenv("AGENCIA_API_KEY", "clave_por_defecto_insegura")
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "https://api.adviceslip.com/advice")
DB_PATH = os.getenv("DB_PATH", "agentes.db")

# Validación básica
if AGENCIA_API_KEY == "clave_por_defecto_insegura":
    print("[ADVERTENCIA] AGENCIA_API_KEY no configurada. Usando valor por defecto inseguro.")

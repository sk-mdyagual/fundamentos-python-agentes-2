# Reto de Consolidación - Agencia del Olimpo
# Doris Mosquera Lozano - doris.mosquera@sofka.com.co
# DMosqueraLSofka

# config.py — Carga de variables de entorno
# Los secretos viven en el archivo .env (que NO se sube a git).
# Este módulo los lee con python-dotenv y los expone como constantes.

import os
from dotenv import load_dotenv

# Carga las variables del archivo .env al entorno del sistema operativo
load_dotenv()

# os.getenv("CLAVE", "valor_por_defecto") busca la variable.
# Si no la encuentra, usa el segundo argumento como fallback.
AGENCIA_API_KEY = os.getenv("AGENCIA_API_KEY", "olympus-key-2026")
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "https://uselessfacts.jsph.pl/api/v2/facts/random")

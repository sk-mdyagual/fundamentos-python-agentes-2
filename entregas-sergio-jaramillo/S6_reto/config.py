## Creado por: Sergio Jaramillo (SergiJaramilloL)
# -----------------------------------------------------------#
# config.py — Carga de variables de entorno
# -----------------------------------------------------------#
# Las claves secretas y URLs externas NO deben estar hardcodeadas
# en el código fuente. Si las subes a GitHub, cualquiera las copia.
# Este módulo usa python-dotenv para leer el archivo `.env` local
# y expone las variables como constantes importables.
# El archivo `.env` está en .gitignore — nunca se versiona.
# El archivo `.env.example` sí se versiona: muestra qué variables
# necesita el proyecto sin revelar los valores reales.
# -----------------------------------------------------------#

import os
from dotenv import load_dotenv

# load_dotenv() busca el archivo `.env` en el directorio actual y carga
# sus variables al entorno del proceso. Si ya existen en el entorno del
# sistema, no las sobreescribe (útil en producción con variables de CI/CD).
load_dotenv()

# Clave secreta de la Agencia. Se usa para proteger los endpoints de escritura.
# Si no existe en el .env, usa un valor por defecto solo para desarrollo local.
AGENCIA_API_KEY: str = os.getenv("AGENCIA_API_KEY", "dev-key-insegura")

# URL de la API externa que alimenta el endpoint /briefing/{nombre}.
# Usando adviceslip.com: retorna un consejo aleatorio como JSON sin autenticación.
EXTERNAL_API_URL: str = os.getenv("EXTERNAL_API_URL", "https://api.adviceslip.com/advice")

## Creado por: Sergio Jaramillo (SergiJaramilloL)

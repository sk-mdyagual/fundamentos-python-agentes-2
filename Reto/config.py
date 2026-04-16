import os
from dotenv import load_dotenv

load_dotenv()

AGENCIA_API_KEY = os.getenv("AGENCIA_API_KEY", "dev_key_default")
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "https://jsonplaceholder.typicode.com")
SERVER_HOST = os.getenv("SERVER_HOST", "http://localhost:8000")
EXTERNAL_API_TIMEOUT = int(os.getenv("EXTERNAL_API_TIMEOUT", "5"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
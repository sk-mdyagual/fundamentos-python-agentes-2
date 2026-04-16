import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AGENCIA_API_KEY")
EXTERNAL_API = os.getenv("EXTERNAL_API_URL")
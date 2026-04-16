from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

# Cargo las settings desde variables de entorno
@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("AGENCIA_API_KEY", "dev-key")
    external_api_url: str = os.getenv("EXTERNAL_API_URL", "https://catfact.ninja/fact")
    external_api_timeout: float = float(os.getenv("EXTERNAL_API_TIMEOUT", "5"))


settings = Settings()

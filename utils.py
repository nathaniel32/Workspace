import os
from dotenv import load_dotenv
from typing import List

# Load .env file
load_dotenv()

class Config:
    # Database
    DB_ADDRESS: str = os.getenv("DB_ADDRESS")
    DB_DATABASE: str = os.getenv("DB_DATABASE")
    DB_USERNAME: str = os.getenv("DB_USERNAME")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    # Service
    SERVICE_HOST: str = os.getenv("SERVICE_HOST", "localhost")
    SERVICE_PORT: int = int(os.getenv("SERVICE_PORT", 8000))

    # App settings
    APP_NAME: str = os.getenv("APP_NAME")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXP: int = int(os.getenv("ACCESS_TOKEN_EXP"))

    # CORS origins
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        origins = os.getenv("ORIGINS", "")
        return [origin.strip() for origin in origins.split(",") if origin.strip()]

config = Config()
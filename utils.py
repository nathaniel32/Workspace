import os
from dotenv import load_dotenv
from typing import List

# Load .env file
load_dotenv()

""" class Config:
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

    ORDER_FILE_XLSX: str = os.getenv("ORDER_FILE_XLSX")
    ORDER_FILE_PDF: str = os.getenv("ORDER_FILE_PDF")
    ORDER_FILE_TITLE: str = os.getenv("ORDER_FILE_TITLE")

    # CORS origins
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        origins = os.getenv("ORIGINS", "")
        return [origin.strip() for origin in origins.split(",") if origin.strip()]

config = Config() """

class Config:
    def __init__(self):
        for key, value in os.environ.items():
            setattr(self, key, value)

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        origins = getattr(self, "ORIGINS", "")
        return [origin.strip() for origin in origins.split(",") if origin.strip()]

config = Config()
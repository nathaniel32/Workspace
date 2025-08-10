import os
from dotenv import load_dotenv
from typing import List

# Load .env file
load_dotenv()

class Config:
    def __init__(self):
        for key, value in os.environ.items():
            setattr(self, key, value)

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        origins = getattr(self, "ORIGINS", "")
        return [origin.strip() for origin in origins.split(",") if origin.strip()]

config = Config()
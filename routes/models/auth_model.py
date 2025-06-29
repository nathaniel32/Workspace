from pydantic import BaseModel

class ValidationBaseModel(BaseModel):
    ip: str
    aud: str
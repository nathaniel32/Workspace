from pydantic import BaseModel

class Validation(BaseModel):
    ip: str
    aud: str
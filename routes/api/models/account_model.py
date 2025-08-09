from pydantic import BaseModel
import database.models

class Validation(BaseModel):
    ip: str
    aud: str

class AccountCreate(BaseModel):
    u_role: database.models.UserRole

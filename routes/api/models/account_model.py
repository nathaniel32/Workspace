from pydantic import BaseModel
import database.models
from typing import Optional

class UserOut(BaseModel):
    u_id: str
    u_name: Optional[str] = None
    u_email: Optional[str] = None
    u_code: Optional[str] = None
    u_role: database.models.UserRole
    u_status: database.models.UserStatus
    u_time: int

    model_config = {
        "from_attributes": True,
    }

class Validation(BaseModel):
    ip: str
    aud: str

class AccountCreate(BaseModel):
    u_role: database.models.UserRole

class AccountUpdate(BaseModel):
    u_id: str
    u_name: Optional[str] = None
    u_email: Optional[str] = None
    u_role: database.models.UserRole
    u_status: database.models.UserStatus

class AccountDelete(BaseModel):
    u_id: str
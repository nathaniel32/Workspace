from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class OutputCreate(BaseModel):
    o_description: str

class OrderOut(BaseModel):
    o_id: str
    u_id: int
    o_description: str
    o_time: int

    model_config = {
        "from_attributes": True,
    }
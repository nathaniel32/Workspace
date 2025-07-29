from pydantic import BaseModel
from typing import List

class OrderCreate(BaseModel):
    o_description: str

class OrderArtikelCreate(BaseModel):
    o_id: str # order
    power: str # power
    oa_description: str
    s_ids: List[str] # specs

class OrderOut(BaseModel):
    o_id: str
    u_id: str
    o_description: str
    o_time: int

    model_config = {
        "from_attributes": True,
    }
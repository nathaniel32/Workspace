from pydantic import BaseModel
from typing import List
from decimal import Decimal

class OrderCreate(BaseModel):
    o_description: str

class OrderArticleCreate(BaseModel):
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

class OrderSpecSchema(BaseModel):
    s_id: str
    p_id: str
    os_price: Decimal

    model_config = {
        "from_attributes": True,
    }

class OrderArticleOut(BaseModel):
    oa_id: str
    o_id: str
    p_id: str
    oa_power: int
    oa_description: str | None = None
    specs: List[OrderSpecSchema]

    model_config = {
        "from_attributes": True,
    }
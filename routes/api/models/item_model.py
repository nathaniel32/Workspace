from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class PowerOut(BaseModel):
    p_id: str
    p_power: int

    model_config = {
        "from_attributes": True,
    }

class PowerCreate(BaseModel):
    p_power: int

class PowerUpdate(BaseModel):
    p_id: str
    p_power: int

class PowerDelete(BaseModel):
    p_id: str


class SpecOut(BaseModel):
    s_id: str
    s_spec: str

    model_config = {
        "from_attributes": True,
    }

class SpecCreate(BaseModel):
    s_spec: str

class SpecUpdate(BaseModel):
    s_id: str
    s_spec: str

class SpecDelete(BaseModel):
    s_id: str


class PriceListOut(BaseModel):
    p_id: str
    s_id: str
    description: Optional[str] = None
    price: Decimal
    power: int
    spec: str

    model_config = {
        "from_attributes": True,
    }

class PriceChange(BaseModel):
    p_id: str
    s_id: str
    pl_description: str
    pl_price: Decimal

class OrderOut(BaseModel):
    o_id: str
    u_id: int
    o_description: str
    o_time: int

    model_config = {
        "from_attributes": True,
    }
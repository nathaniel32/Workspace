from pydantic import BaseModel
from decimal import Decimal

class PowerCreate(BaseModel):
    p_power: int

class PowerUpdate(BaseModel):
    p_id: str
    p_power: int

class PowerDelete(BaseModel):
    p_id: str


class SpecCreate(BaseModel):
    s_spec: str

class SpecUpdate(BaseModel):
    s_id: str
    s_spec: str

class SpecDelete(BaseModel):
    s_id: str

class PriceChange(BaseModel):
    p_id: str
    s_id: str
    pl_price: Decimal
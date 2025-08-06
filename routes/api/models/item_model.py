from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class PowerOut(BaseModel):
    p_id: str
    p_power: int
    p_unit: int

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
    s_corrective: bool

    model_config = {
        "from_attributes": True,
    }

class SpecCreate(BaseModel):
    s_spec: str
    s_corrective: bool

class SpecUpdate(BaseModel):
    s_id: str
    s_spec: str
    s_corrective: bool

class SpecDelete(BaseModel):
    s_id: str


class PriceListOut(BaseModel):
    p_id: str
    s_id: str
    pl_description: Optional[str] = None
    pl_price: Decimal

    model_config = {
        "from_attributes": True,
    }

class PriceChange(BaseModel):
    p_id: str
    s_id: str
    pl_description: Optional[str] = None
    pl_price: Decimal

class PowerChange(BaseModel):
    p_id: str
    p_power: int
    p_unit: int
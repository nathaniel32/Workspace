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


class ItemOut(BaseModel):
    i_id: str
    i_item: str
    i_corrective: bool

    model_config = {
        "from_attributes": True,
    }

class ItemCreate(BaseModel):
    i_item: str
    i_corrective: bool

class ItemUpdate(BaseModel):
    i_id: str
    i_item: str
    i_corrective: bool

class ItemDelete(BaseModel):
    i_id: str


class PriceListOut(BaseModel):
    p_id: str
    i_id: str
    pl_description: Optional[str] = None
    pl_price: Decimal

    model_config = {
        "from_attributes": True,
    }

class PriceChange(BaseModel):
    p_id: str
    i_id: str
    pl_description: Optional[str] = None
    pl_price: Decimal

class PowerChange(BaseModel):
    p_id: str
    p_power: int
    p_unit: int
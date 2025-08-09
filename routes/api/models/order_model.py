from pydantic import BaseModel
from typing import List
from decimal import Decimal
from typing import Optional
from database.models import OrderStatus

class OrderCreate(BaseModel):
    o_name: Optional[str] = None

class OrderArticleCreate(BaseModel):
    o_id: str # order
    power: str # power
    oa_name: str
    i_id_list: List[str] # items

class OrderOut(BaseModel):
    o_id: str
    u_id: str
    o_name: Optional[str] = None
    o_time: int
    o_status: OrderStatus

    model_config = {
        "from_attributes": True,
    }

class PriceListOut(BaseModel):
    p_id: str
    i_id: str
    pl_price: Decimal
    pl_description: Optional[str] = None

    model_config = {
        "from_attributes": True,
    }

class OrderItemSchema(BaseModel):
    i_id: str
    p_id: str
    os_price: Decimal
    price_list: Optional[PriceListOut]

    model_config = {
        "from_attributes": True,
    }

class OrderArticleOut(BaseModel):
    oa_id: str
    o_id: str
    p_id: str
    oa_power: int
    oa_name: str | None = None
    items: List[OrderItemSchema]

    model_config = {
        "from_attributes": True,
    }

class OrderArticleDelete(BaseModel):
    oa_id: str

class OrderDelete(BaseModel):
    o_id: str

class OrderChange(BaseModel):
    o_id: str
    o_name: Optional[str] = None
    o_status: str
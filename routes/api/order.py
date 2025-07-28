from fastapi import APIRouter
import database.connection
import database.models
from typing import List
from fastapi import HTTPException, status, APIRouter
from routes.api.models.item_model import OrderOut
import routes.api.utils

class OrderAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/api/order", tags=["Order"])
        self.router.add_api_route("/order", self.get_all_order, methods=["GET"])

    def get_all_order(self, db: database.connection.db_dependency) -> List[OrderOut]:
        try:
            orders = db.query(database.models.TOrder).all()
            return [OrderOut.model_validate(o) for o in orders]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
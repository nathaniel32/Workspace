from fastapi import APIRouter, Request
import database.connection
import database.models
from typing import List
from fastapi import HTTPException, status, APIRouter
from routes.api.models.order_model import OrderOut, OutputCreate
import routes.api.utils

class OrderAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/api/order", tags=["Order"])
        self.router.add_api_route("/order", self.get_all_order, methods=["GET"])
        self.router.add_api_route("/order", self.insert_order, methods=["POST"])

    def get_all_order(self, db: database.connection.db_dependency) -> List[OrderOut]:
        try:
            orders = db.query(database.models.TOrder).all()
            return [OrderOut.model_validate(o) for o in orders]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    def insert_order(self, request: Request, output: OutputCreate, db: database.connection.db_dependency):
        print(request.cookies['access_token'])
        try:
            return 1
            """ new_order = database.models.TOrder(
                o_id=routes.api.utils.generate_id(),
                u_id=None,
                o_description=output.o_description
            )
            db.add(new_order)
            db.commit()
            db.refresh(new_order)
            return {"message": "Order berhasil ditambahkan", "o_id": new_order.o_id} """
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
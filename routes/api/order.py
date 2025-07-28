from fastapi import APIRouter, Request
import database.connection
import database.models
from typing import List
from fastapi import HTTPException, status, APIRouter
from routes.api.models.order_model import OrderOut, OutputCreate
import routes.api.utils
import logging
import traceback
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

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
        try:
            access_token = request.cookies.get("access_token")
            user_ip = request.client.host
            aud = request.headers.get("user-agent")

            if not access_token:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token.")

            message, payload = routes.api.utils.validate_token(access_token, user_ip, aud)
            user_id = payload.get("id")

            if not user_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token payload.")

            new_order = database.models.TOrder(
                o_id=routes.api.utils.generate_id(),
                u_id=user_id,
                o_description=output.o_description
            )

            db.add(new_order)
            db.commit()
            db.refresh(new_order)

            return {"message": "Order berhasil ditambahkan", "o_id": new_order.o_id}

        except SQLAlchemyError as db_err:
            db.rollback()
            logger.error("Database error: %s", traceback.format_exc())
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.")

        except HTTPException:
            raise # buat 401

        except Exception as e:
            logger.error("Unhandled exception: %s", traceback.format_exc())
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")
from fastapi import APIRouter, Request
import database.connection
import database.models
from typing import List
from fastapi import HTTPException, status, APIRouter
from routes.api.models.order_model import OrderOut, OrderCreate, OrderArticleCreate, OrderArticleOut, OrderSpecSchema, PriceListOut, OrderArticleDelete, OrderChange
import routes.api.utils
import logging
import traceback
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlalchemy import text

logger = logging.getLogger(__name__)

class OrderAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/api/order", tags=["Order"])
        self.router.add_api_route("/status", self.get_enum_order_status, methods=["GET"])
        self.router.add_api_route("/order", self.get_all_order, methods=["GET"])
        self.router.add_api_route("/order", self.insert_order, methods=["POST"])
        self.router.add_api_route("/order", self.change_order, methods=["PUT"])
        self.router.add_api_route("/order-article", self.insert_order_article, methods=["POST"])
        self.router.add_api_route("/order-article/{o_id}", self.get_order_articles_with_specs, methods=["GET"])
        self.router.add_api_route("/order-article", self.delete_order_article, methods=["DELETE"])

    def get_enum_order_status(self, db: database.connection.db_dependency):
        try:
            query = "SELECT e.enumlabel FROM pg_type t JOIN pg_enum e ON t.oid = e.enumtypid WHERE t.typname = 'orderstatus';"
            result = db.execute(text(query))
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def get_all_order(self, db: database.connection.db_dependency) -> List[OrderOut]:
        try:
            orders = db.query(database.models.TOrder).all()
            return [OrderOut.model_validate(o) for o in orders]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def insert_order(self, request: Request, input: OrderCreate, db: database.connection.db_dependency):
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
                o_description=input.o_description
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
        
    def get_order_articles_with_specs(self, o_id: str, db: database.connection.db_dependency) -> List[OrderArticleOut]:
        try:
            articles = db.query(database.models.TOrderArticle).options(
                joinedload(database.models.TOrderArticle.order_specs)  # load specs
                    .joinedload(database.models.TOrderSpec.pricelist)
            ).filter(
                database.models.TOrderArticle.o_id == o_id
            ).all()

            #if not articles:
            #    raise HTTPException(status_code=404, detail="Order articles not found.")

            """ return [
                {
                    "oa_id": article.oa_id,
                    "o_id": article.o_id,
                    "p_id": article.p_id,
                    "oa_power": article.oa_power,
                    "oa_description": article.oa_description,
                    "specs": article.order_specs  # OrderSpecSchema
                }
                for article in articles
            ] """
            
            return [
                OrderArticleOut(
                    oa_id=article.oa_id,
                    o_id=article.o_id,
                    p_id=article.p_id,
                    oa_power=article.oa_power,
                    oa_description=article.oa_description,
                    specs=[
                        OrderSpecSchema(
                            s_id=spec.s_id,
                            p_id=spec.p_id,
                            os_price=spec.os_price,
                            price_list=PriceListOut.model_validate(spec.pricelist) if spec.pricelist else None
                        )
                        for spec in article.order_specs
                    ]
                )
                for article in articles
            ]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def delete_order_article(self, input: OrderArticleDelete, db: database.connection.db_dependency):
        try:
            db_spec = db.query(database.models.TOrderArticle).filter_by(oa_id=input.oa_id).first()
            if not db_spec:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spec tidak ditemukan")
            db.delete(db_spec)
            db.commit()
            return {"message": "Order Article berhasil dihapus"}
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def insert_order_article(self, request: Request, input: OrderArticleCreate, db: database.connection.db_dependency):
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

            print(input.o_id)
            print(input.power)
            print(input.s_ids)
            print(user_id)

            # 1. Check order milik user
            selected_order = db.query(database.models.TOrder).filter(
                database.models.TOrder.o_id == input.o_id,
                database.models.TOrder.u_id == user_id
            ).first()

            print("Data " + input.o_id)

            # 2. Cari power_id sesuai power input (<= input.power)
            selected_power_id = db.query(database.models.TPower.p_id)\
                .filter(database.models.TPower.p_power <= input.power)\
                .order_by(database.models.TPower.p_power.desc())\
                .limit(1)\
                .scalar()

            if not selected_order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found or not owned by user.")

            if not selected_power_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No suitable power found.")

            # 3. Insert TOrderArticle
            new_order_article = database.models.TOrderArticle(
                oa_id=routes.api.utils.generate_id(),
                p_id=selected_power_id,
                o_id=input.o_id,
                oa_power=input.power,
                oa_description=input.oa_description
            )
            db.add(new_order_article)
            db.flush()  # supaya new_order_article.oa_id ada di session

            # 4. Ambil harga dan spec dari TPriceList berdasarkan selected_power_id dan input.s_ids
            price_list_entries = db.query(database.models.TPriceList).filter(
                database.models.TPriceList.p_id == selected_power_id,
                database.models.TPriceList.s_id.in_(input.s_ids)
            ).all()

            # 5. Insert TOrderSpec berdasarkan price_list_entries
            order_specs = [
                database.models.TOrderSpec(
                    oa_id=new_order_article.oa_id,  # pake id yg baru dibuat
                    s_id=pl.s_id,
                    p_id=pl.p_id,
                    os_price=pl.pl_price
                )
                for pl in price_list_entries
            ]
            db.add_all(order_specs)

            # 6. Commit semua perubahan
            db.commit()

            return {"message": "Order berhasil ditambahkan", "o_id": input.o_id}

        except SQLAlchemyError as db_err:
            db.rollback()
            logger.error("Database error: %s", traceback.format_exc())
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.")

        except HTTPException:
            raise  # re-raise

        except Exception:
            logger.error("Unhandled exception: %s", traceback.format_exc())
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")
        
    def change_order(self, input: OrderChange, db: database.connection.db_dependency):
        try:
            query = db.query(database.models.TOrder).filter_by(
                o_id=input.o_id
            ).first()

            if not query:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order tidak ditemukan")

            query.o_description = input.o_description
            query.o_status = input.o_status
            db.commit()
            return {"message": "Order berhasil diperbarui"}
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
from fastapi import APIRouter, Request
import database.connection
import database.models
from typing import List
from fastapi import HTTPException, status, APIRouter, UploadFile, File
from routes.api.models.order_model import OrderOut, OrderCreate, OrderArticleCreate, OrderArticleOut, OrderItemSchema, PriceListOut, OrderArticleDelete, OrderChange, OrderDelete
import routes.api.utils
import routes.api.handler
import logging
import traceback
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlalchemy import text
import services.exel_manager
import services.pdf_manager
import asyncio
import time

logger = logging.getLogger(__name__)

class OrderAPI:
    def __init__(self):
        self.excel_manager = services.exel_manager.ExcelManager("maintenance_form.xlsx")
        self.pdf_manager = services.pdf_manager.PDFManager("maintenance_form.pdf")

        self.router = APIRouter(prefix="/api/order", tags=["Order"])
        self.router.add_api_route("/status", self.get_enum_order_status, methods=["GET"])
        self.router.add_api_route("/order", self.get_all_order, methods=["GET"])
        self.router.add_api_route("/order", self.insert_order, methods=["POST"])
        self.router.add_api_route("/order", self.change_order, methods=["PUT"])
        self.router.add_api_route("/order", self.delete_order, methods=["DELETE"])
        self.router.add_api_route("/order/{o_id}", self.get_order_by_id, methods=["GET"])
        self.router.add_api_route("/order/file", self.insert_order_file, methods=["POST"])
        self.router.add_api_route("/order-article", self.insert_order_article, methods=["POST"])
        self.router.add_api_route("/order-article/{o_id}", self.get_order_articles_with_items, methods=["GET"])
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
                o_name=input.o_name
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
        
    def get_order_articles_with_items(self, o_id: str, db: database.connection.db_dependency) -> List[OrderArticleOut]:
        try:
            articles = db.query(database.models.TOrderArticle).options(
                joinedload(database.models.TOrderArticle.order_items)  # load items
                    .joinedload(database.models.TOrderItem.pricelist)
            ).filter(
                database.models.TOrderArticle.o_id == o_id
            ).order_by(
                database.models.TOrderArticle.oa_time
            ).all()

            #if not articles:
            #    raise HTTPException(status_code=404, detail="Order articles not found.")

            """ return [
                {
                    "oa_id": article.oa_id,
                    "o_id": article.o_id,
                    "p_id": article.p_id,
                    "oa_power": article.oa_power,
                    "oa_name": article.oa_name,
                    "items": article.order_items  # OrderItemSchema
                }
                for article in articles
            ] """
            
            return [
                OrderArticleOut(
                    oa_id=article.oa_id,
                    o_id=article.o_id,
                    p_id=article.p_id,
                    oa_power=article.oa_power,
                    oa_name=article.oa_name,
                    items=[
                        OrderItemSchema(
                            i_id=item.i_id,
                            p_id=item.p_id,
                            os_price=item.os_price,
                            price_list=PriceListOut.model_validate(item.pricelist) if item.pricelist else None
                        )
                        for item in article.order_items
                    ]
                )
                for article in articles
            ]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def get_order_by_id(self, o_id: str, db: database.connection.db_dependency) -> OrderOut:
        try:
            order = db.query(database.models.TOrder).filter(database.models.TOrder.o_id == o_id).first()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found.")
            return OrderOut.model_validate(order)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def delete_order_article(self, input: OrderArticleDelete, db: database.connection.db_dependency):
        try:
            db_item = db.query(database.models.TOrderArticle).filter_by(oa_id=input.oa_id).first()
            if not db_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item tidak ditemukan")
            db.delete(db_item)
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
            print(input.i_id_list)
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
                oa_name=input.oa_name
            )
            db.add(new_order_article)
            db.flush()  # supaya new_order_article.oa_id ada di session

            # 4. Ambil harga dan item dari TPriceList berdasarkan selected_power_id dan input.i_id_list
            price_list_entries = db.query(database.models.TPriceList).filter(
                database.models.TPriceList.p_id == selected_power_id,
                database.models.TPriceList.i_id.in_(input.i_id_list)
            ).all()

            # 5. Insert TOrderItem berdasarkan price_list_entries
            order_items = [
                database.models.TOrderItem(
                    oa_id=new_order_article.oa_id,  # pake id yg baru dibuat
                    i_id=pl.i_id,
                    p_id=pl.p_id,
                    os_price=pl.pl_price
                )
                for pl in price_list_entries
            ]
            db.add_all(order_items)

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

            query.o_name = input.o_name
            query.o_status = input.o_status
            db.commit()
            return {"message": "Order berhasil diperbarui"}
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def delete_order(self, input: OrderDelete, db: database.connection.db_dependency):
        try:
            query = db.query(database.models.TOrder).filter_by(o_id=input.o_id).first()
            if not query:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order tidak ditemukan")
            db.delete(query)
            db.commit()
            return {"message": "Order berhasil dihapus"}
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def insert_order_file(self, request: Request, db: database.connection.db_dependency, order_file: UploadFile = File(...)):
        try:
            file_result_json = await routes.api.handler.upload_order_iden(order_file, self.excel_manager, self.pdf_manager)

            # input order
            input_order_result = self.insert_order(request, OrderCreate(o_name=file_result_json['order_name']), db)
            
            o_id = input_order_result['o_id']

            # input order_article
            for file_data in file_result_json['data']:
                article_power = file_data.get('POWER')
                if article_power is not None:
                    print(article_power)
                    article_power = str(int(float(article_power)))
                    article_name = file_data['ORDER_DESCRIPTION']
                    item_id_list = file_data['checkbox']

                    print("\n\n->", article_power)
                    self.insert_order_article(request, OrderArticleCreate(o_id=o_id, power=article_power, oa_name=article_name, i_id_list=item_id_list), db)
                    #time.sleep(1)
            
            return {"message": "File berhasil input", "data": o_id}

        except SQLAlchemyError as db_err:
            db.rollback()
            logger.error("Database error: %s", traceback.format_exc())
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.")

        except HTTPException:
            raise  # biarkan HTTPException diteruskan apa adanya

        except Exception:
            logger.error("Unhandled exception: %s", traceback.format_exc())
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")
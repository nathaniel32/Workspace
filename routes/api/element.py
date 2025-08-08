from fastapi import APIRouter
import database.connection
import database.models
from typing import List
from fastapi import HTTPException, status, APIRouter
from routes.api.models.element_model import PowerOut, PowerCreate, PowerUpdate, PowerDelete
from routes.api.models.element_model import ItemOut, ItemCreate, ItemUpdate, ItemDelete
from routes.api.models.element_model import PriceListOut, PriceChange, PowerChange
import routes.api.utils
from sqlalchemy import asc

class ElementAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/api/element", tags=["Element"])
        self.router.add_api_route("/power", self.get_all_power, methods=["GET"])
        self.router.add_api_route("/power", self.insert_power, methods=["POST"])
        self.router.add_api_route("/power", self.change_power, methods=["PUT"])
        self.router.add_api_route("/power", self.delete_power, methods=["DELETE"])

        self.router.add_api_route("/item", self.get_all_item, methods=["GET"])
        self.router.add_api_route("/item", self.insert_item, methods=["POST"])
        self.router.add_api_route("/item", self.update_item, methods=["PUT"])
        self.router.add_api_route("/item", self.delete_item, methods=["DELETE"])

        self.router.add_api_route("/price", self.get_all_price, methods=["GET"])
        self.router.add_api_route("/price", self.change_price, methods=["PUT"])
        
    def get_all_power(self, db: database.connection.db_dependency) -> List[PowerOut]:
        try:
            powers = db.query(database.models.TPower).order_by(database.models.TPower.p_power.asc()).all()
            return [PowerOut.model_validate(p) for p in powers]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def insert_power(self, input: PowerCreate, db: database.connection.db_dependency):
        try:
            new_power = database.models.TPower(
                p_id=routes.api.utils.generate_id(),
                p_power=input.p_power
            )
            db.add(new_power)
            db.commit()
            db.refresh(new_power)
            return {"message": "Power berhasil ditambahkan", "p_id": new_power.p_id}
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    def delete_power(self, input: PowerDelete, db: database.connection.db_dependency):
        try:
            db_power = db.query(database.models.TPower).filter_by(p_id=input.p_id).first()
            if not db_power:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Power tidak ditemukan")
            db.delete(db_power)
            db.commit()
            return {"message": "Power berhasil dihapus"}
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

    def get_all_item(self, db: database.connection.db_dependency) -> List[ItemOut]:
        try:
            items = db.query(database.models.TItem).order_by(asc(database.models.TItem.i_corrective), asc(database.models.TItem.i_item)).all()
            return [ItemOut.model_validate(s) for s in items]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    def insert_item(self, input: ItemCreate, db: database.connection.db_dependency):
        try:
            new_item = database.models.TItem(
                i_id=routes.api.utils.generate_id(),
                i_item=input.i_item,
                i_corrective=input.i_corrective
            )
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return {"message": "Item berhasil ditambahkan", "p_id": new_item.i_id}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def update_item(self, input: ItemUpdate, db: database.connection.db_dependency):
        try:
            query = db.query(database.models.TItem).filter_by(i_id=input.i_id).first()
            if not query:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item tidak ditemukan")
            query.i_item = input.i_item
            query.i_corrective = input.i_corrective
            db.commit()
            return {"message": "Item berhasil diperbarui"}
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def delete_item(self, input: ItemDelete, db: database.connection.db_dependency):
        try:
            db_item = db.query(database.models.TItem).filter_by(i_id=input.i_id).first()
            if not db_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item tidak ditemukan")
            db.delete(db_item)
            db.commit()
            return {"message": "Item berhasil dihapus"}
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
        
    def get_all_price(self, db: database.connection.db_dependency):
        try:
            results = db.query(database.models.TPriceList).all()
            return [PriceListOut.model_validate(p) for p in results]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    def change_price(self, input: PriceChange, db: database.connection.db_dependency):
        try:
            db_price = db.query(database.models.TPriceList).filter_by(
                p_id=input.p_id,
                i_id=input.i_id
            ).first()

            if not db_price:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kombinasi power & item tidak ditemukan")

            db_price.pl_description = input.pl_description
            db_price.pl_price = input.pl_price
            db.commit()
            return {"message": "Harga berhasil diperbarui"}
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def change_power(self, input: PowerChange, db: database.connection.db_dependency):
        try:
            query = db.query(database.models.TPower).filter_by(p_id=input.p_id).first()

            if not query:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Power tidak ditemukan")

            query.p_power = input.p_power
            query.p_unit = input.p_unit
            db.commit()
            return {"message": "Power berhasil diperbarui"}
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
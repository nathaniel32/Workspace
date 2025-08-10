from fastapi import APIRouter, Request
import database.connection
import database.models
from typing import List
from fastapi import HTTPException, status, APIRouter
from routes.api.models.element_model import PowerOut, PowerCreate, PowerDelete
from routes.api.models.element_model import ItemOut, ItemCreate, ItemUpdate, ItemDelete
from routes.api.models.element_model import PriceListOut, PriceChange, PowerChange
import routes.api.utils
from sqlalchemy import asc
from jose import JWTError

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
        
    def get_all_power(self, request: Request, db: database.connection.db_dependency) -> List[PowerOut]:
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.ADMIN)
            powers = db.query(database.models.TPower).order_by(database.models.TPower.p_power.asc()).all()
            return [PowerOut.model_validate(p) for p in powers]
        
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def insert_power(self, request: Request, input: PowerCreate, db: database.connection.db_dependency):
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.ADMIN)
            new_power = database.models.TPower(
                p_id=routes.api.utils.generate_id(),
                p_power=input.p_power
            )
            db.add(new_power)
            db.commit()
            db.refresh(new_power)
            return {"message": "Power berhasil ditambahkan", "p_id": new_power.p_id}
        
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    def delete_power(self, request: Request, input: PowerDelete, db: database.connection.db_dependency):
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.ADMIN)
            db_power = db.query(database.models.TPower).filter_by(p_id=input.p_id).first()
            if not db_power:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Power tidak ditemukan")
            db.delete(db_power)
            db.commit()
            return {"message": "Power berhasil dihapus"}
        
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

    def get_all_item(self, request: Request, db: database.connection.db_dependency) -> List[ItemOut]:
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.USER)
            items = db.query(database.models.TItem).order_by(asc(database.models.TItem.i_corrective), asc(database.models.TItem.i_item)).all()
            return [ItemOut.model_validate(s) for s in items]
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    def insert_item(self, request: Request, input: ItemCreate, db: database.connection.db_dependency):
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.ADMIN)
            new_item = database.models.TItem(
                i_id=routes.api.utils.generate_id(),
                i_item=input.i_item,
                i_corrective=input.i_corrective
            )
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return {"message": "Item berhasil ditambahkan", "p_id": new_item.i_id}
        
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def update_item(self, request: Request, input: ItemUpdate, db: database.connection.db_dependency):
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.ADMIN)
            query = db.query(database.models.TItem).filter_by(i_id=input.i_id).first()
            if not query:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item tidak ditemukan")
            query.i_item = input.i_item
            query.i_corrective = input.i_corrective
            db.commit()
            return {"message": "Item berhasil diperbarui"}
        
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def delete_item(self, request: Request, input: ItemDelete, db: database.connection.db_dependency):
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.ADMIN)
            db_item = db.query(database.models.TItem).filter_by(i_id=input.i_id).first()
            if not db_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item tidak ditemukan")
            db.delete(db_item)
            db.commit()
            return {"message": "Item berhasil dihapus"}
        
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
        
    def get_all_price(self, request: Request, db: database.connection.db_dependency):
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.ADMIN)
            results = db.query(database.models.TPriceList).all()
            return [PriceListOut.model_validate(p) for p in results]
        
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    def change_price(self, request: Request, input: PriceChange, db: database.connection.db_dependency):
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.ADMIN)

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
        
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def change_power(self, request: Request, input: PowerChange, db: database.connection.db_dependency):
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.ADMIN)

            query = db.query(database.models.TPower).filter_by(p_id=input.p_id).first()

            if not query:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Power tidak ditemukan")

            query.p_power = input.p_power
            query.p_unit = input.p_unit
            db.commit()
            return {"message": "Power berhasil diperbarui"}
        
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
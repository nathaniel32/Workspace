from fastapi import APIRouter
import database.connection
import database.models
from typing import List
from fastapi import HTTPException, status, APIRouter
from routes.api.models.item_model import PowerOut, PowerCreate, PowerUpdate, PowerDelete
from routes.api.models.item_model import SpecOut, SpecCreate, SpecUpdate, SpecDelete
from routes.api.models.item_model import PriceListOut, PriceChange
import routes.api.utils

class ItemAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/api/item", tags=["Item"])
        self.router.add_api_route("/power", self.get_all_power, methods=["GET"])
        self.router.add_api_route("/power", self.insert_power, methods=["POST"])
        self.router.add_api_route("/power", self.update_power, methods=["PUT"])
        self.router.add_api_route("/power", self.delete_power, methods=["DELETE"])

        self.router.add_api_route("/spec", self.get_all_spec, methods=["GET"])
        self.router.add_api_route("/spec", self.insert_spec, methods=["POST"])
        self.router.add_api_route("/spec", self.update_spec, methods=["PUT"])
        self.router.add_api_route("/spec", self.delete_spec, methods=["DELETE"])

        self.router.add_api_route("/price", self.get_all_price, methods=["GET"])
        self.router.add_api_route("/price", self.change_price, methods=["PUT"])

    def get_all_power(self, db: database.connection.db_dependency) -> List[PowerOut]:
        try:
            powers = db.query(database.models.TPower).all()
            return [PowerOut.model_validate(p) for p in powers]
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
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    def update_power(self, input: PowerUpdate, db: database.connection.db_dependency):
        try:
            db_power = db.query(database.models.TPower).filter_by(p_id=input.p_id).first()
            if not db_power:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Power tidak ditemukan")
            db_power.p_power = input.p_power
            db.commit()
            return {"message": "Power berhasil diperbarui"}
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
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

    def get_all_spec(self, db: database.connection.db_dependency) -> List[SpecOut]:
        try:
            specs = db.query(database.models.TSpec).all()
            return [SpecOut.model_validate(s) for s in specs]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    def insert_spec(self, input: SpecCreate, db: database.connection.db_dependency):
        try:
            new_spec = database.models.TSpec(
                s_id=routes.api.utils.generate_id(),
                s_spec=input.s_spec,
                s_corrective=input.s_corrective
            )
            db.add(new_spec)
            db.commit()
            db.refresh(new_spec)
            return {"message": "Spec berhasil ditambahkan", "p_id": new_spec.s_id}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def update_spec(self, input: SpecUpdate, db: database.connection.db_dependency):
        try:
            db_spec = db.query(database.models.TSpec).filter_by(s_id=input.s_id).first()
            if not db_spec:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spec tidak ditemukan")
            db_spec.s_spec = input.s_spec
            db.commit()
            return {"message": "Spec berhasil diperbarui"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def delete_spec(self, input: SpecDelete, db: database.connection.db_dependency):
        try:
            db_spec = db.query(database.models.TSpec).filter_by(s_id=input.s_id).first()
            if not db_spec:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spec tidak ditemukan")
            db.delete(db_spec)
            db.commit()
            return {"message": "Spec berhasil dihapus"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
        
    def get_all_price(self, db: database.connection.db_dependency):
        try:
            results = (
                db.query(
                    database.models.TPriceList,
                    database.models.TPower.p_power,
                    database.models.TSpec.s_spec,
                )
                .join(database.models.TPower, database.models.TPriceList.p_id == database.models.TPower.p_id)
                .join(database.models.TSpec, database.models.TPriceList.s_id == database.models.TSpec.s_id)
                .all()
            )

            price_list = []
            for price, power_val, spec_val in results:
                price_list.append(
                    PriceListOut(
                        p_id=price.p_id,
                        s_id=price.s_id,
                        description=price.pl_description,
                        price=price.pl_price,
                        power=power_val,
                        spec=spec_val,
                    )
                )
            return price_list
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    def change_price(self, input: PriceChange, db: database.connection.db_dependency):
        try:
            db_price = db.query(database.models.TPriceList).filter_by(
                p_id=input.p_id,
                s_id=input.s_id
            ).first()

            if not db_price:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kombinasi power & spec tidak ditemukan")

            db_price.pl_description = input.pl_description
            db_price.pl_price = input.pl_price
            db.commit()
            return {"message": "Harga berhasil diperbarui"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
from fastapi import HTTPException, status, APIRouter
from sqlalchemy import text
from fastapi import UploadFile, File, Request
from fastapi.responses import FileResponse
from typing import List
from pathlib import Path
import shutil
import database.connection
from utils import config
import database.models
import routes.api.utils
from jose import JWTError

class MediaAPI:
    def __init__(self, excel_order_manager, pdf_order_manager, element_api):
        self.text_columns = [
            {
                "id": "NO",
                "name": "No"
            },
            {
                "id": "ORDER_DESCRIPTION",
                "name": "Equipment No"
            },
            {
                "id": "POWER",
                "name": "Motor KW",
                "number_validation": True
            }
        ]
        self.media_path = Path("data/media")
        self.excel_order_manager = excel_order_manager
        self.pdf_order_manager = pdf_order_manager
        self.element_api = element_api
        self.router = APIRouter(prefix="/api/media", tags=["Media"])
        self.router.add_api_route("/", self.list_media_files, methods=["GET"], response_model=List[str])
        self.router.add_api_route("/{filename}", self.download_media_file, methods=["GET"])
        self.router.add_api_route("/", self.upload_file, methods=["POST"])
        self.router.add_api_route("/{filename}", self.delete_file, methods=["DELETE"])
        self.router.add_api_route("/create_order_file", self.create_order_file, methods=["POST"])

    async def list_media_files(self, request: Request) -> List[str]:
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.USER)
            files = []
            if self.media_path.exists() and self.media_path.is_dir():
                for file_path in self.media_path.rglob("*"):
                    if file_path.is_file():
                        files.append(str(file_path.relative_to(self.media_path)))
            return sorted(files)
        
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    async def upload_file(self, request: Request, file: UploadFile = File(...)):
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.USER)
            self.media_path.mkdir(parents=True, exist_ok=True)

            # cegah path traversal
            safe_filename = Path(file.filename).name
            file_path = self.media_path / safe_filename

            # Simpan file secara streaming
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            return {"message": "File uploaded successfully", "data": safe_filename}

        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    async def download_media_file(self, request: Request, filename: str):
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.USER)
            file_path = (self.media_path / filename).resolve(strict=True)

            # cegah path traversal
            if not str(file_path).startswith(str(self.media_path.resolve())):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file path")

            return FileResponse(
                path=file_path,
                filename=file_path.name,
                media_type="application/octet-stream"
            )

        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except FileNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def delete_file(self, request: Request, filename: str):
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.USER)
            file_path = (self.media_path / filename).resolve(strict=True)
            
            if not str(file_path).startswith(str(self.media_path.resolve())):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file path")

            if file_path.exists():
                file_path.unlink()
                return {"message": f"{filename} deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="File not found")
            
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except FileNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def create_order_file(self, request: Request, db: database.connection.db_dependency):
        checkbox_columns = [c.model_dump() for c in self.element_api.get_all_item(request=request, db=db)]
    
        all_columns = []
        
        for col in self.text_columns:
            all_columns.append({
                "type": "text",
                "id": col["id"],
                "name": col["name"],
                "number_validation": col.get("number_validation", None)
            })
        for col in checkbox_columns:
            all_columns.append({
                "type": "checkbox",
                "id": col["i_id"],
                "name": col["i_item"]
            })

        xlsx_name = config.ORDER_FILE_XLSX
        pdf_name = config.ORDER_FILE_PDF
        
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.USER)
            self.media_path.mkdir(parents=True, exist_ok=True)

            self.excel_order_manager.create_form(
                filename=self.media_path / xlsx_name,
                all_columns=all_columns,
                num_rows=10
            )

            self.pdf_order_manager.create_form(
                filename=self.media_path / pdf_name,
                all_columns=all_columns,
                num_rows=14,
                title=config.ORDER_FILE_TITLE
            )

            return {"message": f"Files '{xlsx_name}' and '{pdf_name}' have been created successfully."}

        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
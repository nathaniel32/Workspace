from fastapi import HTTPException, status, APIRouter
from sqlalchemy import text
from fastapi import UploadFile, File
from fastapi.responses import FileResponse
from typing import List
from pathlib import Path
import shutil

class MediaAPI:
    def __init__(self, media_path):
        self.media_path = media_path
        self.router = APIRouter(prefix="/api/media", tags=["Media"])
        self.router.add_api_route("/", self.list_media_files, methods=["GET"], response_model=List[str])
        self.router.add_api_route("/{filename}", self.download_media_file, methods=["GET"])
        self.router.add_api_route("/", self.upload_file, methods=["POST"])
        self.router.add_api_route("/{filename}", self.delete_file, methods=["DELETE"])

    async def list_media_files(self) -> List[str]:
        try:
            files = []
            if self.media_path.exists() and self.media_path.is_dir():
                for file_path in self.media_path.rglob("*"):
                    if file_path.is_file():
                        files.append(str(file_path.relative_to(self.media_path)))
            return sorted(files)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    async def upload_file(self, file: UploadFile = File(...)):
        try:
            self.media_path.mkdir(parents=True, exist_ok=True)

            # cegah path traversal
            safe_filename = Path(file.filename).name
            file_path = self.media_path / safe_filename

            # Simpan file secara streaming
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            return {"message": "File uploaded successfully", "data": safe_filename}

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    async def download_media_file(self, filename: str):
        try:
            file_path = (self.media_path / filename).resolve(strict=True)

            # cegah path traversal
            if not str(file_path).startswith(str(self.media_path.resolve())):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file path")

            return FileResponse(
                path=file_path,
                filename=file_path.name,
                media_type="application/octet-stream"
            )

        except FileNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def delete_file(self, filename: str):
        try:
            file_path = (self.media_path / filename).resolve(strict=True)
            
            if not str(file_path).startswith(str(self.media_path.resolve())):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file path")

            if file_path.exists():
                file_path.unlink()
                return {"message": f"{filename} deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="File not found")
        except FileNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
from fastapi import HTTPException, status, APIRouter, Request
from routes.api.models.sql_workbench_model import SQLQuery
import database.connection
from sqlalchemy import text
from jose import JWTError
import routes.api.utils
import database.models

class SQLWorkbenchAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/api/workbench", tags=["Workbench"])
        self.router.add_api_route("/schema", self.schema, methods=["GET"])
        self.router.add_api_route("/query", self.query, methods=["POST"])
        self.router.add_api_route("/create_tables", self.create_tables, methods=["POST"])

    async def schema(self, request: Request):
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.ROOT)

            with open('database/schema.sql', 'r') as file:
                sql_script = file.read()
            return {"data": sql_script}
        
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except FileNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schema file not found")
        
    def query(self, request: Request, sql: SQLQuery, db: database.connection.db_dependency):
        query_text = sql.query
        if not query_text:
            raise HTTPException(status_code=400, detail="Missing 'query' in request body")

        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.ROOT)
            
            result = db.execute(text(query_text))

            if query_text.strip().lower().startswith(("insert", "update", "delete", "create", "drop", "alter", "truncate")):
                db.commit()
                message = "Query executed and committed successfully."
            else:
                message = "Query executed successfully."

            try:
                rows = result.fetchall()
                columns = result.keys()
                data = [dict(zip(columns, row)) for row in rows]
            except Exception:
                data = []

            return {
                "message": message,
                "data": data
            }
        
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    def create_tables(self, request: Request):
        try:
            routes.api.utils.auth_role(request, min_role=database.models.UserRole.ROOT)
            
            database.connection.create_tables()

            return {"message": "Tables berhasil dibuat"}
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
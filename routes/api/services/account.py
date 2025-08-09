import routes.api.utils
import database.connection
import database.models
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import Depends, HTTPException, status, Request, Body, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from datetime import timedelta
from jose import ExpiredSignatureError, JWTError
from passlib.context import CryptContext
from utils import config
from routes.api.models.account_model import Validation, AccountCreate, UserOut
from sqlalchemy import and_, text
from typing import Optional, List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/account/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AccountAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/api/account", tags=["Account"])
        self.router.add_api_route("/user", self.get_all_users, methods=["GET"])
        self.router.add_api_route("/role", self.get_enum_user_role, methods=["GET"])
        self.router.add_api_route("/create", self.create, methods=["POST"], status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/signup", self.signup, methods=["POST"], status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/login", self.login, methods=["POST"], status_code=status.HTTP_200_OK)
        self.router.add_api_route("/logout", self.logout, methods=["POST"], status_code=status.HTTP_200_OK)
        self.router.add_api_route("/validate", self.validate, methods=["POST"], status_code=status.HTTP_200_OK) # oauth buat app lain

    def get_all_users(self, db: database.connection.db_dependency) -> List[UserOut]:
        try:
            users = db.query(database.models.TUser).order_by(database.models.TUser.u_time.desc()).all()
            return [UserOut.model_validate(p) for p in users]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def create(self, input: AccountCreate, db: database.connection.db_dependency):
        try:
            code = routes.api.utils.generate_code(6)

            new_account = database.models.TUser(
                u_id = routes.api.utils.generate_id(),
                u_role = input.u_role.value,
                u_status = database.models.UserStatus.ACTIVATED,
                u_code = code
            )
            db.add(new_account)
            db.commit()
            db.refresh(new_account)
            return {"message": "Account berhasil dibuat", "data": code}
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def signup(self, request: Request, db: database.connection.db_dependency, form_oauth_data: OAuth2PasswordRequestForm = Depends(), name: str = Body(...), code: Optional[str] = Body(None)): # gk bisa pake basemodel karena OAuth2PasswordRequestForm
        form_oauth_data.username = form_oauth_data.username.strip()
        name = name.strip()
        
        if not form_oauth_data.username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email cannot be empty!")
        if not form_oauth_data.password.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password cannot be empty!")
        if not name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name cannot be empty!")
        
        strong_password_value, strong_password_message = routes.api.utils.is_strong_password(form_oauth_data.password)
        if not strong_password_value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strong_password_message)

        try:
            # Cek apakah ini user pertama
            user_count = db.query(database.models.TUser).count()
            if user_count == 0:
                new_user = database.models.TUser(
                    u_id = routes.api.utils.generate_id(),
                    u_name = name,
                    u_email = form_oauth_data.username,
                    u_password = pwd_context.hash(form_oauth_data.password),
                    u_role = database.models.UserRole.ROOT,
                    u_status = database.models.UserStatus.ACTIVATED
                )
                db.add(new_user)
                db.commit()
            else:
                invited_user = db.query(database.models.TUser).filter(
                    and_(
                        database.models.TUser.u_code == code,
                        database.models.TUser.u_email.is_(None)
                    )
                ).first()
                
                if not invited_user:
                    raise HTTPException(status_code=404, detail="Code not found")

                invited_user.u_name = name
                invited_user.u_email = form_oauth_data.username
                invited_user.u_password = pwd_context.hash(form_oauth_data.password)
                invited_user.u_code = None
                
                db.commit()

        except HTTPException:
            raise

        except IntegrityError as e:
            db.rollback()
            
            if "u_email" in str(e.orig):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The email address is already registered")
            
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occurred while saving user data. " + str(e))
        
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred on the server. Please try again later. " + str(e)
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )

        return self.login(request, db, form_oauth_data)

    def login(self, request: Request, db: database.connection.db_dependency, form_oauth_data: OAuth2PasswordRequestForm = Depends()):
        try:
            user = db.query(database.models.TUser).filter(database.models.TUser.u_email == form_oauth_data.username).first()
            if not user or not pwd_context.verify(form_oauth_data.password, user.u_password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
            
            u_email = form_oauth_data.username
            u_ip = request.client.host
            u_aud = request.headers.get("user-agent")
            u_id = user.u_id
            u_name = user.u_name
            u_role = user.u_role
            u_status = user.u_status

            access_token = routes.api.utils.create_access_token({"sub": u_name, "ip": u_ip, "aud": u_aud, "id": u_id, "email": u_email, "role": u_role, "status": u_status}, timedelta(hours=24))

            response = JSONResponse(content={"message": "Login successful", "access_token": access_token, "token_type": "bearer"}) #access_token, token_type, buat swagger
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,      # HTTPS = True
                samesite="Lax",    # atau 'Strict' / 'None'
                max_age=int(config.ACCESS_TOKEN_EXP) * 3600,
                path="/"
            )
            return response
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    def logout(self):
        try:
            response = JSONResponse(content={"message": "Logout successful"})
            response.delete_cookie(
                key="access_token",
                path="/"
            )
            return response
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def validate(self, input: Validation, token: str = Depends(oauth2_scheme)):
        try:
            message, payload = routes.api.utils.validate_token(token=token, ip=input.ip, aud=input.aud)
            return {"message": message, "data": payload}
        
        except HTTPException:
            raise
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"An error occurred: {str(e)}")
        
    def get_enum_user_role(self, db: database.connection.db_dependency):
        try:
            query = "SELECT e.enumlabel FROM pg_type t JOIN pg_enum e ON t.oid = e.enumtypid WHERE t.typname = 'userrole';"
            result = db.execute(text(query))
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
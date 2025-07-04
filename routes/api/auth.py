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
from routes.api.models.auth_model import Validation

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/api/auth", tags=["Authentication"])
        self.router.add_api_route("/signup", self.f_signup, methods=["POST"], status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/login", self.f_login, methods=["POST"], status_code=status.HTTP_200_OK)
        self.router.add_api_route("/logout", self.f_logout, methods=["POST"], status_code=status.HTTP_200_OK)
        self.router.add_api_route("/validate", self.f_validate, methods=["POST"], status_code=status.HTTP_200_OK) # oauth buat app lain

    def f_signup(self, request: Request, db: database.connection.db_dependency, form_oauth_data: OAuth2PasswordRequestForm = Depends(), name: str = Body(...)): # gk bisa pake basemodel karena OAuth2PasswordRequestForm
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
            # TODO Hanya Hapus yg blm terauth email
            prev_user = db.query(database.models.TUser).filter(database.models.TUser.u_email == form_oauth_data.username).first()
            
            # hapus yg belum di aktivasi email
            if prev_user and prev_user.u_status == database.models.UserStatus.NOT_ACTIVATED:
                db.delete(prev_user)
                db.flush()

            # Cek apakah ini user pertama
            user_count = db.query(database.models.TUser).count()

            new_user = database.models.TUser(
                u_id = routes.api.utils.generate_id(),
                u_name = name,
                u_email = form_oauth_data.username,
                u_password = pwd_context.hash(form_oauth_data.password),
                u_role = database.models.UserRole.ADMIN if user_count == 0 else database.models.UserRole.USER,
                u_status = database.models.UserStatus.ACTIVATED, # HARUS DI GANTI JIKA INGIN DENGAN AKTIVASI EMAIL
                u_code = routes.api.utils.generate_code(6)
            )
            db.add(new_user)
            db.commit()

        except IntegrityError as e:
            db.rollback()
            
            if "u_email" in str(e.orig):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Die E-Mail-Adresse ist bereits registriert")
            
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Beim Speichern der Benutzerdaten ist ein Fehler aufgetreten " + str(e))
        
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Auf dem Server ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut" + str(e)
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unerwarteter Fehler: {str(e)}"
            )

        return self.f_login(request, db, form_oauth_data)

    def f_login(self, request: Request, db: database.connection.db_dependency, form_oauth_data: OAuth2PasswordRequestForm = Depends()):
        user = db.query(database.models.TUser).filter(database.models.TUser.u_email == form_oauth_data.username).first()
        if not user or not pwd_context.verify(form_oauth_data.password, user.u_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="falsche E-Mail oder falsches Passwort")
        
        u_email = form_oauth_data.username
        u_ip = request.client.host
        u_aud = request.headers.get("user-agent")
        u_id = user.u_id
        u_name = user.u_name
        u_role = user.u_role
        u_status = user.u_status

        access_token = routes.api.utils.create_access_token({"sub": u_name, "ip": u_ip, "aud": u_aud, "id": u_id, "email": u_email, "role": u_role, "status": u_status}, timedelta(hours=24))

        response = JSONResponse(content={"message": "Anmeldung erfolgreich", "access_token": access_token, "token_type": "bearer"}) #access_token, token_type, buat swagger
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,      # HTTPS = True
            samesite="Lax",    # atau 'Strict' / 'None'
            max_age=config.ACCESS_TOKEN_EXP_STD * 3600,
            path="/"
        )
        return response
    
    def f_logout(self):
        response = JSONResponse(content={"message": "Logout erfolgreich"})
        response.delete_cookie(
            key="access_token",
            path="/"
        )
        return response

    def f_validate(self, form_data: Validation, token: str = Depends(oauth2_scheme)):
        print(token)
        try:
            message, payload = routes.api.utils.validate_token(token=token, ip=form_data.ip, aud=form_data.aud)
            return {"message": message, "data": payload}
        
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"An error occurred: {str(e)}")
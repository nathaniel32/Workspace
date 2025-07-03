from datetime import datetime, timedelta, timezone
import uuid
from jose import jwt
import config
import random
import string
import re
from jose import ExpiredSignatureError, JWTError, jwt
from database.models import UserRole

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=config.ACCESS_TOKEN_EXP_STD)):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + expires_delta
    
    to_encode.update({
        "exp": int(expire.timestamp()),  # Expiration (Unix timestamp)
        "iat": int(now.timestamp()),     # Issued at (Unix timestamp)
        "nbf": int(now.timestamp()),     # Token valid from (Unix timestamp)
        "jti": str(uuid.uuid4())         # JWT ID
    })
    
    to_encode["iss"] = config.APP_NAME  # Issuer

    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

def generate_code(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def is_strong_password(password):
    if len(password) < 8:
        return False, "Passwort muss mindestens 8 Zeichen lang sein."
    if not re.search(r"[A-Z]", password):
        return False, "Passwort muss mindestens einen Großbuchstaben enthalten."
    if not re.search(r"[a-z]", password):
        return False, "Passwort muss mindestens einen Kleinbuchstaben enthalten."
    if not re.search(r"\d", password):
        return False, "Passwort muss mindestens eine Zahl enthalten."
    if not re.search(r"[!\"#$%&'()*+,-./:;<=>?@\\^_`{|}~]", password): #kurang []
        return False, "Passwort muss mindestens ein Sonderzeichen enthalten."
    
    return True, "Passwort ist stark genug."

def generate_id():
    return str(uuid.uuid4()).replace('-', '')

def validate_token(token, ip, aud):
    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=[config.ALGORITHM],
            audience=aud,
            issuer=config.APP_NAME
        )

        now = datetime.now(timezone.utc)

        if payload['exp'] < int(now.timestamp()):
            raise ExpiredSignatureError("Token has expired.")
        
        if payload['nbf'] > int(now.timestamp()):
            raise JWTError("Token is not yet valid.")
        
        if payload["ip"] != ip:
            raise Exception("Falsches IP!")
        
        return "Ok", payload
    
    except ExpiredSignatureError:
        return "Token has expired.", None
    except JWTError as e:
        return f"Invalid token: {str(e)}", None
    except Exception as e:
        return f"An error occurred: {str(e)}", None

###############################################################################################

NAV_ITEMS = {
    "dashboard": {"url": "/dashboard", "name": "Dashboard"},
    "pricelist": {"url": "/dashboard/pricelist", "name": "Price List"},
    "dricelist": {"url": "/dashboard/dricelist", "name": "Price List"},
    "input": {"url": "/dashboard/input", "name": "Input"},
    "statistic": {"url": "/dashboard/statistic", "name": "Statistic"},
    "control": {"url": "/dashboard/control", "name": "Price List"},
    "login": {"url": "/", "name": "Login"}
}

def navigation_url(role=None):
    if role == UserRole.ADMIN:
        keys = ["dashboard", "pricelist", "input", "statistic", "control"]
    elif role == UserRole.USER:
        keys = ["dashboard", "dricelist", "input"]
    else:
        return [NAV_ITEMS["login"]]

    return [NAV_ITEMS[key] for key in keys]


def request_init(request):
    try:
        access_token = request.cookies.get("access_token")
        user_ip = request.client.host
        aud = request.headers.get("user-agent")

        message, payload = validate_token(access_token, user_ip, aud)
        if not payload:
            raise ValueError("Invalid token payload")

        role = payload.get('role')
        navigation = navigation_url(role)
        return navigation, payload

    except Exception as e:
        return navigation_url(), None

from fastapi.responses import RedirectResponse

def return_site(request, templates, url, redirect=False):
    navigation, payload = request_init(request)

    context = {
        "request": request,
        "navigation": navigation,
        "registered": payload is not None
    }

    if payload and payload.get("role"):
        if redirect:
            return RedirectResponse(url=url)
        
        return templates.TemplateResponse(url, context)

    return templates.TemplateResponse(
        "shared/base.html",
        context,
        status_code=401  # Unauthorized
    )
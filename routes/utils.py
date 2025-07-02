from datetime import datetime, timedelta, timezone
import uuid
from jose import jwt
import config
import random
import string
import re

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
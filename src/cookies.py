import datetime
from typing import Any

import jwt

from . import settings

ALGORITHM = "HS256"

def new_cookie(secret: str | bytes = settings.SECRET_KEY, 
               exp: datetime.timedelta = settings.COOKIE_LIFETIME,
               payload: dict[str, Any] = {}) -> str:
    
    _payload = payload | { "exp": datetime.datetime.utcnow() + exp }
    return jwt.encode(_payload, secret, algorithm=ALGORITHM)

def validate_cookie(cookie: str | bytes, secret: str | bytes = settings.SECRET_KEY) -> bool:
    try:
        # thorws error if exp has passed
        jwt.decode(cookie, secret, algorithms=[ALGORITHM])
        return True
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
        return False

def get_cookie(cookie: str, secret: str | bytes = settings.SECRET_KEY) -> dict:
    try:
        # thorws error if exp has passed
        payload = jwt.decode(cookie, secret, algorithms=[ALGORITHM])
        payload.pop("exp")
        return payload
    # catch expired signature and decode error
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return {}

def get_cookie_from(source: dict[str, str], 
                    dict_key: str, 
                    secret: str | bytes = settings.SECRET_KEY) -> dict:
    if (cookie := source.get(dict_key)) is None:
        return {}
    return get_cookie(cookie, secret)
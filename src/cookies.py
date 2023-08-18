import datetime
from typing import Optional, Any

import jwt

import time

DEFAULT_LIFETIME = datetime.timedelta(seconds=5)
ALGORITHM = "HS256"

def new_cookie(secret: str | bytes, 
               exp: datetime.timedelta = DEFAULT_LIFETIME,
               payload: dict[str, Any] = {}) -> str:
    
    _payload = payload | { "exp": datetime.datetime.utcnow() + exp }
    return jwt.encode(_payload, secret, algorithm=ALGORITHM)

def validate_cookie(cookie: str | bytes, secret: str | bytes) -> bool:
    try:
        # thorws error if exp has passed
        jwt.decode(cookie, secret, algorithms=[ALGORITHM])
        return True
    except jwt.ExpiredSignatureError:
        return False

def get_cookie(cookie: str, secret: str | bytes) -> Any | None:
    try:
        # thorws error if exp has passed
        return jwt.decode(cookie, secret, algorithms=[ALGORITHM])
    # catch expired signature
    except jwt.ExpiredSignatureError:
        return None
    # catch decode error
    except jwt.exceptions.DecodeError:
        return None
    
def get_cookie_from(source: dict[str, str], dict_key: str, secret: str | bytes) -> Any | None:
    if (cookie := source.get(dict_key)) is None:
        return None
    return get_cookie(cookie, secret)
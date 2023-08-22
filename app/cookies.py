from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Optional
from flask import request, Response

import jwt

from . import settings

def new_jwt(secret: str | bytes = settings.SECRET_KEY, 
            exp: Optional[datetime] = None,
            payload: dict[str, Any] = {}) -> str:
    
    exp = exp or datetime.utcnow() + settings.COOKIE_LIFETIME
    _payload = payload | { "exp": exp }
    return jwt.encode(_payload, secret, algorithm=settings.JWT_ALGORITHM)

def validate_jwt(encoded_str: str | bytes, 
                 secret: str | bytes = settings.SECRET_KEY) -> bool:
    try:
        # thorws error if exp has passed
        jwt.decode(encoded_str, secret, algorithms=[settings.JWT_ALGORITHM])
        return True
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
        return False

def get_jwt(encoded_str: str, 
            secret: str | bytes = settings.SECRET_KEY) -> dict:
    try:
        # thorws error if exp has passed
        payload = jwt.decode(encoded_str, secret, algorithms=[settings.JWT_ALGORITHM])
        return payload
    # catch expired signature and decode error
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return {}


class Cookie(Enum):
    USER_STATIC = auto()
    USER_DATA = auto()

    def get(self, key: str | None = None, type: Optional[Callable] = None) -> Any:
        if (encoded_str := request.cookies.get(self.name)) is None:
            return
        dct = get_jwt(encoded_str)

        if key is None:
            return dct
        value = dct.get(key)

        if type is None:
            return value
        return type(value)

    def set(self, 
            response: Response, 
            payload: dict[str, Any]={}, 
            exp: Optional[datetime] = None):
        cookie = new_jwt(payload=payload, exp=exp)
        response.set_cookie(self.name, cookie)

    def update(self, response: Response, new_payload: dict[str, Any]):
        old_payload = self.get()
        payload = old_payload | new_payload
        self.set(response, payload, exp=payload["exp"])

    def validate(self) -> bool:
        if(encoded_str := request.cookies.get(self.name)) is None:
            return False
        
        return validate_jwt(encoded_str)
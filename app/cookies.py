import datetime
from enum import Enum, auto
from typing import Any, Optional
from flask import request

import jwt

from . import settings

def new_cookie(secret: str | bytes = settings.SECRET_KEY, 
               exp: Optional[datetime.datetime] = None,
               payload: dict[str, Any] = {}) -> str:
    
    exp = exp or datetime.datetime.utcnow() + settings.COOKIE_LIFETIME
    _payload = payload | { "exp": exp }
    return jwt.encode(_payload, secret, algorithm=settings.JWT_ALGORITHM)

def validate_cookie(cookie: str | bytes, secret: str | bytes = settings.SECRET_KEY) -> bool:
    try:
        # thorws error if exp has passed
        jwt.decode(cookie, secret, algorithms=[settings.JWT_ALGORITHM])
        return True
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
        return False

def get_cookie(cookie: str, 
               secret: str | bytes = settings.SECRET_KEY, 
               pop_exp: bool = True) -> dict:
    try:
        # thorws error if exp has passed
        payload = jwt.decode(cookie, secret, algorithms=[settings.JWT_ALGORITHM])
        if pop_exp:
            payload.pop("exp")
        return payload
    # catch expired signature and decode error
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return {}

def get_cookie_from(source: dict[str, str], 
                    dict_key: str, 
                    secret: str | bytes = settings.SECRET_KEY,
                    pop_exp: bool = True) -> dict:
    if (cookie := source.get(dict_key)) is None:
        return {}
    return get_cookie(cookie, secret, pop_exp=pop_exp)


class Cookie(Enum):
    USER_STATIC = auto()
    USER_DATA = auto()

    def get(self, key: str | None = None, pop_exp: bool = True) -> Any:
        cookies = get_cookie_from(request.cookies, self.name, pop_exp=pop_exp)
        if key is None:
            return cookies
        return cookies.get(key)

    def set(self, response, payload={}, exp=None):
        cookie = new_cookie(payload=payload, exp=exp)
        response.set_cookie(self.name, cookie)

    def update(self, response, new_payload):
        old_payload = self.get(pop_exp=False)
        payload = old_payload | new_payload
        self.set(response, payload, exp=payload["exp"])

        
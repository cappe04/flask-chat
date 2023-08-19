import functools
from typing import Optional

from flask import redirect, request, url_for

from app import cookies


def require_cookie(*requirements: str, 
                   redirect_to: Optional[str] = None, 
                   with_args: bool = True):
    def require_cookie_inner(f):
        endpoint = redirect_to or (f.__module__.split(".")[-1] + "." + f.__name__)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):

            endpoint_args = kwargs if with_args else {}

            for requirement in requirements:
                cookie = request.cookies.get(requirement)
                if cookie is None or not cookies.validate_cookie(cookie):
                    return redirect(url_for("auth.login", redirect_to=endpoint, **endpoint_args))
            
            return f(*args, **kwargs)
        return wrapper
    return require_cookie_inner
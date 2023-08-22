import functools
from typing import Optional

from flask import redirect, request, url_for

from app import cookies
from app.cookies import Cookie


def require_cookie(*requirements: Cookie, 
                   redirect_to: Optional[str] = None, 
                   with_args: bool = True):
    def require_cookie_inner(f):
        endpoint = redirect_to or (f.__module__.split(".")[-1] + "." + f.__name__)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):

            endpoint_args = kwargs if with_args else {}

            for requirement in requirements:
                if not requirement.validate():
                    return redirect(url_for("auth.login", redirect_to=endpoint, **endpoint_args))
            
            return f(*args, **kwargs)
        return wrapper
    return require_cookie_inner
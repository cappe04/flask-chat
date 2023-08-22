

from flask import Blueprint, make_response, redirect, render_template, request, url_for

from app.cookies import Cookie
from app.db import DbHandle
from .utils import require_cookie

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return redirect(url_for("main.home"))

@bp.route("/home/")
@require_cookie(Cookie.USER_STATIC)
def home():
    user_id = Cookie.USER_STATIC.get("user_id")

    response = make_response(render_template("home.html", 
                           username=DbHandle().get_username(user_id), 
                           channels=DbHandle().get_channels()))

    return response
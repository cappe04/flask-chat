

from flask import Blueprint, redirect, render_template, request, url_for

from app import cookies
from app.db import DbHandle
from .utils import require_cookie

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return redirect(url_for("main.home"))

@bp.route("/home/")
@require_cookie("token", "user_id")
def home():
    user_id = cookies.get_cookie_from(request.cookies, "user_id").get("user_id")


    return render_template("home.html", 
                           username=DbHandle().get_username(user_id), 
                           channels=DbHandle().get_channels())
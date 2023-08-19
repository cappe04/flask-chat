

from flask import Blueprint, redirect, render_template, request, url_for, current_app

from app import cookies, database
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
                           username=database.get_username(user_id), 
                           channel_items=database.get_channels())


from flask import Blueprint, render_template, request

from app import cookies
from app.db import DbHandle
from app.schemas import convert_timestamp
from .utils import require_cookie


bp = Blueprint("chat", __name__)

@bp.route("/chat/<int:channel_id>")
@require_cookie("token", "user_id")
def chat(*, channel_id):
    if not DbHandle().validate_channel(channel_id):
        return # missing channel page
    
    user_id = cookies.get_cookie_from(request.cookies, "user_id").get("user_id")

    return render_template("chat.html",
                           username=DbHandle().get_username(user_id),
                           channel_name=DbHandle().get_channel_name(channel_id))
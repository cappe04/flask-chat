

from flask import Blueprint, render_template, request
from app import cookies, database

from .utils import require_cookie

bp = Blueprint("chat", __name__)

@bp.route("/chat/<int:channel_id>")
@require_cookie("token", "user_id")
def chat(*, channel_id):
    if not database.validate_channel(channel_id):
        return # missing channel page
    
    user_id = cookies.get_cookie_from(request.cookies, "user_id").get("user_id")

    messages = list(database.get_messages("channel_id", channel_id, 10))

    return render_template("chat.html",
                           username=database.get_username(user_id),
                           channel_name=database.get_channel_name(channel_id),
                           messages=messages)
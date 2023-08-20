

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

    messages = DbHandle().get_messages(channel_id)

    def convert_msgs():
        for message in messages or []:
            yield {
                "message_id": message["message_id"],
                "channel_id": message["channel_id"],
                "message": message["message"],
                "username": DbHandle().get_username(message["user_id"]),
                "post_time": convert_timestamp(message["post_time"]),
            }

    return render_template("chat.html",
                           username=DbHandle().get_username(user_id),
                           channel_name=DbHandle().get_channel_name(channel_id),
                           messages=convert_msgs())
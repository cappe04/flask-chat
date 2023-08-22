

from flask import Blueprint, make_response, render_template, request

from app.cookies import Cookie
from app.db import DbHandle
from app.schemas import convert_timestamp
from .utils import require_cookie


bp = Blueprint("chat", __name__)

@bp.route("/chat/<int:channel_id>")
@require_cookie(Cookie.USER_STATIC, Cookie.USER_DATA)
def chat(*, channel_id):
    if not DbHandle().validate_channel(channel_id):
        return # missing channel page
    
    user_id = Cookie.USER_STATIC.get("user_id")

    response = make_response(render_template("chat.html",
                             username=DbHandle().get_username(user_id),
                             channel_name=DbHandle().get_channel_name(channel_id)))
    
    Cookie.USER_DATA.update(response, { "last_channel": channel_id })

    return response
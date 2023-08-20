import time
import json

from flask import request
from flask_socketio import SocketIO, join_room

from app import cookies
from app.schemas import convert_timestamp
from app.db import DbHandle


socketio = SocketIO()

init_app = socketio.init_app
run = socketio.run


@socketio.on("client_connect")
def client_connect(data):
    channel_id = data.get("channel_id")
    if not DbHandle().validate_channel(channel_id):
        return

    join_room(channel_id)

@socketio.on("client_send_message")
def send_message(data):
    user_id = cookies.get_cookie_from(request.cookies, "user_id").get("user_id")

    timestamp = int(time.time())

    message_id = DbHandle().post_message(user_id=user_id, timestamp=timestamp, **data)
    channel_id = data["channel_id"]

    if message_id is None or not DbHandle().validate_channel(channel_id):
        socketio.emit("refresh")
        return
    
    socketio.emit("server_send_message", json.dumps({
        "message_id": message_id,
        "username": DbHandle().get_username(user_id),
        "timestamp": convert_timestamp(timestamp)
    } | data), to=channel_id)
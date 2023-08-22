import time

from flask import request
from flask_socketio import SocketIO, join_room

from app.cookies import Cookie
from app.schemas import convert_timestamp
from app.db import DbHandle, MessageFormat


socketio = SocketIO()

init_app = socketio.init_app
run = socketio.run


@socketio.on("client:connect")
def client_connect(data):
    channel_id = data.get("channel_id")
    if not DbHandle().validate_channel(channel_id):
        return

    join_room(channel_id)

@socketio.on("message:send")
def send_message(data):
    user_id = Cookie.USER_STATIC.get("user_id")

    timestamp = int(time.time())

    message_id = DbHandle().post_message(user_id=user_id, timestamp=timestamp, **data)
    channel_id = data["channel_id"]

    if message_id is None or not DbHandle().validate_channel(channel_id):
        socketio.emit("page:reload")
        return
    
    socketio.emit("message:new", data | {
        "message_id": message_id,
        "username": DbHandle().get_username(user_id),
        "timestamp": convert_timestamp(timestamp)
    }, to=channel_id)

@socketio.on("message:get")
def load_messages(data):
    if (offset := data.get("offset")) is None:
        return
    if (channel_id := data.get("channel_id")) is None:
        return
    
    messages = DbHandle().get_messages(channel_id, 
                                       offset=offset, 
                                       format=MessageFormat.CHAT)
    socketio.emit("message:load", messages, to=request.sid)
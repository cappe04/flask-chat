import time

from flask import request
from flask_socketio import SocketIO, join_room

from app.cookies import Cookie
from app.schemas import convert_timestamp
from app.db import DbHandle, MessageFormat


socketio = SocketIO()

init_app = socketio.init_app
run = socketio.run


@socketio.on("connect")
def client_connect():
    channel_id = Cookie.USER_DATA.get("last_channel", type=int)
    join_room(channel_id)

@socketio.on("message:send")
def send_message(data):
    user_id = Cookie.USER_STATIC.get("user_id")
    channel_id = Cookie.USER_DATA.get("last_channel", type=int)
    timestamp = int(time.time())
    message = data.get("message")

    message_id = DbHandle().post_message(channel_id, user_id, message, timestamp)
    
    if message_id is None:
        socketio.emit("page:reload")
        return
    
    socketio.emit("message:new", data | {
        "message_id": message_id,
        "username": DbHandle().get_username(user_id),
        "timestamp": convert_timestamp(timestamp),
        "message": message
    }, to=channel_id)

@socketio.on("message:get")
def load_messages(data):
    if (offset := data.get("offset")) is None:
        return
    
    messages = DbHandle().get_messages(Cookie.USER_DATA.get("last_channel", type=int), 
                                       offset=offset, 
                                       format=MessageFormat.CHAT)
    socketio.emit("message:load", messages, to=request.sid)
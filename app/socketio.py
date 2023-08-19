import time

from flask import request
from flask_socketio import SocketIO, join_room
from pydantic import ValidationError

from app import cookies, database
from app.schemas import ChatMessage, DatabaseMessage


socketio = SocketIO()

def init_socket(app):
    socketio.init_app(app)

def run(app, **kwargs):
    socketio.run(app, **kwargs)


@socketio.on("client_connect")
def client_connect(data):
    channel_id = data.get("channel_id")
    if not database.validate_channel(channel_id):
        return

    join_room(channel_id)

@socketio.on("client_send_message")
def send_message(data):
    user_id = cookies.get_cookie_from(request.cookies, "user_id").get("user_id")
    timestamp = int(time.time())
    
    try:
        database_message = DatabaseMessage(user_id=user_id, timestamp=timestamp, **data)
        message_id = database.append_message(database_message)

        username = database.get_username(database_message.user_id)
        chat_message = ChatMessage(username=username, message_id=message_id, 
                                   **database_message.model_dump())

    except ValidationError:
        socketio.emit("refresh")
        return

    socketio.emit("server_send_message", 
                  chat_message.model_dump_json(), 
                  to=chat_message.channel_id)
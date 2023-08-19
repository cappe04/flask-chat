import functools
import time
import json
from typing import Optional

from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_socketio import SocketIO, join_room
from pydantic import ValidationError

from . import settings
from . import cookies
from . import database
from .schemas import ChatMessage, DatabaseMessage

app = Flask(__name__)
app.config["SECRET_KEY"] = settings.SECRET_KEY
socketio = SocketIO(app)

def run(**kwargs):
    socketio.run(app, **kwargs)


def require_cookie(*requirements: str, 
                   redirect_to: Optional[str] = None, 
                   with_args: bool = True):
    def require_auth_inner(f):
        endpoint = f.__name__ if redirect_to is None else redirect_to

        @functools.wraps(f)
        def wrapper(*args, **kwargs):

            endpoint_args = kwargs if with_args else {}

            for requirement in requirements:
                cookie = request.cookies.get(requirement)
                if cookie is None or not cookies.validate_cookie(cookie):
                    return redirect(url_for("login", redirect_to=endpoint, **endpoint_args))
            
            return f(*args, **kwargs)
        return wrapper
    return require_auth_inner


@app.route("/")
def index():
    return redirect(url_for("home"))

@app.route("/home/")
@require_cookie("token", "user_id")
def home():
    user_id = cookies.get_cookie_from(request.cookies, "user_id").get("user_id")
    
    return render_template("home.html", 
                           username=database.get_username(user_id), 
                           channel_items=database.get_channels())

@app.route("/chat/<int:channel_id>")
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

@app.route("/login/", methods = ["GET", "POST"])
def login():
    args = request.args.to_dict()

    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]
        if (user_id := database.get_login(username, password)) is None:
            return render_template(
                "login.html", 
                args=args,
                error_message="Opss! You did something wrong. Im not surprised..."
            )

        endpoint = args.pop("redirect_to", "home")
        response = make_response(redirect(url_for(endpoint, **args)))

        token_cookie = cookies.new_cookie()
        response.set_cookie("token", token_cookie)
        user_cookie = cookies.new_cookie(payload={ "user_id": user_id })
        response.set_cookie("user_id", user_cookie)

        return response
    
    return render_template("login.html", args=args)



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

    socketio.emit("server_send_message", chat_message.model_dump_json(), to=chat_message.channel_id)

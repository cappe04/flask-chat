import functools
import time
from typing import Optional

from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_socketio import SocketIO, join_room
from pydantic import ValidationError

from . import settings
from . import cookies
from .schemas import ChatMessage

app = Flask(__name__)
app.config["SECRET_KEY"] = settings.SECRET_KEY
socketio = SocketIO(app)

db = {
    "cappe_04": "abc123",
    "a": "b",
}

channel = {
    0: "all",
    1: "not all"
}

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
    if (user := cookies.get_cookie_from(request.cookies, "user_id")) is None: 
        return
    
    return render_template("home.html", 
                           username=user.get("user_id"), 
                           channel_items=channel.items())


@app.route("/chat/<int:channel_id>")
@require_cookie("token", "user_id")
def chat(*, channel_id):
    if (channel_name := channel.get(channel_id)) is None:
        return
    
    user = cookies.get_cookie_from(request.cookies, "user_id")
    user_id = user.get("user_id")

    return render_template("chat.html",
                           username=user_id,
                           channel_name=channel_name)


@app.route("/login/", methods = ["GET", "POST"])
def login():

    args = request.args.to_dict()

    if request.method == "POST":

        username, password = request.form["username"], request.form["password"]
        if (username, password) in db.items():
            
            endpoint = args.pop("redirect_to", "home")
            response = make_response(redirect(url_for(endpoint, **args)))

            token_cookie = cookies.new_cookie()
            response.set_cookie("token", token_cookie)

            user_cookie = cookies.new_cookie(payload={ "user_id": username })
            response.set_cookie("user_id", user_cookie)

            return response
        
        return render_template("login.html", 
                               args=args,
                               error_message="Opss! You did something wrong. Im not surprised...")

    return render_template("login.html", args=args)



@socketio.on("client_connect")
def client_connect(data):
    if (channel_id := data.get("channel_id")) is None:
        return
    
    join_room(int(channel_id))


@socketio.on("client_send_message")
def send_message(data):
    user = cookies.get_cookie_from(request.cookies, "user_id")
    timestamp = int(time.time())
    try:
        message = ChatMessage(user_id=user.get("user_id"), 
                              timestamp=timestamp, 
                              **data)
    except ValidationError:
        socketio.emit("refresh")
        return

    socketio.emit("server_send_message", message.model_dump_json(), to=message.channel_id)

import functools
import os
import datetime
from typing import Optional

from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_socketio import SocketIO, join_room
import jwt

import cookies

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECREY_KEY", default="")
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


def require_cookie(*requirements: str, redirect_to: Optional[str] = None):
    def require_auth_inner(f):
        endpoint = f.__name__ if redirect_to is None else redirect_to

        @functools.wraps(f)
        def wrapper(*args, **kwargs):

            for requirement in requirements:
                cookie = request.cookies.get(requirement)
                if cookie is None or not cookies.validate_cookie(cookie, app.secret_key):
                    return redirect(url_for("login", redirect_to=endpoint, **kwargs))
            
            return f(*args, **kwargs)
        return wrapper
    return require_auth_inner


@app.route("/")
def root():
    return redirect(url_for("home"))


@app.route("/home/")
@require_cookie("token", "user")
def home():
    if (user := cookies.get_cookie_from(request.cookies, "user", app.secret_key)) is None: 
        return
    
    return render_template("home.html", 
                           user=user, 
                           channel_items=channel.items())


@app.route("/chat/<int:channel_id>")
@require_cookie("token", "user", redirect_to="home")
def chat(*, channel_id):
    if (user := cookies.get_cookie_from(request.cookies, "user", app.secret_key)) is None: 
        return
    if (channel_name := channel.get(channel_id)) is None:
        return
  
    return render_template("chat.html", 
                           user=user, 
                           channel_name=channel_name)


@app.route("/login/", methods = ["GET", "POST"])
def login():

    args = request.args.to_dict()

    if request.method == "POST":

        username, password = request.form["username"], request.form["password"]
        if (username, password) in db.items():
            
            endpoint = args.pop("redirect_to", "home")
            response = make_response(redirect(url_for(endpoint, **args)))

            token_cookie = cookies.new_cookie(app.secret_key)
            response.set_cookie("token", token_cookie)
            
            user_cookie = cookies.new_cookie(app.secret_key, payload={ "username": username })
            response.set_cookie("user", user_cookie)

            return response
        
        return render_template("login.html", 
                               args=args,
                               error_message="Opss! You did something wrong. Im not surprised...")

    return render_template("login.html", args=args)



@socketio.on("user_connect")
def event_user_connect(data):
    if (user := cookies.get_cookie_from(request.cookies, "user", app.secret_key)) is None: 
        return

    if (channel_id := data.get("channel_id")) is None:
        return

    join_room(channel_id)


@socketio.on("client_send_message")
def send_message(data):
    if (user := cookies.get_cookie_from(request.cookies, "user", app.secret_key)) is None: 
        return

    if (channel_id := data.get("channel_id")) is None:
        return

    socketio.emit("server_send_message", data | user, to=channel_id)

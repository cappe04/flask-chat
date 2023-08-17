import functools
import os
import datetime

from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_socketio import SocketIO

import jwt

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

TOKEN_LIFETIME = datetime.timedelta(seconds=5)

def run(**kwargs):
    socketio.run(app, **kwargs)

def validate_token(token, secret) -> bool:
    try:
        return bool(jwt.decode(token, secret, algorithms=["HS256"]))
    except jwt.ExpiredSignatureError:
        return False

def generate_token(secret) -> str:
    return jwt.encode({
        "exp": datetime.datetime.utcnow() + TOKEN_LIFETIME
    }, secret)

def get_user(request):
    user_cookie = request.cookies.get("user", default=None)
    if user_cookie is None:
        return
    
    return jwt.decode(user_cookie, 
                      app.secret_key, 
                      algorithms=["HS256"])

def require_auth(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):

        token = request.cookies.get("token", default=None)

        if token is None or not validate_token(token, app.secret_key):
            return redirect(url_for("login", redirect_to=f.__name__, **kwargs))
        
        # send socket event
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
def root():
    return redirect(url_for("home"))


@app.route("/home/")
@require_auth
def home():
    if (user := get_user(request)) is None: 
        return
    
    return render_template("home.html", 
                           user=user, 
                           channel_items=channel.items())


@app.route("/chat/<int:channel_id>")
@require_auth
def chat(*, channel_id):
    if (user := get_user(request)) is None: 
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
            response.set_cookie("token", generate_token(app.secret_key))
            response.set_cookie("user", 
                                jwt.encode({ "username": username }, app.secret_key), 
                                max_age=TOKEN_LIFETIME)
            return response
        
        return render_template("login.html", 
                               args=args,
                               error_message="Opss! You did something wrong. Im not surprised...")

    return render_template("login.html", args=args)


# dont need i think
@socketio.on("user_connect")
def event_user_connect():
    if (user := get_user(request)) is None: 
        return
    
    socketio.emit("user_connected", user, to=request.sid)


@socketio.on("client_send_message")
def send_message(data):
    if (user := get_user(request)) is None: 
        return

    socketio.emit("server_send_message", data | user)

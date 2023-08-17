import os

from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECREY_KEY", default="")
socketio = SocketIO(app)

db = {
    
}

def run(**kwargs):
    socketio.run(app, **kwargs)

@app.route("/")
def start_page():
    return render_template("index.html")

@socketio.on("event")
def handle_event(json, methods=["GET", "POST"]):
    print(json)
    socketio.emit("response", json)
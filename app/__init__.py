from flask import Flask

from . import settings, socketio
from .routes import auth, main, chat

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(chat.bp)

    socketio.init_socket(app)

    return app
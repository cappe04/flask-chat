from flask import Flask

from . import settings, socketio, db
from .routes import auth, main, chat

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["DATABASE"] = settings.DATABASE

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(chat.bp)

    socketio.init_app(app)
    db.init_app(app)

    return app
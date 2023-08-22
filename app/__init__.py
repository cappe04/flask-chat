from flask import Flask

from . import sockets, db, cli
from .routes import auth, main, chat

def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(chat.bp)

    sockets.init_app(app)
    db.init_app(app)
    cli.init_cli(app)

    return app
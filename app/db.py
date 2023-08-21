import os
import sqlite3
import json
import enum
from typing import Any

import click
from flask import current_app, g
import bcrypt
from pydantic import ValidationError

from .settings import DATABASE, DATABASE_SCHEMA, DATABASE_FUNCTIONS, DATABASE_SAMPLE_DATA
from .schemas import DbUser, DbMessage, convert_timestamp

class MessageFormat(enum.Enum):
    DATA = enum.auto()
    CHAT = enum.auto()

class DbHandle:
    """Singleton database handle. Can only be called within a flask requst context."""

    func_prefix = "DB_"

    def __new__(cls):
        if hasattr(cls, "instance"):
            return cls.instance
        cls.instance = super().__new__(cls)

        with current_app.open_resource(DATABASE_FUNCTIONS) as file:
            func_dict = json.load(file)

            for k, v in func_dict["commit"].items():
                setattr(cls.instance, cls.func_prefix + k, cls.__commit_(**v))

            for k, v in func_dict["read"].items():
                setattr(cls.instance, cls.func_prefix + k, cls.__read_(**v))
        
        return cls.instance

    @staticmethod
    def __commit_(command, fetchall):
        def wrapper(*db_args: Any) -> list[dict[str, Any]] | None:
            db = get_db()
            result = db.execute(command, db_args)
            result = result.fetchall() if fetchall else result.fetchone()
            db.commit()
            return result if result else None
        return wrapper

    @staticmethod
    def __read_(command, fetchall):
        def wrapper(*db_args: Any) -> dict[str, Any] | None:
            db = get_db()
            result = db.execute(command, db_args)
            result = result.fetchall() if fetchall else result.fetchone()
            return result if result else None
        return wrapper
    
    # region ---------------- User Functions ----------------
    def get_login(self, username: str, password: str) -> int | None:
        user_id = (self.DB_user_getid(username) or {}).get("user_id")
        if user_id is None:
            return

        hashed_pw = self.DB_user_getpw(user_id)["password"]
        if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
            return user_id
        return

    def validate_user(self, user_id: int) -> bool:
        return self.DB_user_getname(user_id) is not None

    def get_username(self, user_id: int):
        res = self.DB_user_getname(user_id) or {}
        return res.get("username")
    
    def new_user(self, username: str, password: str, profile_picture: bytes = None) -> bool:
        try:
            user = DbUser(username=username, 
                          password=password, 
                          profile_picture=profile_picture)
            self.DB_user_register(user.username,
                                  user.password,
                                  user.profile_picture)
            return True
        except ValidationError:
            return False
    # endregion

    # region ---------------- Channel Functions ----------------
    def get_channels(self, limit: int=100, offset: int=0) -> list[dict[str, Any]]:
        return self.DB_channel_getmany(limit, offset)
    
    def get_channel_name(self, channel_id: int) -> str | None:
        res = self.DB_channel_get_name(channel_id) or {}
        return res.get("channel_name")
    
    def validate_channel(self, channel_id: int) -> bool:
        return self.DB_channel_get_name(channel_id) is not None
    # endregion

    # region ---------------- Message Functions ----------------
    def post_message(self, *, channel_id, user_id, message, timestamp):
        try:
            db_message = DbMessage(channel_id=channel_id,
                                   user_id=user_id,
                                   message=message,
                                   post_time=timestamp)
            message_id = self.DB_message_post(db_message.channel_id, 
                                              db_message.user_id, 
                                              db_message.message, 
                                              db_message.post_time)

            return (message_id or {}).get("message_id")
        except ValidationError:
            return

    def get_messages(self, channel_id: int, 
                     limit: int = 10, 
                     offset: int = 0, 
                     format: MessageFormat = MessageFormat.DATA):
        messages = self.DB_message_getmany(channel_id, limit, offset)
        if format == MessageFormat.DATA or messages is None:
            return messages
        
        for i, message in enumerate(messages):
            messages[i] |= {
                "timestamp": convert_timestamp(message["post_time"]),
                "username": self.get_username(message["user_id"])
            }
        
        return messages

    #endregion




def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def init_db(sample_data: bool = False):
    db = get_db()

    with current_app.open_resource(DATABASE_SCHEMA, "r") as file:
        db.executescript(file.read())
    
    if not sample_data:
        return
    
    with current_app.open_resource(DATABASE_SAMPLE_DATA, "r") as file:
        db.executescript(file.read())


@click.command("init-db")
@click.option("--sample-data", default=False)
def init_db_command(sample_data):
    click.echo("initializing database" + " with sample data"*sample_data + "...")
    init_db(sample_data=sample_data)
    click.echo("finished!")


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(os.path.join(current_app.root_path, DATABASE))
        g.db.row_factory = dict_factory

    return g.db

def close_db(exeption):
    db = g.pop("db", None)

    if db is not None:
        db.close()
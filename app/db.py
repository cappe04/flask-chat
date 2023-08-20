import sqlite3

import click
from flask import current_app, g

from .settings import DATABASE, DATABASE_SCHEMA, DATABASE_FUNCTIONS, DATABASE_SAMPLE_DATA

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


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(exeption):
    db = g.pop("db", None)

    if db is not None:
        db.close()
from app.cli.db import init_db_command

def init_cli(app):
    app.cli.add_command(init_db_command)
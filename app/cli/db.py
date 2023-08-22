

import click

from app.db import init_db

@click.command("init-db")
@click.option("--sample-data", default=False)
def init_db_command(sample_data):
    click.echo("initializing database" + " with sample data"*sample_data + "...")
    init_db(sample_data=sample_data)
    click.echo("finished!")
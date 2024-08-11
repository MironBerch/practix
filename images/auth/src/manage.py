import click
import flask_migrate

from flask import Flask
from flask.cli import with_appcontext

from core.config import settings
from core.logger import logger
from db import postgres, redis


@click.command()
@with_appcontext
def makemigrations():
    flask_migrate.migrate()


@click.command()
@with_appcontext
def migrate():
    flask_migrate.upgrade()


@click.command()
@with_appcontext
def createsuperuser():
    ...


def create_app() -> Flask:
    app = Flask(__name__)
    app.logger = logger
    postgres.init(app)
    redis.redis = redis.init()
    app.cli.add_command(makemigrations)
    app.cli.add_command(migrate)
    app.cli.add_command(createsuperuser)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=settings.flask.host,
        port=settings.flask.port,
        debug=settings.flask.debug
    )

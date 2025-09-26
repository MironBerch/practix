import click
import flask_migrate
from flasgger import Swagger
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from flask import Flask, current_app
from flask.cli import with_appcontext

from src.api.urls import init_routers
from src.core.config import settings
from src.core.logger import logger
from src.db import postgres, redis


@click.command()
@with_appcontext
def makemigrations() -> None:
    flask_migrate.Migrate(current_app, postgres.db)
    flask_migrate.migrate()


@click.command()
@with_appcontext
def migrate() -> None:
    flask_migrate.upgrade()


@click.command()
@with_appcontext
def createsuperuser() -> None: ...


def create_app() -> Flask:
    app = Flask(__name__)
    app.logger = logger

    app.config['JWT_SECRET_KEY'] = settings.security.jwt_secret_key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = settings.security.jwt_access_token_expires
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = settings.security.jwt_refresh_token_expires

    CORS(app)

    postgres.init(app)
    redis.redis = redis.init()

    app.cli.add_command(makemigrations)
    app.cli.add_command(migrate)
    app.cli.add_command(createsuperuser)

    init_routers(app)

    app.config['SWAGGER'] = {
        'title': 'Movies auth API v1',
        'uiversion': 3,
    }

    swagger_template = {
        'securityDefinitions': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'JWT Authorization header using the Bearer scheme.\
                    Example: "Authorization: Bearer {token}"',
            }
        },
        'security': [{'Bearer': []}],
    }

    swagger_config = {
        'headers': [],
        'specs': [
            {
                'endpoint': 'apispec_1',
                'route': '/auth/api/openapi.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: True,
            }
        ],
        'static_url_path': '/auth/flasgger_static',
        'swagger_ui': True,
        'specs_route': '/auth/api/docs',
    }

    Swagger(app, template=swagger_template, config=swagger_config)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload) -> bool:
        jti = jwt_payload['jti']
        token_in_redis = redis.redis.get(jti)
        return token_in_redis is not None

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=settings.flask.host,
        port=settings.flask.port,
        debug=settings.flask.debug,
    )
else:
    app = create_app()

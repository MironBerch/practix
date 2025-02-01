import click
import flask_migrate
from celery import Celery, Task
from flasgger import Swagger
from flask_jwt_extended import JWTManager

from flask import Flask, current_app
from flask.cli import with_appcontext

from api.urls import init_routers
from core.config import settings
from core.logger import logger
from core.mail import mail
from db import postgres, redis


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config['CELERY'])
    celery_app.set_default()
    app.extensions['celery'] = celery_app
    return celery_app


@click.command()
@with_appcontext
def makemigrations():
    flask_migrate.Migrate(current_app, postgres.db)
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

    app.config.from_mapping(
        CELERY=dict(
            broker_url=settings.celery.broker_url,
            result_backend=settings.celery.result_backend,
            broker_connection_retry_on_startup=True,
            task_ignore_result=True,
        )
    )

    app.config['MAIL_SERVER'] = settings.mail.server
    app.config['MAIL_PORT'] = settings.mail.port
    app.config['MAIL_USERNAME'] = settings.mail.username
    app.config['MAIL_PASSWORD'] = settings.mail.password
    app.config['MAIL_USE_TLS'] = settings.mail.use_tls
    app.config['MAIL_USE_SSL'] = settings.mail.use_ssl

    mail.init_app(app)

    app.config['JWT_SECRET_KEY'] = settings.security.jwt_secret_key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = settings.security.jwt_access_token_expires
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = settings.security.jwt_refresh_token_expires

    postgres.init(app)
    redis.redis = redis.init()

    celery_init_app(app)

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
        'specs_route': '/auth/api/docs'
    }

    Swagger(app, template=swagger_template, config=swagger_config)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
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

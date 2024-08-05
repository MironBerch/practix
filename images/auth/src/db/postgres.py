from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask import Flask

from core.config import settings

db = SQLAlchemy()
migrate = Migrate()


def init(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
            user=settings.postgres.user,
            password=settings.postgres.password,
            host=settings.postgres.host,
            port=settings.postgres.port,
            db=settings.postgres.db,
        )
    )
    db.init_app(app)
    migrate.init_app(app, db)

from flask import Flask

from api.v1 import auth, health


def init_routers(app: Flask) -> None:
    """Register all `flask.Blueprint` on the application."""
    app.register_blueprint(health.bp)
    app.register_blueprint(auth.bp)

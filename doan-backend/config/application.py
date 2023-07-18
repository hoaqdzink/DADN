from flask import Flask
from flask_cors import CORS

from api.router import analysis_blueprint, admin_blueprint, default_blueprint
from config.config import Config
from db.db import db, session as db_session
from db.mongo_db import mongo_db


def config(app: Flask) -> Flask:
    app.config.from_object(Config)
    return app


def register_blueprint(app: Flask) -> Flask:
    app.register_blueprint(analysis_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(default_blueprint)
    return app


def configure_database(app: Flask):
    db.init_app(app)
    mongo_db.init_app(app, serverSelectionTimeoutMS=15000)

    try:
        mongo_db.cx.server_info()
    except Exception as err:
        raise err

    @app.teardown_request
    def shutdown_session(exception=None):
        db_session.remove()
        if exception and db_session.is_active:
            db_session.rollback()


def init_app() -> Flask:
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app = config(app)
    CORS(app)  # TODO: ensure correct security for CORS
    configure_database(app)
    app = register_blueprint(app)

    return app


def init_test_app(test_config) -> Flask:
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.config.from_object(test_config)
    CORS(app)  # TODO: ensure correct security for CORS
    configure_database(app)
    app = register_blueprint(app)

    return app

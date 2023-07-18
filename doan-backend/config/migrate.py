from flask import Flask
from flask_migrate import upgrade, migrate, Migrate

from db.db import db


def migrate_database(app: Flask):
    Migrate(app, db)

    with app.app_context():
        migrate()


def upgrade_database(app: Flask):
    Migrate(app, db)

    with app.app_context():
        upgrade()

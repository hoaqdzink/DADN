import argparse
import os

from dotenv import load_dotenv

from config.migrate import migrate_database, upgrade_database


def run():
    get_env()

    from config.application import init_app

    app = init_app()

    # Config for running Flask app:
    port = int(os.getenv("FLASK_PORT"))
    host = os.getenv("FLASK_HOST")
    debug = os.getenv("DEBUG") == "True"
    app.run(host=host, port=port, debug=debug)


def migrate():
    get_env()

    from config.application import init_app

    app = init_app()

    migrate_database(app)


def upgrade_db():
    get_env()

    from config.application import init_app

    app = init_app()

    upgrade_database(app)


def get_env(env: str):
    load_dotenv(".env")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=run)

    subparsers = parser.add_subparsers(help="sub commands")

    parser_migrate = subparsers.add_parser("migrate", help="Create new migrate version")
    parser_migrate.set_defaults(func=migrate)

    parser_upgrade_db = subparsers.add_parser(
        "migrate up", help="Upgrade db to the current schema version"
    )
    parser_upgrade_db.set_defaults(func=upgrade_db)

    args = parser.parse_args()
    args.func(args)

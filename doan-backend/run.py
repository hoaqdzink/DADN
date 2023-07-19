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


def get_env():
    load_dotenv(".env")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, help='default: run; migrate or migrate up',
                    choices=['migrate', 'migrate up'])
    
    args = parser.parse_args()
    if args.mode == "migrate":
        migrate()
    elif args.mode == "migrate up":
        upgrade_db()
    else:
        run()

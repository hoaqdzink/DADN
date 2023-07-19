import os


class Config(object):
    JWT_EXPIRY = int(os.getenv("JWT_EXPIRY"))
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # DB information
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )

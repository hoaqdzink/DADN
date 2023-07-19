import os


JWT_EXPIRY = 24


class Config(object):
    JWT_EXPIRY = os.getenv("JWT_EXPIRY") or JWT_EXPIRY

    # DB information
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )

import os
from datetime import timedelta
from pkg import secret_manager
import urllib.parse

# from binascii import unhexlify

JWT_EXPIRY = 24
SESSION_EXPIRY = 7  # day


class Config(object):
    JWT_EXPIRY = os.getenv("JWT_EXPIRY") or JWT_EXPIRY
    SECRET_KEY = os.getenv("SECRET_KEY")

    # SESSION EXPIRY
    PERMANENT_SESSION_LIFETIME = timedelta(days=SESSION_EXPIRY)

    # DB information
    SECRET_MANAGER_DB_NAME = os.getenv("SECRET_MANAGER_DB")
    SECRET_MANAGER_DB = {}
    if SECRET_MANAGER_DB_NAME:
        SECRET_MANAGER_DB = secret_manager.get_secret(SECRET_MANAGER_DB_NAME)

    DB_HOST = os.getenv("DB_HOST") or SECRET_MANAGER_DB.get("host")
    DB_USER = os.getenv("DB_USER") or SECRET_MANAGER_DB.get("username")
    DB_PASSWORD = os.getenv("DB_PASSWORD") or SECRET_MANAGER_DB.get("password")
    DB_NAME = os.getenv("DB_NAME") or SECRET_MANAGER_DB.get("dbname")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
    )

    SECRET_MANAGER_MONGO_DB_NAME = os.getenv("SECRET_MANAGER_MONGO_DB")
    SECRET_MANAGER_MONGO_DB = {}
    if SECRET_MANAGER_MONGO_DB_NAME:
        SECRET_MANAGER_MONGO_DB = secret_manager.get_secret(
            SECRET_MANAGER_MONGO_DB_NAME
        )
    MONGO_DB_USER = os.getenv("MONGO_DB_USER") or SECRET_MANAGER_MONGO_DB.get(
        "username"
    )
    MONGO_DB_PASSWORD = urllib.parse.quote(
        os.getenv("MONGO_DB_PASSWORD") or SECRET_MANAGER_MONGO_DB.get("password") or ""
    )
    MONGO_DB_HOST = os.getenv("MONGO_DB_HOST") or SECRET_MANAGER_MONGO_DB.get("host")
    MONGO_DB_PORT = int(
        os.getenv("MONGO_DB_PORT") or SECRET_MANAGER_MONGO_DB.get("port") or 6379
    )
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
    MONGO_URI = (
        os.getenv("MONGO_URI")
        or f"mongodb://{MONGO_DB_USER}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOST}:{MONGO_DB_PORT}/{MONGO_DB_NAME}?tls=false&retryWrites=false"
    )

    S3_BUCKET = os.getenv("S3_BUCKET") or ""

    # Encrypt/Decrypt
    # CRYPT_KEY = unhexlify(os.getenv('CRYPT_KEY'))
    # CRYPT_IV = unhexlify(os.getenv('CRYPT_IV'))

    # Encrypt/Decrypt
    CRYPT_KEY = (os.getenv("CRYPT_KEY") or "").encode()
    CRYPT_IV = (os.getenv("CRYPT_IV") or "").encode()

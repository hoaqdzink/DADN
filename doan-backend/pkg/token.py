import jwt
from datetime import datetime, timedelta
from config.config import Config


def get_token(body):
    body["exp"] = datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRY)
    token = jwt.encode(body, Config.JWT_SECRET_KEY)
    return token


def decode_token(token):
    data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    return data

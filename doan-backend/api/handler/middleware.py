from flask import request
from api.handler.api_response import response_unauthorized
from usecase import auth


def check_auth():
    if request.endpoint != "default.login":
        headers = request.headers
        if "Authorization" not in headers:
            return response_unauthorized({"message": "Not found token"})
        token = headers.get("Authorization")
        if not auth.check_auth(token):
            return response_unauthorized()

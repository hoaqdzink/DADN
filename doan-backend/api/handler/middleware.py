from flask import request
from api.handler.api_response import response_unauthorized
from usecase import auth


def check_auth():
    if request.endpoint != "default.login":
        if not auth.check_auth():
            return response_unauthorized()
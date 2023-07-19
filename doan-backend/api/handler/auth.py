from datetime import datetime, timezone
from flask import request

from api.handler.api_response import response_bad_request, response_success
from usecase import auth


def login():
    body = request.form
    email = body["email"]
    password = body["password"]
    is_validate, token = auth.login_by_email_password(email, password)
    if is_validate:
        return response_success({"token": token})
    else:
        return response_bad_request({"message": "Wrong email of password"})

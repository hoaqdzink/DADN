from datetime import datetime, timezone
from flask import request

from api.handler.api_response import API_Response, error, response
from usecase import auth


def login() -> API_Response:
    body = request.form
    email = body["email"]
    password = body["password"]
    is_validate, user = auth.login_by_email_password(email, password)
    if is_validate:
        if user.is_suspended:
            return error(msg.user["out_of_service"], 400)

        session[request.blueprint] = {
            "email": email,
            "hash_pass": user.password,
            "last_activity": datetime.now(timezone.utc),
        }
        session.permanent = True
        return response(
            {
                "email": email,
            },
            200,
        )
    else:
        return error(msg.user["login_fail"], 400)

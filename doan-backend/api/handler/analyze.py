from flask import request
from api.handler.api_response import (
    response_bad_request,
    response_server_error,
    response_created,
)
from usecase import analyze


def add_mode():
    form = request.form
    if "value" not in form:
        return response_bad_request({"mesage": "Not Found value"})
    value = form.get("value")
    if value not in ["0", "1"]:
        return response_bad_request({"mesage": "Wrong Value"})
    is_success = analyze.add_mode(value)
    if not is_success:
        return response_server_error()
    return response_created({"mode": value})


def add_motor_ctrl():
    form = request.form
    if "value" not in form:
        return response_bad_request({"mesage": "Not Found value"})
    value = form.get("value")
    if value not in ["0", "1"]:
        return response_bad_request({"mesage": "Wrong Value"})
    is_success = analyze.add_motor_ctrl(value)
    if not is_success:
        return response_server_error()
    return response_created({"mode": value})

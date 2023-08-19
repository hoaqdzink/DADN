from usecase import config as usecase_config
from api.handler import api_response
from flask import request
from pkg import token_helper


def set_notification(mode):
    headers = request.headers
    token = headers.get("Authorization").replace("Bearer ", "")
    user = token_helper.decode_token(token)
    id = user.get("id")

    is_notified = True
    if mode == "0":
        is_notified = False
    is_success = usecase_config.set_notification(id, is_notified)
    if not is_success:
        return api_response.response_server_error()

    return api_response.response_no_content()


def get_config():
    headers = request.headers
    token = headers.get("Authorization").replace("Bearer ", "")
    user = token_helper.decode_token(token)
    id = user.get("id")

    config = usecase_config.get_config(id)

    return api_response.response_success(config)

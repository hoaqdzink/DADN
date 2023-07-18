from flask import Response, jsonify
from typing import Union, Optional, Tuple

API_Response = Tuple[Response, int]


def response(body: Optional[Union[dict, str]], code: int) -> API_Response:
    return jsonify(body), code


def response_created(body: dict) -> API_Response:
    """Use for successful POST"""
    return response(body, 201)


def response_no_content() -> API_Response:
    """Use for successful PUT or DELETE apis"""
    return response(None, 204)


def error(message: str, code) -> API_Response:
    body = {
        "message": message,
        "code": code,
    }
    return response(body, code)

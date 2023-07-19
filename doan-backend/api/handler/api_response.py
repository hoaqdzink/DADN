from flask import Response, jsonify


def response(body, code):
    return jsonify(body), code

def response_success(body):
    # Use for successful request
    if body is not None:
        return response(body, 200)
    else:
        return response({"message": "successful"}, 200)


def response_created(body):
    # Use for successful POST
    return response(body, 201)


def response_no_content():
    # Use for successful PUT or DELETE apis
    return response(None, 204)


def response_bad_request(body=None):
    # Use for Bad Request
    if body is not None:
        return response(body, 400)
    else:
        return response({"message": "Bad Request"}, 400)
    
def response_unauthorized(body=None):
    # Use for unathorized request
    if body is not None:
        return response(body, 401)
    else:
        return response({"message": "Unauthorized"}, 401)


def error(message: str, code):
    body = {
        "message": message,
        "code": code,
    }
    return response(body, code)

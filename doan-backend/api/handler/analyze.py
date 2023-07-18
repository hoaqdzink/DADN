from flask import render_template, request, jsonify, session
from usecase import upload as process_upload
from api.handler.api_response import API_Response, error, response
from pkg.logger import logger


def upload() -> str:
    email = session["analysis"]["email"]
    data_files_ids = process_upload.get_list_files_not_confirmed(email)
    return render_template("upload.html", data_files_ids=data_files_ids)


def upload_file() -> API_Response:
    try:
        form = request.form
        email = session["analysis"]["email"]
        file_name = form["file_name"]
        status_code, body = process_upload.upload_file(email, file_name)
        return response(body, status_code)
    except Exception as e:
        logger.error(e)
        return response({"message": "Bad Request"}, 400)


def get_upload_presigned_url() -> API_Response:
    try:
        file_name = request.args["file_name"]
        email = session["analysis"]["email"]
        presigned_url = process_upload.get_upload_presigned_url(email, file_name)
        return response({"presigned_url": presigned_url}, 200)
    except Exception as e:
        logger.error(e)
        return response({"message": "Bad Request"}, 400)


def confirm_upload_file(data_files_id: int) -> API_Response:
    form = request.form
    tags = form["tags"]
    memo = form["memo"]
    email = session["analysis"]["email"]
    status_code, message = process_upload.confirm_upload_file(
        email, int(data_files_id), tags, memo
    )
    return jsonify(message), status_code


def delete_files() -> API_Response:
    body = request.args
    email = session["analysis"]["email"]
    data_files_id_list = body["ids"].split(",")
    data_files_ids = [int(data_files_id) for data_files_id in data_files_id_list]
    status_code, message = process_upload.delete_files(email, data_files_ids)
    return jsonify(message), status_code


def get_data_file() -> API_Response:
    email = session["analysis"]["email"]
    data_files_id = request.args.get("id", type=int)
    is_success, result = process_upload.get_file(data_files_id, email)
    if not is_success:
        return error(result["message"], 500)
    else:
        return response(result, 200)

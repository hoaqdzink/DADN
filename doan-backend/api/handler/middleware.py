from datetime import datetime, timezone
from typing import Union
import os
from flask import session, redirect, url_for, request, render_template
from werkzeug.wrappers.response import Response
from api.handler.api_response import error, API_Response
from usecase import config
from usecase import auth

TEMPLATE = [
    "analysis.index",
    "analysis.login_template",
    "analysis.dashboard",
    "analysis.upload",
    "analysis.edit_template",
    "analysis.edit_data_files",
    "analysis.analyze",
    "analysis.analyze_visualize",
    "admin.index",
    "admin.login_template",
    "admin.users",
    "admin.edit_user_template",
    "admin.add_user_template",
    "analysis.handle_analysis",
]
session_lifetime = float(os.getenv("SESSION_LIFETIME") or 3600)


def admin_check_auth():
    session.permanent = True
    session.modified = True

    request.files.get(
        "file"
    )  # Check there is file in body. If not, there will be Err_Connection

    if is_maintenance():
        return render_template("maintenance.html"), 399
    elif is_login():
        if session.get(request.blueprint):
            if request.blueprint == "admin":
                return redirect(url_for(f"{request.blueprint}.index"))
            else:
                return redirect(url_for(f"{request.blueprint}.dashboard"))
        return
    else:
        blueprint = session.get(request.blueprint)
        if "last_activity" in session[request.blueprint]:
            elapsed_time = (
                datetime.now(timezone.utc) - session[request.blueprint]["last_activity"]
            )
            if elapsed_time.total_seconds() > session_lifetime:
                return redirect_login(
                    "申し訳ありませんが、セッションの有効期限が経過しましたので、自動的にログアウトされました。再度ログインしてください。"
                )
            session[request.blueprint]["last_activity"] = datetime.now(timezone.utc)

    if not blueprint or is_pass_changed():
        return redirect_login("Unauthorized")


def is_maintenance() -> bool:
    return config.get_maintenance()


def is_pass_changed() -> bool:
    hash_pass = session[request.blueprint].get("hash_pass")
    email = session[request.blueprint].get("email")
    if request.blueprint == "admin":
        if auth.pass_changed("admin", email, hash_pass):
            return True
    if request.blueprint == "analysis":
        if auth.pass_changed("analysis", email, hash_pass):
            return True
    return False


def is_login() -> bool:
    if request.endpoint == "admin.login" or request.endpoint == "admin.login_template":
        return True
    elif (
        request.endpoint == "analysis.login"
        or request.endpoint == "analysis.login_template"
    ):
        return True
    return False


def redirect_login(msg: str) -> Union[Response, API_Response]:
    session[request.blueprint].clear()
    if request.endpoint in TEMPLATE:
        if request.blueprint == "admin":
            return redirect(url_for("admin.login_template"))
        if request.blueprint == "analysis":
            return redirect(url_for("analysis.login_template"))
        return redirect(url_for("admin.login_template"))
    else:
        return error(msg, 401)

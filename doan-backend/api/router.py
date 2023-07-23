from flask import Blueprint

from api.handler import auth, middleware, analyze

bp = Blueprint("default", __name__)

bp.add_url_rule("/login", view_func=auth.login, methods=["POST"], endpoint="login")

bp.add_url_rule("/login", view_func=auth.login, methods=["POST"], endpoint="login")

bp.add_url_rule(
    "/add_mode", view_func=analyze.add_mode, methods=["POST"], endpoint="add_mode"
)

bp.add_url_rule(
    "/add_motor_ctrl",
    view_func=analyze.add_motor_ctrl,
    methods=["POST"],
    endpoint="add_motor_ctrl",
)


@bp.before_request
def before_request():
    return middleware.check_auth()

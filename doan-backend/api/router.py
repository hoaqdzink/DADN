from flask import Blueprint, request

from api.handler import auth, middleware, analyze, config

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

bp.add_url_rule(
    "/stream",
    view_func=analyze.stream,
    methods=["GET"],
    endpoint="stream",
)

bp.add_url_rule(
    "/set_notification/<mode>",
    view_func=config.set_notification,
    methods=["PUT"],
    endpoint="set_notification",
)

bp.add_url_rule(
    "/get_config",
    view_func=config.get_config,
    methods=["GET"],
    endpoint="get_config",
)


@bp.before_request
def before_request():
    if request.method == "OPTIONS":
        pass
    else:
        return middleware.check_auth()

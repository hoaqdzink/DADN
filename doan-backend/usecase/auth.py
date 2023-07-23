from db.repository import users
from pkg import hash, token_helper


def check_auth(token):
    try:
        token = token.replace("Bearer ", "")
        data = token_helper.decode_token(token)
        id = data.get("id")
        user = users.get_user_by_id(id)
        if not user:
            return False
        return True

    except Exception as e:
        print(e)
        return False


def login_by_email_password(email, password):
    user_info = users.get_user_by_email(email)
    if user_info is None:
        print(f"{email} not exist")
        return False, None

    if hash.verify_pass(password, user_info.password):
        data = {"id": user_info.id}
        tk = token_helper.get_token(data)
        return True, tk

    return False, None

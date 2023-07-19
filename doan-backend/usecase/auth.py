from db.repository import users
from pkg import hash, jwt
from typing import Tuple

def check_auth(token):
    return True


def login_by_email_password(email, password):
    user_info = users.get_user_by_email(email)
    if user_info is None:
        print(f"{email} not exist")
        return False, None
    
    if hash.verify_pass(password, user_info.password):
        token = jwt.get_token(None)
        return True, token

    return False, None

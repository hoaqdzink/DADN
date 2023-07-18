from db.repository import users, admin_users
from pkg import hash
from pkg.logger import logger
from typing import Tuple


def login_by_email_password(email: str, password: str) -> Tuple[bool, str]:
    user_info = users.get_user_by_email(email)
    if user_info is None:
        logger.info(f"{email} not exist")
        return False, ""

    return hash.verify_pass(password, user_info.password), user_info


def admin_login_by_email_password(email: str, password: str) -> Tuple[bool, str]:
    try:
        admin_info = admin_users.get_admin_by_email(email)
    except Exception as e:
        logger.error(e)
        return False, ""

    return hash.verify_pass(password, admin_info.password), admin_info.password


def pass_changed(portal: str, email: str, hash_pass: str) -> bool:
    if portal == "admin":
        admin_info = admin_users.get_admin_by_email(email)
        return admin_info.password != hash_pass
    if portal == "analysis":
        user_info = users.get_user_by_email(email)
        if user_info is not None:
            if user_info.is_suspended:
                return True
            
            return user_info.password != hash_pass
        else:
            return True
    return False

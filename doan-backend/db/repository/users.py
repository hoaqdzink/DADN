from db.db import session
from entity.users import Users


def get_user_by_email(email):
    results = session.query(Users.email, Users.password).filter_by(email=email).all()
    return results[0] if len(results) > 0 else None

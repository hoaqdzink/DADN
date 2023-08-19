from db.db import session
from entity.users import Users


def get_user_by_email(email):
    results = (
        session.query(Users.id, Users.email, Users.password)
        .filter_by(email=email)
        .all()
    )
    return results[0] if len(results) > 0 else None


def get_user_by_id(id):
    results = (
        session.query(Users.id, Users.email, Users.password).filter_by(id=id).all()
    )
    return results[0] if len(results) > 0 else None


def get_notified_email():
    results = session.query(Users.email).filter_by(is_notified=True).all()
    emails = []
    for result in results:
        emails.append(result.email)
    return emails

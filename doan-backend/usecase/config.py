from db.repository import users


def set_notification(id, mode):
    is_success = users.set_notification_by_id(id, mode)
    return is_success

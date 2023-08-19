from db.repository import users


def set_notification(id, mode):
    is_success = users.set_notification_by_id(id, mode)
    return is_success


def get_config(id):
    is_notified = users.get_is_notified_by_id(id)
    return {'isNotified': is_notified}

import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from pkg.send_mail import send_mail
from usecase import analyze
from datetime import datetime
from pkg import db_helper

THRESHOLD = 30


def alert_temperature():
    data = analyze.get_latest_data()
    temp = data.get("temp")
    date_temp = temp[0].get("date")
    value_temp = float(temp[0].get("value") or 0)
    date_obj = datetime.strptime(date_temp, "%Y-%m-%dT%H:%M:%SZ")
    if (datetime.now() - date_obj).seconds <= 24 * 60 * 60 and value_temp > THRESHOLD:
        mail_body = f"Your Temperature is {value_temp} exceed threshold {THRESHOLD}"
        emails = db_helper.get_all("SELECT email from users WHERE is_notified=TRUE")
        for email in emails:
            send_mail("Temperature exceed threshold", mail_body, email[0])


def register_batch():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=alert_temperature, trigger="interval", hours=1)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

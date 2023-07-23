from pkg import adafruit
from datetime import datetime, timedelta
import os


def add_mode(value):
    aio_feed_mode = os.getenv("AIO_FEED_MODE")
    mode = adafruit.add(aio_feed_mode, value)
    if not mode:
        return False
    return True


def add_motor_ctrl(value):
    aio_feed_motor_ctrl = os.getenv("AIO_FEED_MOTOR_CTRL")
    mode = adafruit.add(aio_feed_motor_ctrl, value)
    if not mode:
        return False
    return True


def get_data_with_range(start=None, stop=None):
    aio_feed_temperature = os.getenv("AIO_FEED_TEMPERATURE")
    aio_feed_humidity = os.getenv("AIO_FEED_HUMIDITY")
    aio_feed_motor_fbk = os.getenv("AIO_FEED_MOTOR_FBK")

    current = datetime.utcnow()
    stop = stop or current.strftime("%Y-%m/%d:%H:%M")
    current_1_week = current - timedelta(weeks=1)
    start = start or current_1_week.strftime("%Y-%m/%d:%H:%M")

    temps = adafruit.get_range_value(aio_feed_temperature, start, stop)
    humids = adafruit.get_range_value(aio_feed_humidity, start, stop)
    motor_fbk = adafruit.get_latest_value(aio_feed_motor_fbk)

    return {"temp": temps, "humid": humids, "aio_feed_motor_fbk": motor_fbk}


def get_latest_data():
    aio_feed_temperature = os.getenv("AIO_FEED_TEMPERATURE")
    aio_feed_humidity = os.getenv("AIO_FEED_HUMIDITY")
    aio_feed_motor_fbk = os.getenv("AIO_FEED_MOTOR_FBK")

    temp = adafruit.get_latest_value(aio_feed_temperature)
    humid = adafruit.get_latest_value(aio_feed_humidity)
    motor_fbk = adafruit.get_latest_value(aio_feed_motor_fbk)

    return {"temp": [temp], "humid": [humid], "aio_feed_motor_fbk": motor_fbk}

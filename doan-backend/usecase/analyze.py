from pkg import adafruit
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

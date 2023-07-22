import random
import time
import os
from dotenv import load_dotenv
from pkg.adafruit_io import AdafruitIO
from handler import adafruit_msg
from pkg import serial

load_dotenv(".env")
adfruit_io = AdafruitIO()
AIO_FEED_TEMPERATURE = os.getenv("AIO_FEED_TEMPERATURE")
AIO_FEED_HUMIDITY = os.getenv("AIO_FEED_HUMIDITY")
AIO_FEED_MOTOR_FBK = os.getenv("AIO_FEED_MOTOR_FBK")
AIO_FEED_MOTOR_CTRL = os.getenv("AIO_FEED_MOTOR_CTRL")
AIO_FEED_MODE = os.getenv("AIO_FEED_MODE")

adfruit_io.on_subscribe(AIO_FEED_MOTOR_CTRL, adafruit_msg.motor_ctrl_handler)
adfruit_io.on_subscribe(AIO_FEED_MODE, adafruit_msg.mode_handler)


while True:
    temp, humid, motor_fbk = serial.get_data()
    adfruit_io.publish(AIO_FEED_TEMPERATURE, temp)
    adfruit_io.publish(AIO_FEED_HUMIDITY, humid)
    adfruit_io.publish(AIO_FEED_MOTOR_FBK, int(motor_fbk))
    print(temp, humid, motor_fbk)
    time.sleep(10)

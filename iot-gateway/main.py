import random
import time
import os
from dotenv import load_dotenv
from pkg.adafruit_io import AdafruitIO
from handler import adafruit_msg

load_dotenv(".env")
adfruit_io = AdafruitIO()
aio_feed_test = os.getenv("AIO_FEED_TEST")
adfruit_io.on_subscribe(aio_feed_test, adafruit_msg.message)


while True:
    value = random.randint(0, 100)
    print("Cap nhat :", value)
    adfruit_io.publish(aio_feed_test, value)
    time.sleep(30)

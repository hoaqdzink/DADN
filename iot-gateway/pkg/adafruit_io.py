from Adafruit_IO import MQTTClient
import os
import sys


class AdafruitIOMsg:
    def __init__(self):
        pass

    def aio(self, client, feed_id, payload):
        self.client = client
        self.feed_id = feed_id
        self.payload = payload

    def process_payload(self, msg_handler):
        msg_handler(self.payload)


class AdafruitIO:
    def __init__(self, aio_username=None, aio_key=None):
        aio_username = aio_username or os.getenv("IO_USERNAME")
        aio_key = aio_key or os.getenv("IO_KEY")
        client = MQTTClient(aio_username, aio_key)
        client.on_connect = self.__connected
        client.on_disconnect = self.__disconnected
        client.connect()
        self.client = client

    @staticmethod
    def __connected(client):
        print("Successfully Connected...")

    @staticmethod
    def __disconnected():
        print("Ngat ket noi ...")
        sys.exit(1)

    @staticmethod
    def __subscribe(client, userdata, mid, granted_qos):
        print("Subcribe successfully")

    def publish(self, aio_feed_id, value):
        self.client.publish(aio_feed_id, value)

    def on_subscribe(self, aio_feed_id, message_handler):
        self.client.subscribe(aio_feed_id)
        self.client.on_subscribe = self.__subscribe
        self.client.on_message = message_handler

        self.client.loop_background()

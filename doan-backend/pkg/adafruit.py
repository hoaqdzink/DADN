import requests
import os


def get_latest_value(feed_key):
    adafruit_key = os.getenv("ADAFRUIT_KEY")
    adafruit_username = os.getenv("ADAFRUIT_USER_NAME")
    url = os.getenv("ADAFRUIT_LASTEST_URL").format(
        username=adafruit_username, feed_key=feed_key
    )
    headers = {"X-AIO-Key": adafruit_key}
    response = requests.get(url, headers=headers)
    json_value = response.json()
    if len(json_value) > 0:
        data = json_value[0]
        return {"date": data.get("created_at"), "value": data.get("value")}
    else:
        return None


def get_range_value(feed_key, start_time, end_time):
    adafruit_key = os.getenv("ADAFRUIT_KEY")
    adafruit_username = os.getenv("ADAFRUIT_USER_NAME")
    url = os.getenv("ADAFRUIT_RANGE_URL").format(
        username=adafruit_username,
        feed_key=feed_key,
        start_time=start_time,
        end_time=end_time,
    )
    headers = {"X-AIO-Key": adafruit_key}
    response = requests.get(url, headers=headers)
    values = []
    if response.status_code == 200:
        json_value = response.json()
        if len(json_value) > 0:
            for data in json_value:
                values.append(
                    {"date": data.get("created_at"), "value": data.get("value")}
                )
    return values


def add(feed_key, value):
    adafruit_key = os.getenv("ADAFRUIT_KEY")
    adafruit_username = os.getenv("ADAFRUIT_USER_NAME")
    url = os.getenv("ADAFRUIT_ADD_URL").format(
        username=adafruit_username, feed_key=feed_key
    )
    headers = {"X-AIO-Key": adafruit_key}
    response = requests.post(url, headers = headers, data={"value": value})
    if response.status_code == 200:
        json_value = response.json()
        return json_value.get("value")
    return None

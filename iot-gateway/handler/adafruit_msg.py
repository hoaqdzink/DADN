from pkg import serial


def motor_ctrl_handler(client, feed_id, payload):
    if payload == "1":
        serial.write_data(b"01")
    if payload == "0":
        serial.write_data(b"00")


def mode_handler(client, feed_id, payload):
    print(f"Recieved:{payload}")

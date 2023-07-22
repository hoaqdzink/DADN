import serial
import io

ser = serial.Serial()
ser.baudrate = 9600
ser.port = "COM3"
if not ser.is_open:
    ser.open()


def get_data():
    data = ser.readline()
    data_str = data.decode("UTF-8").replace("\r\n", "")
    datas = data_str.split(",")

    temp = float(datas[0])
    humid = float(datas[1])
    motor_fbk = bool(datas[2])
    return temp, humid, motor_fbk

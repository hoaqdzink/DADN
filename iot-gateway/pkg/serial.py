import serial

ser = serial.Serial()
ser.baudrate = 9600
ser.port = "COM3"
if not ser.is_open:
    ser.open()


def get_data():
    data = ser.read_all()
    data_str = data.decode("UTF-8")
    datas = data_str.split("\r\n")[-2].split(",")
    if len(datas) >= 3:
        temp = float(datas[0])
        humid = float(datas[1])
        motor_fbk = bool(int(datas[2]))
        return True, [temp, humid, motor_fbk]
    else:
        return False, [0, 0, 0]


def write_data(data):
    ser.write(data)

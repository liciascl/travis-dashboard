import serial


class Send:
    def __init__(self, interface, baud):

        self.ser = serial.Serial(port=interface,
                                 baudrate=baud)

    def send_string(self, data):
        self.ser.write(data.encode())

    def close(self):
        self.ser.close()


if __name__ == "__main__":
    send = Send("/dev/ttyS0", 115200)

    send.send_string("RRRRCCCCGGGG")

    send.close()

import serial


class Send:
    def __init__(self, interface, baud):

        self.ser = serial.Serial(interface)

    def send_string(self, data):
        self.ser.write(data)  # Send back the received data

    def close(self):
        self.ser.close()

import serial
import time
import decimal

from .base import Sensor


CR = '\n'
ENQ = '\x05'
sleeptime_rs = 0.05


class PressureSensor(Sensor):
    def __init__(self, port, sensor):
        self.port = port
        self.sensor = sensor

    def read(self):
        ser = serial.Serial(self.port, 9600, timeout=5,
                            parity='N', bytesize=8, stopbits=1)
        ser.write('P'+bytes(self.sensor)+CR)
        time.sleep(sleeptime_rs)
        ser.readline()  # read acknowledgement
        time.sleep(sleeptime_rs)
        ser.write(ENQ)  # send enquiry
        time.sleep(sleeptime_rs)
        value = ser.readline().strip()  # read value
        ser.close()
        return self.from_string(value[2:])

    def to_string(self, value):
        return '%.2e' % value

    def from_string(self, value):
        return decimal.Decimal(value)

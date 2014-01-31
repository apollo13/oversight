import serial
import time

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
        ser.write('P'+str(self.sensor)+CR)
        time.sleep(sleeptime_rs)
        ser.readline()  # read acknowledgement
        time.sleep(sleeptime_rs)
        ser.write(ENQ)  # send enquiry
        time.sleep(sleeptime_rs)
        value = ser.readline()  # read value
        ser.close()
        return value[2:]

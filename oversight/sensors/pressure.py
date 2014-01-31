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
        ser = serial.Serial(port_no, 9600, timeout=5, parity='N', bytesize=8, stopbits=1)
        ser.write('P%s%s' % (self.sensor, CR))
        time.sleep(sleeptime_rs)
        ack = ser.readline()   # read acknowledgement
        time.sleep(sleeptime_rs)
        ser.write(ENQ);        # send enquiry
        time.sleep(sleeptime_rs)
        value = ser.readline() # read value
        ser.close()
        return value.strip()


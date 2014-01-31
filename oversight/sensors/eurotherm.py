from .base import Sensor

import minimalmodbus
# Yikes, but we can't change this otherwise
minimalmodbus.BAUDRATE = 9600


class EuroTherm(Sensor):
    def __init__(self, port, number_of_decimals):
        self.port = port
        self.number_of_decimals = number_of_decimals

    def read(self):
        instrument = minimalmodbus.Instrument(self.port, 1)
        data = instrument.read_register(1, self.number_of_decimals, signed=True)
        instrument.serial.close()
        return round(data, 2)

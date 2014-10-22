from .base import Sensor

import minimalmodbus
# Yikes, but we can't change this otherwise
minimalmodbus.BAUDRATE = 9600


class EuroTherm(Sensor):
    def __init__(self, port, number_of_decimals, register=1):
        self.port = port
        self.number_of_decimals = number_of_decimals
        self.register = register

    def read(self):
        instrument = minimalmodbus.Instrument(self.port, 1)
        data = instrument.read_register(self.register, self.number_of_decimals,
                                        signed=True)
        #instrument.serial.close()
        return round(data, 2)

    def write(self, value):
        instrument = minimalmodbus.Instrument(self.port, 1)
        instrument.write_register(self.register, value, self.number_of_decimals,
                                  signed=True)
        #instrument.serial.close()
        return ''

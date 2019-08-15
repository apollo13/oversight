from .base import Sensor

import minimalmodbus
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

import logging
logger = logging.getLogger(__name__)

class EuroTherm(Sensor):
    def __init__(self, port, number_of_decimals, register=1):
        self.port = port
        self.number_of_decimals = number_of_decimals
        self.register = register
        self.baudrate = 9600
        self.instrument = minimalmodbus.Instrument(self.port, 1)
        self.instrument.serial.baudrate = self.baudrate

    def read(self):
        data = self.instrument.read_register(self.register,
                                             self.number_of_decimals,
                                             signed=True)
        return round(data, 2)

    def write(self, value):
        self.instrument.write_register(self.register,
                                       value,
                                       self.number_of_decimals,
                                       signed=True)
        return ''

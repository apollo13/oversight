import random
import time

from .base import Sensor


class TestSensor(Sensor):
    def __init__(self, **kwargs):
        self.port = 'testport'

    def read(self):
        time.sleep(5)
        return random.randint(1, 100)

    def write(self, value):
        pass

    def to_string(self, value):
        return u"%i" % value

    def from_string(self, value):
        return unicode(value)

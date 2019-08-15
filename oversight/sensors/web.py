import decimal

from .base import Sensor
from requests import get

class WebSensor(Sensor):
    def __init__(self, url):
        self.url = url

    def read(self):
        res = get(self.url)
        if(res.status_code == 200):
            return self.from_string(res.text)
        return self.from_string("-1")

    def to_string(self, value):
        return '%.2e' % value

    def from_string(self, value):
        return decimal.Decimal(value)

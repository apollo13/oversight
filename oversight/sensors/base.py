

class Sensor(object):
    def read(self):
        raise NotImplementedError("Subclasses need to implement that method")

    def write(self, value):
        raise NotImplementedError("Subclasses need to implement that method")

    def to_string(self, value):
        if not isinstance(value, basestring):
            value = repr(value)
        return value

    def from_string(self, value):
        raise NotImplementedError("Subclasses need to implement that method")

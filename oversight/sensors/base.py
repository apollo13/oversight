from contextlib import contextmanager
import threading


GLOBAL_LOCK = threading.Lock()
LOCAL_LOCKS = {}


class Sensor(object):
    def read(self):
        raise NotImplementedError("Subclasses need to implement that method")

    def write(self, value):
        raise NotImplementedError("Subclasses need to implement that method")

    def api(self, action, args):
        if action == 'read':
            return self.to_string(self.read())
        elif action == 'write':
            return self.write(self.from_string(args[0]))

    def to_string(self, value):
        if not isinstance(value, basestring):
            value = repr(value)
        return value

    def from_string(self, value):
        return float(value)

    @property
    @contextmanager
    def lock(self):
        l = None
        if hasattr(self, 'port') and self.port not in LOCAL_LOCKS:
            with GLOBAL_LOCK:
                l = LOCAL_LOCKS[self.port] = threading.Lock()
        if l:
            with l:
                yield self
        else:
            yield self

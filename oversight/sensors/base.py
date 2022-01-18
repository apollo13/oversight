import threading
from contextlib import contextmanager

GLOBAL_LOCK = threading.Lock()
LOCAL_LOCKS = {}


class Sensor(object):
    def read(self):
        raise NotImplementedError("Subclasses need to implement that method")

    def write(self, value):
        raise NotImplementedError("Subclasses need to implement that method")

    def api(self, action, args):
        if action == "read":
            return self.to_string(self.read())
        elif action == "write":
            return self.write(self.from_string(args[0]))

    def to_string(self, value):
        if not isinstance(value, str):
            value = repr(value)
        return value

    def from_string(self, value):
        return float(value)

    @property
    @contextmanager
    def lock(self):
        if hasattr(self, "port"):
            if self.port not in LOCAL_LOCKS:
                with GLOBAL_LOCK:
                    if self.port not in LOCAL_LOCKS:
                        LOCAL_LOCKS[self.port] = threading.Lock()

            with LOCAL_LOCKS[self.port]:
                yield

        else:
            yield

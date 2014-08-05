import logging
import threading
import Queue
from SimpleXMLRPCServer import SimpleXMLRPCServer

from django.core.management.base import NoArgsCommand

from oversight.models import Sensor, LogEntry


logger = logging.getLogger(__name__)


SENSOR_INTERVAL = 60


def read_sensors():
    for sensor in Sensor.objects.all():
        backend = sensor.backend
        try:
            value = backend.to_string(backend.read())
        except Exception as e:
            logger.error("Task failed: ", exc_info=e)
            continue
        log = LogEntry.objects.create(sensor=sensor, value=value)
        sensor.current_log = log
        sensor.save(update_fields=['current_log'])


def api(sensor, action, args):
    sensor = Sensor.objects.get(api_endpoint=sensor)
    backend = sensor.backend
    with backend.lock:
        data = backend.api(action, args)
    return data


TASKS = {
    'read_sensors': read_sensors
}


def schedule_sensor_checks(queue):
    queue.put(('read_sensors',))
    timer = threading.Timer(SENSOR_INTERVAL, schedule_sensor_checks, args=[queue])
    timer.start()


def worker(queue):
    while True:
        item = queue.get()
        try:
            TASKS[item[0]](*item[1:])
        except Exception as e:
            logger.error("Task failed: ", exc_info=e)
        queue.task_done()


class Command(NoArgsCommand):
    def handle(self, **options):
        queue = Queue.Queue()
        server = SimpleXMLRPCServer(("localhost", 12345))
        server.register_function(api)
        schedule_sensor_checks(queue)
        threading.Thread(target=worker, args=[queue]).start()
        server.serve_forever()

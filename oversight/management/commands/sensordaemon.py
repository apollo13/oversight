import logging
import threading
import Queue
from SimpleXMLRPCServer import SimpleXMLRPCServer

from django.conf import settings
from django.core.management.base import NoArgsCommand

import requests

from oversight.models import Sensor, LogEntry


logger = logging.getLogger(__name__)


SENSOR_INTERVAL = 60

USE_PUSHOVER = getattr(settings, 'PUSHOVER_TOKEN') and getattr(settings, 'PUSHOVER_GROUP')


class SensorManager(object):
    def _check_alarm(self, sensor, backend, value):
        notify = False
        if sensor.alarm_below:
            below = backend.from_string(sensor.alarm_below)
            if value <= below:
                notify = True
        if sensor.alarm_above:
            above = backend.from_string(sensor.alarm_above)
            if value >= above:
                notify = True

        if notify and sensor.alarm_acked:
            requests.post('https://api.pushover.net/1/messages.json', {
                'token': settings.PUSHOVER_TOKEN,
                'user': settings.PUSHOVER_GROUP,
                'title': 'Oversight',
                'message': 'Sensor "%s" triggered an alarm.' % sensor.name,
                'priority': 1,
            })

    def _read_sensors(self):
        for sensor in Sensor.objects.all():
            if not sensor.logging_enabled:
                continue

            backend = sensor.backend
            try:
                with backend.lock:
                    value = backend.read()
                self._check_alarm(sensor, backend, value)
            except Exception as e:
                logger.error("Task failed: ", exc_info=e)
                continue
            log = LogEntry.objects.create(sensor=sensor, value=backend.to_string(value))
            sensor.current_log = log
            sensor.save(update_fields=['current_log'])

    def api(self, sensor, action, args):
        sensor = Sensor.objects.get(api_endpoint=sensor)
        backend = sensor.backend
        with backend.lock:
            data = backend.api(action, args)
        return data


def schedule_sensor_checks(queue):
    queue.put(('read_sensors',))
    timer = threading.Timer(SENSOR_INTERVAL, schedule_sensor_checks, args=[queue])
    timer.start()


def worker(queue, tasks):
    while True:
        item = queue.get()
        try:
            tasks[item[0]](*item[1:])
        except Exception as e:
            logger.error("Task failed: ", exc_info=e)
        queue.task_done()


class Command(NoArgsCommand):
    def handle(self, **options):
        queue = Queue.Queue()
        server = SimpleXMLRPCServer(("localhost", 12345))
        sensor_manager = SensorManager()
        server.register_instance(sensor_manager)
        tasks = {
            'read_sensors': sensor_manager._read_sensors
        }
        schedule_sensor_checks(queue)
        threading.Thread(target=worker, args=[queue, tasks]).start()
        server.serve_forever()

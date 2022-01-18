import logging
import threading
from queue import Queue
from xmlrpc.server import SimpleXMLRPCServer

from django.conf import settings
from django.core.management.base import BaseCommand

import requests

from oversight.models import Sensor, LogEntry


logger = logging.getLogger(__name__)


SENSOR_INTERVAL = 60

USE_PUSHOVER = getattr(settings, "PUSHOVER_TOKEN", None) and getattr(
    settings, "PUSHOVER_GROUP", None
)


class SensorManager(object):
    def _check_alarm(self, sensor, backend, value):
        if not USE_PUSHOVER:
            return

        notify = False
        msg = 'Sensor "%s" triggered an alarm: %s'
        if sensor.alarm_below:
            below = backend.from_string(sensor.alarm_below)
            if value <= below:
                notify = True
                part = "%s <= %s" % (backend.to_string(value), sensor.alarm_below)
        if sensor.alarm_above:
            above = backend.from_string(sensor.alarm_above)
            if value >= above:
                notify = True
                part = "%s >= %s" % (backend.to_string(value), sensor.alarm_above)

        if notify and sensor.alarm_acked:
            msg = msg % (sensor.name, part)
            sensor.alarm_acked = False
            sensor.save(update_fields=["alarm_acked"])
            requests.post(
                "https://api.pushover.net/1/messages.json",
                {
                    "token": settings.PUSHOVER_TOKEN,
                    "user": settings.PUSHOVER_GROUP,
                    "title": 'Alarm from "%s"' % sensor.name,
                    "message": msg,
                    "priority": 1,
                },
            )

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
            sensor.save(update_fields=["current_log"])

    def api(self, sensor, action, args):
        sensor = Sensor.objects.get(api_endpoint=sensor)
        backend = sensor.backend
        with backend.lock:
            data = backend.api(action, args)
        return data


def schedule_sensor_checks(queue):
    queue.put(("read_sensors",))
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


class Command(BaseCommand):
    def handle(self, **options):
        queue = Queue()
        server = SimpleXMLRPCServer(("localhost", 12345))
        sensor_manager = SensorManager()
        server.register_instance(sensor_manager)
        tasks = {"read_sensors": sensor_manager._read_sensors}
        schedule_sensor_checks(queue)
        threading.Thread(target=worker, args=[queue, tasks]).start()
        server.serve_forever()

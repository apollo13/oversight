from django.core.management.base import NoArgsCommand

from oversight.models import Sensor, LogEntry

class Command(NoArgsCommand):
    def handle(self, **options):
        for sensor in Sensor.objects.all():
            backend = sensor.backend
            value = backend.to_string(backend.read())
            log = LogEntry.objects.create(sensor=sensor, value=value)
            sensor.current_log = log
            sensor.save(update_fields=['current_log'])

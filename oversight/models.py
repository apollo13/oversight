import json

from django.core.exceptions import ValidationError
from django.db import models
#from django.utils.module_loading import import_by_path
from django.utils.module_loading import import_string
from django.utils.timezone import now


class Sensor(models.Model):
    name = models.CharField(max_length=255)
    api_endpoint = models.SlugField(unique=True)
    unit = models.CharField(max_length=255)
    sensor_class = models.CharField(max_length=255)
    params = models.TextField()
    current_log = models.ForeignKey('LogEntry', null=True,
                                    blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='+')
    log_plot = models.BooleanField(default=False)
    logging_enabled = models.BooleanField(default=True)

    alarm_below = models.CharField(max_length=255, blank=True)
    alarm_above = models.CharField(max_length=255, blank=True)
    alarm_acked = models.BooleanField(default=True)

    def clean(self):
        try:
            json.loads(self.params)
        except ValueError:
            raise ValidationError('Params is not a valid JSON object')

    @property
    def backend(self):
        params = json.loads(self.params)
        return import_string(self.sensor_class)(**params)

    @property
    def frozen(self):
        if self.current_log:
            return (now() - self.current_log.datetime).total_seconds() > 300

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name



class LogEntry(models.Model):
    datetime = models.DateTimeField(default=now)
    sensor = models.ForeignKey(Sensor,on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        index_together = (('sensor', 'datetime'),)

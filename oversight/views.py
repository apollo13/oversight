import json
from datetime import timedelta

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import now

from .models import Sensor, LogEntry


def index(request):
    sensor_data = Sensor.objects.select_related('current_log').order_by('name')
    return render(request, 'oversight/index.html', {'sensor_data': sensor_data})


def sensor_detail(request, slug):
    sensor = Sensor.objects.get(api_endpoint=slug)
    if request.GET.get('format') == 'json':
        sensor_data = LogEntry.objects\
            .filter(sensor=sensor, datetime__gt=now()-timedelta(days=2))\
            .order_by('datetime').values('datetime', 'value')
        sensor_data = json.dumps(list(sensor_data), cls=DjangoJSONEncoder)
        return HttpResponse(sensor_data)
    else:
        sensor_data = LogEntry.objects.filter(sensor=sensor).order_by('-datetime')[:5]
        context = {
            'sensor': sensor,
            'sensor_data': sensor_data
        }
        return render(request, 'oversight/detail.html', context)


def sensor_api(request, slug):
    return HttpResponse('')
    sensor = Sensor.objects.get(api_endpoint=slug)
    backend = sensor.backend
    if request.method == 'GET':
        data = backend.to_string(backend.read())
    elif request.method == 'POST':
        data = backend.write(backend.from_string('123'))
    return HttpResponse(data)

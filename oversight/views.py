from django.shortcuts import render
from django.http import HttpResponse

from .models import Sensor, LogEntry


def index(request):
    sensor_data = Sensor.objects.select_related('current_log')
    return render(request, 'oversight/index.html', {'sensor_data': sensor_data})


def sensor_detail(request, slug):
    sensor = Sensor.objects.get(api_endpoint=slug)
    sensor_data = LogEntry.objects.filter(sensor=sensor).order_by('-datetime')[:50]
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

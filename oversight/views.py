import xmlrpclib
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.utils.crypto import constant_time_compare
from django.views.decorators.csrf import csrf_exempt

from .models import Sensor, LogEntry


def _prepare_json_data(*sensors):
    data = []
    for sensor in sensors:
        sensor_data = LogEntry.objects\
            .filter(sensor=sensor, datetime__gt=now()-timedelta(days=2))\
            .order_by('datetime').values_list('datetime', 'value')
        data.append({'points': list(sensor_data), 'name': sensor.name,
                     'log_plot': sensor.log_plot})

    return data


def index(request):
    sensor_data = Sensor.objects.select_related('current_log').order_by('name')
    return render(request, 'oversight/index.html', {'sensor_data': sensor_data})


def sensor_detail(request, slug):
    sensor = Sensor.objects.get(api_endpoint=slug)
    if request.GET.get('format') == 'json':
        return JsonResponse(_prepare_json_data(sensor), safe=False)
    else:
        sensor_data = LogEntry.objects.filter(sensor=sensor).order_by('-datetime')[:5]
        context = {
            'sensor': sensor,
            'sensor_data': sensor_data
        }
        return render(request, 'oversight/detail.html', context)


def sensor_compare(request):
    sensors = request.GET.getlist('sensor')
    sensors = Sensor.objects.filter(api_endpoint__in=sensors)
    if request.GET.get('format') == 'json':
        return JsonResponse(_prepare_json_data(*sensors), safe=False)
    else:
        context = {'sensors': sensors}
        return render(request, 'oversight/compare.html', context)


@csrf_exempt
def sensor_api(request, slug, action):
    data = request.POST
    if not constant_time_compare(data.get('api-key', ''), settings.OVERSIGHT_KEY):
        raise PermissionDenied
    proxy = xmlrpclib.ServerProxy('http://localhost:12345', allow_none=True)
    return HttpResponse(proxy.api(slug, action, data.getlist('args')))

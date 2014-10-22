import json
import socket
import xmlrpclib
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.utils.crypto import constant_time_compare
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


@login_required
def toggle_logging(request):
    sensors = Sensor.objects.filter(api_endpoint__in=request.POST.getlist('sensor'))
    # Sadly flipping booleans doesn't work via a single query.
    for sensor in sensors:
        sensor.logging_enabled = not sensor.logging_enabled
        sensor.save(update_fields=['logging_enabled'])
    msg = "Toggled status of selected sensors."
    messages.add_message(request, messages.SUCCESS, msg)
    return redirect('oversight_index')


def index(request):
    sensor_data = Sensor.objects.select_related('current_log').order_by('name')
    return render(request, 'oversight/index.html', {'sensor_data': sensor_data})


def sensor_detail(request, slug):
    sensor = Sensor.objects.get(api_endpoint=slug)
    sensor_data = LogEntry.objects.filter(sensor=sensor).order_by('-datetime')[:5]
    context = {
        'sensor': sensor,
        'sensor_ids_json': json.dumps([slug]),
        'sensor_data': sensor_data
    }
    return render(request, 'oversight/detail.html', context)


def sensor_compare(request):
    if request.is_ajax():
        sensors = Sensor.objects.filter(api_endpoint__in=request.GET.getlist('sensor'))
        return JsonResponse(_prepare_json_data(*sensors), safe=False)

    sensors = request.POST.getlist('sensor')
    sensor_ids_json = json.dumps(sensors)
    sensors = Sensor.objects.filter(api_endpoint__in=sensors) \
        .select_related('current_log').order_by('name')
    context = {'sensors': sensors, 'sensor_ids_json': sensor_ids_json}
    return render(request, 'oversight/compare.html', context)


@csrf_exempt
def sensor_api(request, slug, action):
    data = request.POST
    if not constant_time_compare(data.get('api-key', ''), settings.OVERSIGHT_KEY):
        raise PermissionDenied
    proxy = xmlrpclib.ServerProxy('http://localhost:12345', allow_none=True)
    return HttpResponse(proxy.api(slug, action, data.getlist('args')))

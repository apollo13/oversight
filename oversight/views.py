import json
import xmlrpclib
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import now
from django.utils.crypto import constant_time_compare
from django.views.decorators.csrf import csrf_exempt

from .models import Sensor, LogEntry


def index(request):
    sensor_data = Sensor.objects.select_related('current_log').order_by('name')
    return render(request, 'oversight/index.html', {'sensor_data': sensor_data})


def sensor_detail(request, slug):
    sensor = Sensor.objects.get(api_endpoint=slug)
    if request.GET.get('format') == 'json':
        sensor_data = LogEntry.objects\
            .filter(sensor=sensor, datetime__gt=now()-timedelta(days=2))\
            .order_by('datetime').values_list('datetime', 'value')
        sensor_data = json.dumps(list(sensor_data), cls=DjangoJSONEncoder)
        return HttpResponse(sensor_data)
    else:
        sensor_data = LogEntry.objects.filter(sensor=sensor).order_by('-datetime')[:5]
        context = {
            'sensor': sensor,
            'sensor_data': sensor_data
        }
        return render(request, 'oversight/detail.html', context)


@csrf_exempt
def sensor_api(request, slug, action):
    # TODO: switch to post
    data = request.GET
    if not constant_time_compare(data.get('api-key', ''), settings.OVERSIGHT_KEY):
        raise PermissionDenied
    sensor = Sensor.objects.get(api_endpoint=slug)
    proxy = xmlrpclib.ServerProxy('http://localhost:12345', allow_none=True)
    return HttpResponse(proxy.api(slug, action, data.getlist('args')))

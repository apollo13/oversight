from django.conf.urls import patterns, url

from .views import (index, toggle_logging, sensor_detail, sensor_api, sensor_compare,
    ack_alarms)


urlpatterns = patterns('',
    url(r'^$', index, name='oversight_index'),
    url(r'^sensor/(?P<slug>[\w-]+)/$', sensor_detail, name='oversight_sensor_detail'),
    url(r'^toggle_logging/$', toggle_logging, name='oversight_toggle_logging'),
    url(r'^acknowledge_alarms/$', ack_alarms, name='oversight_ack_alarms'),
    url(r'^compare/$', sensor_compare, name='oversight_sensor_compare'),
    url(r'^api/(?P<slug>[\w-]+)/(?P<action>[^/]+)/$', sensor_api, name='oversight_sensor_api'),
)

from django.conf.urls import patterns, url

from .views import index, sensor_detail, sensor_api


urlpatterns = patterns('',
    url(r'^$', index, name='oversight_index'),
    url(r'^sensor/(?P<slug>[\w-]+)/$', sensor_detail, name='oversight_sensor_detail'),
    url(r'^api/(?P<slug>[\w-]+)/$', sensor_api, name='oversight_sensor_api'),
)

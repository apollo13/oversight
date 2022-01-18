from django.urls import path

from .views import (
    index,
    toggle_logging,
    sensor_detail,
    sensor_api,
    sensor_compare,
    ack_alarms,
)


urlpatterns = [
    path("", index, name="oversight_index"),
    path("sensor/<slug>/", sensor_detail, name="oversight_sensor_detail"),
    path("toggle_logging/", toggle_logging, name="oversight_toggle_logging"),
    path("acknowledge_alarms/", ack_alarms, name="oversight_ack_alarms"),
    path("compare/", sensor_compare, name="oversight_sensor_compare"),
    path("api/<slug>/<action>/", sensor_api, name="oversight_sensor_api"),
]

from django.contrib import admin

from .models import Sensor


class SensorAdmin(admin.ModelAdmin):
    save_as = True
    prepopulated_fields = {'api_endpoint': ('name',)}
    exclude = ('current_log',)


admin.site.site_header = 'Oversight administration'
admin.site.site_title = admin.site.site_header
admin.site.register(Sensor, SensorAdmin)

from django.apps import AppConfig
from django.contrib import admin


class OversightConfig(AppConfig):
   name = 'oversight'

   def ready(self):
       admin.autodiscover()

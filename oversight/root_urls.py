from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin


urlpatterns = patterns('',
    url(r'^oversight/', include('oversight.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(pattern_name='oversight_index')),
)

from django.urls import include, path
from django.views.generic.base import RedirectView

from django.contrib import admin


urlpatterns = [
    path("oversight/", include("oversight.urls")),
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="oversight_index")),
]

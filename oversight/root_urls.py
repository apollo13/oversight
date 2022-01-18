from django.conf.urls import include, url
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin


urlpatterns = [
    url(r'^oversight/', include('oversight.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(pattern_name='oversight_index')),
]#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

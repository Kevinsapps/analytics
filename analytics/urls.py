from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from .views import home, ProfileRedirect

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/profile/$', ProfileRedirect.as_view()),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^v1/events/', include('events.api_urls', namespace='events_api')),

    url(r'^$', home, name='home'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
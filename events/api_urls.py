from django.conf.urls import url, include

from .api import EventsCountView, TopUsersView, TopEventsView

urlpatterns = [
    url(r'^count/$', EventsCountView.as_view(), name='count'),
    url(r'^top_users/$', TopUsersView.as_view(), name='top_users'),
    url(r'^top_events/$', TopEventsView.as_view(), name='top_events')
]
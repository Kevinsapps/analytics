from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Count
from django.db.models.expressions import RawSQL

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Event


class EventsCountView(APIView):
    """
    View dedicated to returning the total number of events stored.
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        events_count = Event.objects.count()

        return Response({'count_int': events_count, 'count': intcomma(events_count)})


class TopUsersView(APIView):
    """
    Get users with the most events, and their count of events.
    @TODO: We may need a custom serializer for this eventually.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        kwargs['max_users'] optional (default: 5) - the max number of users to return.
        """
        limit = kwargs.get('max_users', 5)
        if not type(limit) == int:
            return Response({'message': 'max_users must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

        users = Event.objects.values('user__username').annotate(Count("id")).order_by()[:limit]
        num_users = len(users) + 1  # Note we need to +1 this due to the other user who is always around

        events_count = Event.objects.count()
        for user in users:
            # This could be done with more ORM magic, but we only have to loop through 5 items so this is plenty fast.
            events_count -= user['id__count']

        other_user = {
            'username': 'other',
            'count': events_count
        }

        data = {
            'count': num_users,
            'results': [{'username': u['user__username'], 'count': u['id__count']} for u in users]
        }

        data['results'].append(other_user)

        return Response(data)


class TopEventsView(APIView):
    """
    Get the types of events and number of events for each type.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # The superquery: SELECT ••• FROM "events_event" GROUP BY (((event->>'type')::text))
        # Unfortunately django 1.11  doesn't support values('jsonfield__value') yet.
        events = Event.objects.annotate(event_type=RawSQL("((event->>%s)::text)", ('type',))
                               ).values('event_type').annotate(Count("event_type")).order_by()

        data = {
            'count': len(events),
            'results': [{'event': e['event_type'], 'count': e['event_type__count']} for e in events]
        }

        return Response(data)

from django.contrib.humanize.templatetags.humanize import intcomma

from channels.generic.websockets import JsonWebsocketConsumer

from events.models import Event
from events.serializers import EventSerializer


class LogConsumer(JsonWebsocketConsumer):
    http_user = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connection_groups(self, **kwargs):
        return ['log']

    def connect(self, message, **kwargs):
        # Reply with accept: True for protocol reasons.
        super(LogConsumer, self).connect(message, **kwargs)

        self.group_send('log', 'hello {}'.format(message.user))

    def receive(self, content, **kwargs):
        self.group_send('log', content)

    def disconnect(self, message, **kwargs):
        self.group_send('log', 'bye {}'.format(message.user))


class EventConsumer(JsonWebsocketConsumer):
    http_user = True

    def connection_groups(self, **kwargs):
        return ['events']

    def receive(self, content, **kwargs):
        data = {
            'event': content,
            'user': self.message.user.pk
        }

        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            event = serializer.save()
            count = Event.objects.count()  # @TODO YIKES SLOW!! Look into caching this or something?
            self.group_send('events', {'count': intcomma(count)})
        else:
            self.send(serializer.errors)

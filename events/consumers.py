from django.contrib.humanize.templatetags.humanize import intcomma

from channels.generic.websockets import JsonWebsocketConsumer

from events.serializers import EventSerializer


class LogConsumer(JsonWebsocketConsumer):
    http_user = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connection_groups(self, **kwargs):
        return ['log']

    def connect(self, message, **kwargs):
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
        self.send('Data received')

        data = {
            'event': content,
            'user': self.message.user.pk
        }

        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            event = serializer.save()
            self.group_send('events', {'count': intcomma(event.pk)})
        else:
            self.send(serializer.errors)

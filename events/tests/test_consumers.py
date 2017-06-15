from channels import Channel, Group
from channels.test import ChannelTestCase, HttpClient, apply_routes
from django.contrib.auth import get_user_model

from events.consumers import EventConsumer, LogConsumer
from events.models import Event

User = get_user_model()


class LogConsumerTests(ChannelTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='123456')

    def test_anon_connected(self):
        """
        AnonymousUser connection
        """
        client = HttpClient()

        client.send_and_consume('websocket.connect', path='/log/')
        data = client.receive()
        self.assertEqual(data, "hello AnonymousUser")

    def test_user_connected(self):
        """
        Logged in user connection
        """
        client = HttpClient()
        client.login(username='test', password='123456')

        client.send_and_consume('websocket.connect', path='/log/')
        data = client.receive()
        self.assertEqual(data, "hello test")

    def test_other_user_login(self):
        """
        Test if another user joining send a message to everyone
        Note: Uses apply_routes for a change to see if it's nicer to work with.
        """
        client1 = HttpClient()
        client2 = HttpClient()

        user1 = self.user
        user2 = User.objects.create_user(
            username='test2', email='test@test.com', password='123456')

        client1.login(username='test', password='123456')
        client2.login(username='test2', password='123456')

        with apply_routes([LogConsumer.as_route(path='/log/')]):
            client1.send_and_consume('websocket.connect', path='/log/')
            self.assertEqual(client1.receive(), 'hello test')
            self.assertIsNone(client2.receive())

            client2.send_and_consume('websocket.connect', path='/log/')
            self.assertEqual(client2.receive(), 'hello test2')
            self.assertEqual(client1.receive(), 'hello test2')

    def test_other_user_logout(self):
        """
        Test if another user leaving sends a message to everyone
        Note: Uses apply_routes for a change to see if it's nicer to work with.
        """
        client1 = HttpClient()
        client2 = HttpClient()

        user1 = self.user
        user2 = User.objects.create_user(
            username='test2', email='test@test.com', password='123456')

        client1.login(username='test', password='123456')
        client2.login(username='test2', password='123456')

        with apply_routes([LogConsumer.as_route(path='/log/')]):
            client1.send_and_consume('websocket.connect', path='/log/')
            client2.send_and_consume('websocket.connect', path='/log/')

            client1.send_and_consume('websocket.disconnect', path='/log/')
            self.assertEqual(client2.receive(), 'hello test2')
            self.assertEqual(client2.receive(), 'bye test')


class EventsConsumerTests(ChannelTestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='123456')

    def test_create_event(self):
        """
        Ensure events can be created through the consumer.
        """
        client = HttpClient()
        payload = {'event': {'target': 'button', 'type': 'click'}}

        client.send_and_consume('websocket.connect', path='/events/')
        self.assertIsNone(client.receive())

        # client.send_and_consume('websocket.receive', path='/events/')
        Group('events').send(payload, immediately=True)
        self.assertEqual(client.receive(), payload)

        client.send_and_consume('websocket.receive', text=payload, path='/events/')

        self.assertDictEqual(client.receive(), {'count': '1'})

    def test_create_event_not_logged_in(self):
        """
        Ensure events created store non-logged in user.
        """
        client = HttpClient()
        payload = {'event': {'target': 'button', 'type': 'click'}}

        client.send_and_consume('websocket.receive', text=payload, path='/events/')

        event_count = Event.objects.count()
        self.assertEqual(event_count, 1)

        # We just guaranteed one event, so can use objects.first() with relative safety.
        event = Event.objects.first()
        self.assertEqual(event.user, None)

    def test_create_event_logged_in(self):
        """
        Ensure events created store logged in user.
        """
        client = HttpClient()
        client.login(username='test', password='123456')
        payload = {'event': {'target': 'button', 'type': 'click'}}

        client.send_and_consume('websocket.receive', text=payload, path='/events/')

        event_count = Event.objects.count()
        self.assertEqual(event_count, 1)

        # We just guaranteed one event, so can use objects.first() with relative safety.
        event = Event.objects.first()
        self.assertEqual(event.user, self.user)

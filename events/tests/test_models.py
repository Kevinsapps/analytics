from django.contrib.auth import get_user_model
from django.test import TestCase

from events.models import Event
User = get_user_model()


class EventTests(TestCase):

    def test_create_event(self):
        """
        Test to make sure we can create an event. Eventually will test validation on event creation too.
        """

        Event.objects.create(event={'target': 'button', 'type': 'click'})

        self.assertEqual(Event.objects.count(), 1)

    def test_str_not_loggedin(self):
        """
        test str(event) repr
        """
        event = Event.objects.create(event={'target': 'button', 'type': 'click'})

        self.assertEqual(str(event), 'click None')

    def test_str_loggedin(self):
        """
        test str(event) repr
        """
        user = User.objects.create_user(
            username='test', email='test@test.com', password='123456')
        self.client.login(username='test', password='123456')

        event = Event.objects.create(event={'target': 'button', 'type': 'click'}, user=user)

        self.assertEqual(str(event), 'click test')

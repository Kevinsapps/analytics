import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from events.models import Event
User = get_user_model()


class EventsCountViewTests(APITestCase):

    def setUp(self):
        Event.objects.get_or_create(event={'target': 'target', 'event': 'mousedown'})
        self.count_url = reverse('events_api:count')

    def test_count_events(self):
        """
        Ensure that adding accounts increases the count.
        """

        response = self.client.get(self.count_url)

        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data), 2)
        self.assertEquals(data.get('count'), '1')
        self.assertEquals(data.get('count_int'), 1)


class TopUsersViewTests(APITestCase):

    def setUp(self):
        self.top_url = reverse('events_api:top_users')
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='123456')

    def test_no_events(self):
        """
        Test what happens if we hae no events at all
        """
        self.client.login(username='test', password='123456')

        response = self.client.get(self.top_url)

        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data.get('count'), 1)

    def test_one_user_one_event(self):
        """
        Database has a user and event
        """
        Event.objects.create(event={'event': 'click'}, user=self.user)

        self.client.login(username='test', password='123456')

        response = self.client.get(self.top_url)

        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data.get('count'), 2)

        expected_results = [{'username': 'test', 'count': 1}, {'username': 'other', 'count': 0}]
        self.assertListEqual(data.get('results'), expected_results)


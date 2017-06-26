from django.urls import reverse
from django.test import TestCase


class SiteViewsTest(TestCase):

    def test_home(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
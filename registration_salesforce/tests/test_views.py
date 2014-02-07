from mock import patch

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.data = dict(
            first_name="Test",
            last_name="User",
            email="test@user.com",
            password1='asdfasdf',
            password2='asdfasdf',
            lead_source='mobilepartners.mozilla.org'
            )

        self.url = reverse('signup')

    def test_get(self):
        """
        A GET request should simply return a 200.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    @patch('requests.post')
    def test_successful_post(self, sf_post):
        """
        A successful POST request
        """
        response = self.client.post(self.url, data=self.data)
        self.assertTrue(sf_post.called)
        self.assertEqual(response.status_code, 302)
        users = User.objects.all()
        self.assertEqual(1, users.count())
        user = users[0]
        self.assertFalse(user.is_active)
        self.assertEqual(self.data['first_name'], user.first_name)

    @patch('requests.post')
    def test_honeypot_post(self, sf_post):
        """
        A POST request that includes the honeypot field
        """
        self.data['superpriority'] = 1
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(sf_post.called)
        users = User.objects.all()
        self.assertEqual(0, users.count())


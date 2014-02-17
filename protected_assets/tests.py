from __future__ import unicode_literals

from urllib import urlencode

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from mezzanine.conf import settings
from mezzanine.pages.models import RichTextPage

from .models import Agreement


User = get_user_model()


class AgreementMixin(object):
    """Base setup and helpers for testing user agreement related views."""

    def setUp(self):
        self.agreement_page = RichTextPage.objects.create(
            title='User Agreement', slug='download-agreement',
            content='Legal Text Here', login_required=True)
        self.agreement_url = self.agreement_page.get_absolute_url()
        self.asset_url = reverse('protected_assets.views.protected_download', args=['test.png', ])
        self.user = self.create_user(username='test', password='test')
        self.client.login(username='test', password='test')

    def create_user(self, **kwargs):
        """Create a test user."""
        defaults = {
            'username': 'test',
            'email': '',
            'password': 'test'
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)

    def create_agreement(self, **kwargs):
        """Create a signed agreement."""
        defaults = {
            'ip': '127.0.0.1',
            'version': settings.DOWNLOAD_AGREEMENT_VERSION
        }
        defaults.update(kwargs)
        if 'user' not in defaults:
            defaults['user'] = self.create_user()
        return Agreement.objects.create(**defaults)


class ProtectAssetTestCase(AgreementMixin, TestCase):
    """Integration test for attempting to download a protected asset."""

    def test_agreement_redirect(self):
        """If user has not signed the agreement they should be redirected to sign."""
        response = self.client.get(self.asset_url)
        expected_url = '%s?%s' % (self.agreement_url, urlencode({'next': self.asset_url}))
        self.assertRedirects(response, expected_url)

    def test_already_signed(self):
        """Download should be trigged if the agreement was previously signed."""
        self.create_agreement(user=self.user)
        response = self.client.get(self.asset_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=test.png')
        self.assertEqual(response['X-Accel-Redirect'], '/__protected__/test.png')

    def test_signed_old_version(self):
        """User will need to resign the agreement if they signed and older version."""
        self.create_agreement(user=self.user, version='0.9')
        response = self.client.get(self.asset_url)
        expected_url = '%s?%s' % (self.agreement_url, urlencode({'next': self.asset_url}))
        self.assertRedirects(response, expected_url)


class SignAgreementTestCase(AgreementMixin, TestCase):
    """Integration test for signing the user agreement."""

    def test_agree_to_terms(self):
        """Create Agreement record when user signs the form."""
        response = self.client.post(self.agreement_url, data={'agree': 'on'})
        self.assertRedirects(response, '/')
        self.assertTrue(Agreement.objects.filter(user=self.user).exists())

    def test_did_not_agree(self):
        """No record should be created if they didn't agree."""
        response = self.client.post(self.agreement_url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Agreement.objects.filter(user=self.user).exists())

    def test_next_redirect(self):
        """Redirect user to custom location."""
        next_url = self.asset_url
        url = '%s?next=%s' % (self.agreement_url, self.asset_url)
        response = self.client.post(url, data={'agree': 'on'})
        self.assertRedirects(response, next_url)
        self.assertTrue(Agreement.objects.filter(user=self.user).exists())

from django.contrib.auth import get_user_model
from django.test import TestCase

from mezzanine.conf import settings
from mezzanine.pages.models import RichTextPage

from .models import Agreement


User = get_user_model()


class AgreementMixin(object):
    """Base setup and helpers for testing user agreement related views."""

    def setUp(self):
        self.agreement_page = RichTextPage.object.create(
            title='User Agreement', slug='download-agreement',
            content='Legal Text Here', login_required=True)
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


class SignAgreementTestCase(AgreementMixin, TestCase):
    """Integration test for signing the user agreement."""

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from ..utils import build_site_for_language
from ..middleware import LocaleSiteMiddleware


class LocaleSiteMiddlewareTestCase(TestCase):
    """Set the current request site based on the user's language."""

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {}
        self.middleware = LocaleSiteMiddleware()

    def assertMatchedSite(self, request, site_id):
        self.assertTrue(hasattr(self.request, 'site_id'))
        self.assertEqual(self.request.site_id, site_id)
        self.assertIn('site_id', self.request.session)
        self.assertEqual(self.request.session['site_id'], site_id)

    def assertNoMatchedSite(self, request):
        self.assertFalse(hasattr(self.request, 'site_id'))
        self.assertNotIn('site_id', self.request.session)

    def test_default_language(self):
        """Don't set if using the default language."""
        self.request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        result = self.middleware.process_request(self.request)
        self.assertIsNone(result)
        self.assertNoMatchedSite(self.request)

    def test_other_language(self):
        """Switch to non-default language site."""
        site = build_site_for_language('zh-cn')
        self.request.LANGUAGE_CODE = 'zh-cn'
        result = self.middleware.process_request(self.request)
        self.assertIsNone(result)
        self.assertMatchedSite(self.request, site.pk)

    def test_unknown_language(self):
        """Use the default site if the language doesn't match a site."""
        self.request.LANGUAGE_CODE = 'foo'
        result = self.middleware.process_request(self.request)
        self.assertIsNone(result)
        self.assertNoMatchedSite(self.request)

    def test_switch_to_default(self):
        """Handle switching back the default after the site was previously set."""
        site = build_site_for_language('zh-cn')
        self.request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        self.request.session['site_id'] = site.pk 
        result = self.middleware.process_request(self.request)
        self.assertIsNone(result)
        self.assertNoMatchedSite(self.request)

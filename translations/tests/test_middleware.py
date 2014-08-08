from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from mock import patch

from ..utils import build_site_for_language
from ..middleware import LocaleSiteMiddleware, waffle


@patch.object(waffle, 'flag_is_active')
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

    def test_default_language(self, mock_flag):
        """Don't set if using the default language."""
        mock_flag.return_value = True
        self.request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        result = self.middleware.process_request(self.request)
        self.assertIsNone(result)
        self.assertNoMatchedSite(self.request)

    def test_other_language(self, mock_flag):
        """Switch to non-default language site."""
        mock_flag.return_value = True
        site = build_site_for_language('zh-cn')
        self.request.LANGUAGE_CODE = 'zh-cn'
        result = self.middleware.process_request(self.request)
        self.assertIsNone(result)
        self.assertMatchedSite(self.request, site.pk)

    def test_unknown_language(self, mock_flag):
        """Use the default site if the language doesn't match a site."""
        mock_flag.return_value = True
        self.request.LANGUAGE_CODE = 'foo'
        result = self.middleware.process_request(self.request)
        self.assertIsNone(result)
        self.assertNoMatchedSite(self.request)

    def test_switch_to_default(self, mock_flag):
        """Handle switching back the default after the site was previously set."""
        mock_flag.return_value = True
        site = build_site_for_language('zh-cn')
        self.request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        self.request.session['site_id'] = site.pk 
        result = self.middleware.process_request(self.request)
        self.assertIsNone(result)
        self.assertNoMatchedSite(self.request)

    def test_flag_not_enabled(self, mock_flag):
        """Switching is not available if the flag is not active."""
        mock_flag.return_value = False
        site = build_site_for_language('zh-cn')
        self.request.LANGUAGE_CODE = 'zh-cn'
        result = self.middleware.process_request(self.request)
        self.assertIsNone(result)
        self.assertNoMatchedSite(self.request)

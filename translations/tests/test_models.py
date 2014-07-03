from django.conf import settings
from django.contrib.sites.models import Site
from django.test import TestCase

from .. import models


class GetSiteForLanguageTestCase(TestCase):
    """Fetch site object for a given language."""

    def test_default_language(self):
        """Default language code should return the default site."""
        result = models.get_site_for_language(settings.LANGUAGE_CODE)
        expected = Site.objects.get_current()
        self.assertEqual(result, expected)

    def test_non_default_language(self):
        """Other languages are found by the site name."""
        expected = Site.objects.create(name='fr', domain='example.com')
        result = models.get_site_for_language('fr')
        self.assertEqual(result, expected)

    def test_not_found(self):
        """Handle languages without matching sites."""
        result = models.get_site_for_language('fr')
        self.assertIsNone(result)

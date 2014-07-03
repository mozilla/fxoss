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
        expected = Site.objects.create(name='zh-cn', domain='example.com')
        result = models.get_site_for_language('zh-cn')
        self.assertEqual(result, expected)

    def test_not_found(self):
        """Handle languages without matching sites."""
        result = models.get_site_for_language('zh-cn')
        self.assertIsNone(result)


class BuildSiteForLanguageTestCase(TestCase):
    """Create site for a given language."""

    def test_create_site(self):
        """Create a new site for the language code."""
        result = models.build_site_for_language('zh-cn')
        self.assertEqual(result.name, 'zh-cn')
        default = Site.objects.get_current()
        # New sites need to have different domains or this breaks
        # Mezzanine's expecation that the domain is unique
        self.assertNotEqual(result.domain, default.domain)

    def test_existing_site(self):
        """Site should not be created if it already exists."""
        result = models.build_site_for_language(settings.LANGUAGE_CODE)
        default = Site.objects.get_current()
        self.assertEqual(result, default)
        self.assertEqual(Site.objects.all().count(), 1)

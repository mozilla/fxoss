from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.query import QuerySet
from django.test import TestCase

from mezzanine.pages.models import Page, RichTextPage, Link

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


class BuildSiteContentTestCase(TestCase):
    """Copy content from one site to another."""

    def assertCopied(self, original, site):
        """Assert that the model was copied to the new site."""
        # Again use the QuerySet to get around the forced site filter
        # when using the CurrentSiteManager
        copied = QuerySet(original.__class__).filter(slug=original.slug, site=site)
        print original.site_id
        print QuerySet(original.__class__).all()
        self.assertTrue(copied.exists())
        self.assertEqual(copied.count(), 1)
        self.assertTrue(copied.exists())
        copy = copied[0]
        print copy.site_id
        self.assertNotEqual(copy.pk, original.pk)

    def test_copy_default_minimal(self):
        """Copy all CMS models from the default site (minimal example)."""
        # This will be created with the default site
        page = Page.objects.create(title='Build')
        site = Site.objects.create(name='zh-cn', domain='example.com')
        models.build_site_content(site)
        self.assertCopied(page, site)

    def test_copy_multiple_models(self):
        """CMS Pages, RichTextPage, Links should all be copied."""
        page = Page.objects.create(title='Build')
        # TODO: .create fails because somehow related to django-concurrency
        rich_page = RichTextPage(title='Learn', content='<h1>Title</h1>')
        rich_page.save()
        link = Link.objects.create(title='External Link')
        site = Site.objects.create(name='zh-cn', domain='example.com')
        models.build_site_content(site)
        self.assertCopied(page, site)
        self.assertCopied(rich_page, site)
        self.assertCopied(link, site)

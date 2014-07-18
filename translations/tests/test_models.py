from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.query import QuerySet
from django.test import TestCase

from mezzanine.forms.models import Form, Field
from mezzanine.forms.fields import EMAIL
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
        # Use the QuerySet to get around the forced site filter when using the CurrentSiteManager
        copied = QuerySet(original.__class__).filter(slug=original.slug, site=site)
        self.assertTrue(copied.exists())
        self.assertEqual(copied.count(), 1)
        self.assertTrue(copied.exists())
        copy = copied[0]
        self.assertNotEqual(copy.pk, original.pk)

    def test_copy_default_minimal(self):
        """Copy all CMS models from the default site (minimal example)."""
        # This will be created with the default site
        # TODO: .create fails somehow related to django-concurrency
        page = RichTextPage(title='Learn', content='<h1>Title</h1>')
        page.save()
        site = Site.objects.create(name='zh-cn', domain='example.com')
        models.build_site_content(site)
        self.assertCopied(page, site)

    def test_copy_multiple_models(self):
        """CMS Pages, RichTextPage, Links should all be copied."""
        # TODO: .create fails somehow related to django-concurrency
        page = RichTextPage(title='Learn', content='<h1>Title</h1>')
        page.save()
        link = Link.objects.create(title='External Link')
        site = Site.objects.create(name='zh-cn', domain='example.com')
        models.build_site_content(site)
        self.assertCopied(page, site)
        self.assertCopied(link, site)

    def test_copy_forms(self):
        """Forms and their fields should be copied."""
        # TODO: .create fails somehow related to django-concurrency
        form = Form(title='Contact Us')
        form.save()
        form.fields.create(label='Email', field_type=EMAIL)
        site = Site.objects.create(name='zh-cn', domain='example.com')
        models.build_site_content(site)
        self.assertCopied(form, site)
        copy = QuerySet(Form).get(slug=form.slug, site=site)
        self.assertEqual(copy.fields.count(), 1)

    def test_nested_pages(self):
        """Page hierarchy should be preserved on copy."""
        # TODO: .create fails somehow related to django-concurrency
        page = RichTextPage(title='Learn', content='<h1>Title</h1>')
        page.save()
        subpage = RichTextPage(title='Sub Learn', content='<h1>Title</h1>', parent=page)
        subpage.save()
        site = Site.objects.create(name='zh-cn', domain='example.com')
        models.build_site_content(site)
        self.assertCopied(page, site)
        self.assertCopied(subpage, site)
        copy = QuerySet(RichTextPage).get(slug=page.slug, site=site)
        subcopy = QuerySet(RichTextPage).get(slug=subpage.slug, site=site)
        self.assertEqual(subcopy.parent_id, copy.pk)

    def test_nested_forms_links(self):
        """Page hierarchy for forms and links should be preserved on copy."""
        # TODO: .create fails somehow related to django-concurrency
        page = RichTextPage(title='Learn', content='<h1>Title</h1>')
        page.save()
        form = Form(title='Contact Us', parent=page)
        form.save()
        link = Link(title='Foo', parent=page)
        link.save()
        site = Site.objects.create(name='zh-cn', domain='example.com')
        models.build_site_content(site)
        self.assertCopied(page, site)
        self.assertCopied(form, site)
        self.assertCopied(link, site)
        copy = QuerySet(RichTextPage).get(slug=page.slug, site=site)
        formcopy = QuerySet(Form).get(slug=form.slug, site=site)
        linkcopy = QuerySet(Link).get(slug=link.slug, site=site)
        self.assertEqual(formcopy.parent_id, copy.pk)
        self.assertEqual(linkcopy.parent_id, copy.pk)

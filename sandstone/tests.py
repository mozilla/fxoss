from concurrency.utils import ConcurrencyTestMixin

from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase
from django.test.client import RequestFactory

import mezzanine.core.request
from mezzanine.forms.models import Form
from mezzanine.pages.models import RichTextPage, Link

from .admin import SandstoneRichTextPageAdmin, SandstoneFormAdmin, SandstoneLinkAdmin


class RichTextPageLockTestCase(ConcurrencyTestMixin, TestCase):
    concurrency_model = RichTextPage
    concurrency_kwargs = {
        'title': 'test',
        'content': 'Foo',
    }

    def setUp(self):
        self.obj = self.concurrency_model(**self.concurrency_kwargs)
        self.obj.save()


class FormLockTestCase(RichTextPageLockTestCase):
    concurrency_model = Form


class AdminTestMixin(object):
    """Helpers for testing admin ustomizations."""

    admin_class = None
    model_class = None
    model_defaults = {}
    expected_base_template = 'admin/change_form.html'

    def setUp(self):
        super(AdminTestMixin, self).setUp()
        self.factory = RequestFactory()
        self.request = self.factory.get('/admin/')
        # Fake the sesssion middleware
        self.request.session = {}
        self.user = get_user_model()(username='staff', is_staff=True, is_superuser=True)
        self.user.save()
        # Fake the authentication middleware
        self.request.user = self.user
        self.admin = self.admin_class(self.model_class, admin.site)

        # Temporarily replace mezzanine's thread local request with our fake
        # after saving the original for restoring during tearDown
        self.unfaked_request = mezzanine.core.request._thread_local.request
        mezzanine.core.request._thread_local.request = self.request

    def tearDown(self):
        # we must restore the original or tests in other threads can break
        mezzanine.core.request._thread_local.request = self.unfaked_request

    def create_model(self, **kwargs):
        values = self.model_defaults.copy()
        values.update(kwargs)
        instance = self.model_class(**values)
        instance.save()
        return instance

    def create_new_site(self, **kwargs):
        defaults = {
            'name': 'test site',
            'domain': 'example.com'
        }
        defaults.update(kwargs)
        return Site.objects.create(**defaults)

    def test_change_form_default_site(self):
        """Rending the change form on the default site should use the default template."""
        instance = self.create_model()
        response = self.admin.change_view(self.request, str(instance.pk))
        # Default admin template discovery
        meta = self.model_class._meta
        expected = [
            'admin/%s/%s/change_form.html' % (meta.app_label, meta.model_name),
            'admin/%s/change_form.html' % meta.app_label,
            'admin/change_form.html'
        ]
        self.assertEqual(response.template_name, expected)
        self.assertNotIn('default_language_url', response.context_data)
        self.assertNotIn('tranlsated_fields', response.context_data)

    def test_change_form_translated_site(self):
        """Rending the change form on the non-default site should link back to the original page."""
        original = self.create_model()
        site = self.create_new_site()
        # Create an instance on a non-default site
        with self.settings(SITE_ID=site.pk):
            instance = self.create_model(slug=original.slug)
        # Fake the locale site middleware
        self.request.site_id = site.pk
        response = self.admin.change_view(self.request, str(instance.pk))
        self.assertEqual(response.template_name, 'translations/admin/change_form.html')
        expected_url_name = admin_urlname(self.model_class._meta, 'change')
        expected_url = reverse(expected_url_name, args=(original.id, ))
        self.assertEqual(response.context_data['default_language_url'], expected_url)
        self.assertEqual(response.context_data['tranlsated_fields'], self.admin.tranlsated_fields)
        self.assertEqual(response.context_data['base_template'], self.expected_base_template)

    def test_change_form_default_not_found(self):
        """Handle the non-default site when the original page isn't found."""
        site = self.create_new_site()
        # Create an instance on a non-default site
        with self.settings(SITE_ID=site.pk):
            instance = self.create_model()
        # Fake the locale site middleware
        self.request.site_id = site.pk
        response = self.admin.change_view(self.request, str(instance.pk))
        self.assertEqual(response.template_name, 'translations/admin/change_form.html')
        self.assertIsNone(response.context_data['default_language_url'])
        self.assertEqual(response.context_data['base_template'], self.expected_base_template)


class RichTextPageAdminTestCase(AdminTestMixin, TestCase):
    """Customizations to editing RichTextPages in the admin."""

    admin_class = SandstoneRichTextPageAdmin
    model_class = RichTextPage
    model_defaults = {
        'title': 'test',
        'content': 'test',
    }


class FormAdminTestCase(AdminTestMixin, TestCase):
    """Customizations to editing Forms in the admin."""

    admin_class = SandstoneFormAdmin
    model_class = Form
    model_defaults = {
        'title': 'test',
        'content': 'test',
    }
    expected_base_template = 'admin/forms/change_form.html'


class LinkAdminTestCase(AdminTestMixin, TestCase):
    """Customizations to editing Links in the admin."""

    admin_class = SandstoneLinkAdmin
    model_class = Link
    model_defaults = {
        'title': 'test',
    }
    expected_base_template = 'admin/pages/link/change_form.html'

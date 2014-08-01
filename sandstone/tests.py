from concurrency.utils import ConcurrencyTestMixin

from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

import mezzanine.core.request
from mezzanine.forms.models import Form
from mezzanine.pages.models import RichTextPage, Link
from mock import Mock

from translations.models import TODOItem
from translations.utils import build_site_for_language

from .admin import SandstoneRichTextPageAdmin, SandstoneFormAdmin, SandstoneLinkAdmin
from .middleware import SetJustLoggedInCookieMiddleware

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
        self.other = build_site_for_language('zh-cn', copy_content=False)

        # Temporarily replace mezzanine's thread local request with our fake
        # after saving the original for restoring during tearDown
        self.unfaked_request = getattr(mezzanine.core.request._thread_local, 'request', None)
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
        # Create an instance on a non-default site
        with self.settings(SITE_ID=self.other.pk):
            instance = self.create_model(slug=original.slug)
        # Fake the locale site middleware
        self.request.site_id = self.other.pk
        response = self.admin.change_view(self.request, str(instance.pk))
        self.assertEqual(response.template_name, 'translations/admin/change_form.html')
        expected_url_name = admin_urlname(self.model_class._meta, 'change')
        expected_url = reverse(expected_url_name, args=(original.id, ))
        self.assertEqual(response.context_data['default_language_url'], expected_url)
        self.assertEqual(response.context_data['tranlsated_fields'], self.admin.tranlsated_fields)
        self.assertEqual(response.context_data['base_template'], self.expected_base_template)

    def test_change_form_default_not_found(self):
        """Handle the non-default site when the original page isn't found."""
        # Create an instance on a non-default site
        with self.settings(SITE_ID=self.other.pk):
            instance = self.create_model()
        # Fake the locale site middleware
        self.request.site_id = self.other.pk
        response = self.admin.change_view(self.request, str(instance.pk))
        self.assertEqual(response.template_name, 'translations/admin/change_form.html')
        self.assertIsNone(response.context_data['default_language_url'])
        self.assertEqual(response.context_data['base_template'], self.expected_base_template)

    def test_create_default_version(self):
        """Creating a new item on the default will create TODO items for other language sites."""
        instance = self.model_class(**self.model_defaults)
        form = self.admin.get_form(self.request)(instance=instance)
        self.admin.save_model(self.request, instance, form, False)
        todos = TODOItem.objects.all()
        self.assertEqual(len(todos), 1)
        todo = todos[0]
        self.assertEqual(todo.title, instance.title)
        self.assertEqual(todo.slug, instance.slug)
        self.assertEqual(todo.site, self.other)
        self.assertEqual(todo.action, TODOItem.ACTION_CREATE)
        self.assertEqual(todo.editor, self.user)

    def test_create_translated_version(self):
        """Creating a new item on a translation site does not create TODO items."""
        instance = self.model_class( **self.model_defaults)
        form = self.admin.get_form(self.request)(instance=instance)
        # Fake the locale site middleware
        self.request.site_id = self.other.pk
        self.admin.save_model(self.request, instance, form, False)
        todos = TODOItem.objects.all()
        self.assertEqual(len(todos), 0)

    def test_edit_default_version(self):
        """Edits to an item on the default will create TODO items for other language sites."""
        instance = self.create_model()
        with self.settings(SITE_ID=self.other.pk):
            translated = self.create_model(slug=instance.slug)
        form = self.admin.get_form(self.request)(instance=instance)
        # Fake a change to the title
        form._changed_data = ['title', ]
        # Handle Mezzinine slug tracking
        instance._old_slug = instance.slug
        self.admin.save_model(self.request, instance, form, True)
        todos = TODOItem.objects.all()
        self.assertEqual(len(todos), 1)
        todo = todos[0]
        self.assertEqual(todo.title, instance.title)
        self.assertEqual(todo.slug, instance.slug)
        self.assertEqual(todo.page.pk, translated.page_ptr_id)
        self.assertEqual(todo.site, self.other)
        self.assertEqual(todo.action, TODOItem.ACTION_EDIT)
        self.assertEqual(todo.editor, self.user)

    def test_multiple_edits(self):
        """Multiple edits in a row should only create one TODO."""
        instance = self.create_model()
        with self.settings(SITE_ID=self.other.pk):
            translated = self.create_model(slug=instance.slug)
        form = self.admin.get_form(self.request)(instance=instance)
        # Fake a change to the title
        form._changed_data = ['title', ]
        # Handle Mezzinine slug tracking
        instance._old_slug = instance.slug
        self.admin.save_model(self.request, instance, form, True)
        todos = TODOItem.objects.all()
        self.assertEqual(len(todos), 1)
        todo = todos[0]
        self.assertEqual(todo.action, TODOItem.ACTION_EDIT)
        self.assertIn('title', todo.description)
        # Fake another edit
        if 'content' in self.admin.tranlsated_fields:
            form._changed_data = ['content', ]
        else:
            form._changed_data = ['title', ]
        self.admin.save_model(self.request, instance, form, True)
        todos = TODOItem.objects.all()
        self.assertEqual(len(todos), 1)
        todo = todos[0]
        self.assertEqual(todo.action, TODOItem.ACTION_EDIT)
        self.assertIn('title', todo.description)
        if 'content' in self.admin.tranlsated_fields:
            self.assertIn('content', todo.description)

    def test_edit_translated_version(self):
        """Edits to an item on a translation site does not create TODO items."""
        instance = self.create_model()
        with self.settings(SITE_ID=self.other.pk):
            translated = self.create_model(slug=instance.slug)
        form = self.admin.get_form(self.request)(instance=instance)
        # Fake a change to the title
        form._changed_data = ['title', ]
        # Fake the locale site middleware
        self.request.site_id = self.other.pk
        # Handle Mezzinine slug tracking
        translated._old_slug = translated.slug
        self.admin.save_model(self.request, translated, form, True)
        todos = TODOItem.objects.all()
        self.assertEqual(len(todos), 0)

    def test_delete_default_version(self):
        """Deleted an item on the default will create TODO items for other language sites."""
        instance = self.create_model()
        with self.settings(SITE_ID=self.other.pk):
            translated = self.create_model(slug=instance.slug)
        self.admin.delete_model(self.request, instance)
        todos = TODOItem.objects.all()
        self.assertEqual(len(todos), 1)
        todo = todos[0]
        self.assertEqual(todo.title, instance.title)
        self.assertEqual(todo.slug, instance.slug)
        self.assertEqual(todo.page.pk, translated.page_ptr_id)
        self.assertEqual(todo.site, self.other)
        self.assertEqual(todo.action, TODOItem.ACTION_DELETE)
        self.assertEqual(todo.editor, self.user)

    def test_delete_translated_version(self):
        """Deleted an item on a translation site does not create TODO items."""
        instance = self.create_model()
        with self.settings(SITE_ID=self.other.pk):
            translated = self.create_model(slug=instance.slug)
        # Fake the locale site middleware
        self.request.site_id = self.other.pk
        self.admin.delete_model(self.request, translated)
        todos = TODOItem.objects.all()
        self.assertEqual(len(todos), 0)

    def test_delete_with_outstanding_create(self):
        """Deleting a page which wasn't created for the other site should resolve
        the create TODO."""
        instance = self.model_class(**self.model_defaults)
        form = self.admin.get_form(self.request)(instance=instance)
        self.admin.save_model(self.request, instance, form, False)
        todos = TODOItem.objects.all()
        self.assertEqual(len(todos), 1)
        todo = todos[0]
        self.assertEqual(todo.action, TODOItem.ACTION_CREATE)
        self.assertIsNone(todo.resolved_by)
        # Delete the newly created model
        self.admin.delete_model(self.request, instance)
        todos = TODOItem.objects.all()
        self.assertEqual(len(todos), 1)
        todo = todos[0]
        self.assertEqual(todo.action, TODOItem.ACTION_CREATE)
        self.assertEqual(todo.resolved_by, self.user)

    def test_delete_with_outstanding_edits(self):
        """Deleting a page with existing edit TODOs should resolve the TODOS."""
        instance = self.create_model()
        with self.settings(SITE_ID=self.other.pk):
            translated = self.create_model(slug=instance.slug)
        form = self.admin.get_form(self.request)(instance=instance)
        # Fake a change to the title
        form._changed_data = ['title', ]
        # Fake the locale site middleware
        self.request.site_id = self.other.pk
        # Handle Mezzinine slug tracking
        instance._old_slug = instance.slug
        self.admin.save_model(self.request, instance, form, True)
        todos = TODOItem.objects.all()
        self.assertEqual(len(todos), 1)
        todo = todos[0]
        self.assertEqual(todo.action, TODOItem.ACTION_EDIT)
        self.assertIsNone(todo.resolved_by)
        # Delete the page
        self.admin.delete_model(self.request, instance)
        todos = TODOItem.objects.all().order_by('created')
        self.assertEqual(len(todos), 2)
        edit_todo = todos[0]
        self.assertEqual(edit_todo.action, TODOItem.ACTION_EDIT)
        self.assertEqual(edit_todo.resolved_by, self.user)
        delete_todo = todos[1]
        self.assertEqual(delete_todo.action, TODOItem.ACTION_DELETE)
        self.assertIsNone(delete_todo.resolved_by)


TEST_LANGUAGES = (
    ('en', 'English'),
    ('zh-cn', 'Simplified Chinese'),
)


@override_settings(LANGUAGES=TEST_LANGUAGES, LANGUAGE_CODE='en')
class RichTextPageAdminTestCase(AdminTestMixin, TestCase):
    """Customizations to editing RichTextPages in the admin."""

    admin_class = SandstoneRichTextPageAdmin
    model_class = RichTextPage
    model_defaults = {
        'title': 'test',
        'content': 'test',
    }


@override_settings(LANGUAGES=TEST_LANGUAGES, LANGUAGE_CODE='en')
class FormAdminTestCase(AdminTestMixin, TestCase):
    """Customizations to editing Forms in the admin."""

    admin_class = SandstoneFormAdmin
    model_class = Form
    model_defaults = {
        'title': 'test',
        'content': 'test',
    }
    expected_base_template = 'admin/forms/change_form.html'


@override_settings(LANGUAGES=TEST_LANGUAGES, LANGUAGE_CODE='en')
class LinkAdminTestCase(AdminTestMixin, TestCase):
    """Customizations to editing Links in the admin."""

    admin_class = SandstoneLinkAdmin
    model_class = Link
    model_defaults = {
        'title': 'test',
    }
    expected_base_template = 'admin/pages/link/change_form.html'


class SetJustLoggedInMiddlewareTestCase(TestCase):
    def setUp(self):
        self.middleware = SetJustLoggedInCookieMiddleware()

    def test_no_just_logged_in(self):
        """
        If the just_logged_in flag isn't set, don't set the cookie.
        """
        request, response = Mock(), Mock()
        del request.just_logged_in
        self.middleware.process_response(request, response)
        self.assertFalse(response.set_cookie.called)

    def test_just_logged_in(self):
        """
        If the just_logged_in flag is set, set the cookie.
        """
        request, response = Mock(just_logged_in=True), Mock()
        self.middleware.process_response(request, response)
        response.set_cookie.assert_called_with('just_logged_in', 'true', httponly=False)

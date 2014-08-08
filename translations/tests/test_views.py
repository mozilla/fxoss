from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase


class ViewOnSiteShortcutTestCase(TestCase):
    """Customized view on site shortcut for the admin."""

    def setUp(self):
        self.user = User.objects.create_user('staff', '', 'test')
        self.user.is_staff = True
        self.user.save()
        self.ct = ContentType.objects.get_for_model(self.user)
        self.client.login(username='staff', password='test')

    def test_get_shortcut(self):
        """Redirect to the object's get_absolute_url."""
        url = reverse('view_on_site', kwargs={
            'content_type_id': self.ct.id, 'object_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/users/staff/')

    def test_unknown_object(self):
        """Handle invalid object PK."""
        url = reverse('view_on_site', kwargs={
            'content_type_id': self.ct.id, 'object_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_unknown_content_type(self):
        """Handle invalid content type PK."""
        url = reverse('view_on_site', kwargs={
            'content_type_id': 0, 'object_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_no_url(self):
        """Handle a model which doesn't have a get_absolute_url."""
        site = Site.objects.get_current()
        ct = ContentType.objects.get_for_model(site)
        url = reverse('view_on_site', kwargs={
            'content_type_id': ct.id, 'object_id': site.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

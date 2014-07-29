import csv
from datetime import datetime
from urllib import urlencode

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings
from django.utils import timezone
from django.utils.translation import activate

from mock import Mock, patch

from .models import Agreement, SignedAgreement
from .views import export_csv, export_signedagreement_csv


User = get_user_model()


class AgreementMixin(object):
    """Base setup and helpers for testing user agreement related views."""

    def setUp(self):
        activate('en')
        self.agreement = Agreement.objects.create(
            version='v1.0', agreement_pdf='blah.pdf')
        self.agreement_url = reverse('protected_assets.sign_agreement')
        self.asset_url = reverse(
            'protected_assets.views.protected_download', args=['test.png', ])
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

    def create_signed_agreement(self, **kwargs):
        """Create a signed agreement."""
        defaults = {
            'ip': '127.0.0.1',
            'agreement': self.agreement,
        }
        defaults.update(kwargs)
        if 'user' not in defaults:
            defaults['user'] = self.create_user()
        return SignedAgreement.objects.create(**defaults)


@override_settings(DOWNLOAD_AGREEMENT_VERSION='v1.0')
class ProtectAssetTestCase(AgreementMixin, TestCase):
    """Integration test for attempting to download a protected asset."""

    def test_agreement_redirect(self):
        """
        If user has not signed the agreement they should be redirected to sign.
        """
        response = self.client.get(self.asset_url)
        expected_url = '?'.join(
            [self.agreement_url, urlencode({'next': self.asset_url})])
        self.assertRedirects(response, expected_url)

    def test_already_signed(self):
        """
        Download should be trigged if the agreement was previously signed.
        """
        self.create_signed_agreement(user=self.user)
        response = self.client.get(self.asset_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Disposition'], 'attachment; filename=test.png')
        self.assertEqual(
            response['X-Accel-Redirect'], '/__protected__/test.png')

    def test_signed_old_version(self):
        """
        User will need to resign the agreement if they signed an older version.
        """
        old_agreement = Agreement.objects.create(
            version='v0.9', agreement_pdf='blah.pdf')
        self.create_signed_agreement(user=self.user, agreement=old_agreement)
        response = self.client.get(self.asset_url)
        expected_url = '?'.join(
            [self.agreement_url, urlencode({'next': self.asset_url})])
        self.assertRedirects(response, expected_url)

    def test_return_to_referring_page(self):
        """Redirect to the original page after signing the user agreement."""
        response = self.client.get(self.asset_url, HTTP_REFERER='/')
        expected_url = '%s?%s' % (self.agreement_url, urlencode({'next': '/'}))
        self.assertRedirects(response, expected_url)
        self.assertEqual(
            self.client.session['waiting_download'], self.asset_url)


@override_settings(DOWNLOAD_AGREEMENT_VERSION='v1.0')
class SignAgreementTestCase(AgreementMixin, TestCase):
    """Integration test for signing the user agreement."""

    def test_agree_to_terms(self):
        """Create Agreement record when user signs the form."""
        response = self.client.post(self.agreement_url, data={'agree': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], 'http://testserver/')
        self.assertTrue(
            SignedAgreement.objects.filter(user=self.user).exists())

    def test_did_not_agree(self):
        """No record should be created if they didn't agree."""
        response = self.client.post(self.agreement_url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            SignedAgreement.objects.filter(user=self.user).exists())

    def test_next_redirect(self):
        """Redirect user to custom location."""
        next_url = self.asset_url
        url = '%s?next=%s' % (self.agreement_url, self.asset_url)
        response = self.client.post(url, data={'agree': 'on'})
        self.assertRedirects(response, next_url)
        self.assertTrue(
            SignedAgreement.objects.filter(user=self.user).exists())

    def test_mark_download_as_ready(self):
        """
        If download is waiting in the session it should be marked as ready.
        """
        session = self.client.session
        session['waiting_download'] = self.asset_url
        session.save()
        response = self.client.post(self.agreement_url, data={'agree': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], 'http://testserver/')
        self.assertNotIn('waiting_download', self.client.session)
        self.assertEqual(self.client.session['ready_download'], self.asset_url)

    def test_process_request_with_cluster_client_ip(self):
        """Check IP of agreement with X-Cluster_Client_IP header."""
        self.client.post(
            self.agreement_url, data={'agree': 'on'},
            HTTP_X_CLUSTER_CLIENT_IP='1.1.1.1')
        agreement = SignedAgreement.objects.get(user=self.user)
        self.assertEqual('1.1.1.1', agreement.ip)

    def test_process_request_with_proxy(self):
        """Check IP of agreement with a single proxy in place."""
        self.client.post(
            self.agreement_url, data={'agree': 'on'},
            HTTP_X_FORWARDED_FOR='1.1.1.1')
        agreement = SignedAgreement.objects.get(user=self.user)
        self.assertEqual('1.1.1.1', agreement.ip)

    def test_process_request_with_multiple_proxies(self):
        """Check IP of agreement with multiple proxies in place."""
        self.client.post(
            self.agreement_url, data={'agree': 'on'},
            HTTP_X_FORWARDED_FOR='1.1.1.1, 2.2.2.2, 3.3.3.3')
        agreement = SignedAgreement.objects.get(user=self.user)
        self.assertEqual('1.1.1.1', agreement.ip)

    def test_no_existing_agreement_404(self):
        """If no agreement can be found, return a 404."""
        with self.settings(DOWNLOAD_AGREEMENT_VERSION='vX.X'):
            response = self.client.get(self.agreement_url)
            self.assertEqual(response.status_code, 404)


def aware_datetime(*args, **kwargs):
    dt = datetime(*args, **kwargs)
    return timezone.make_aware(dt, timezone.utc)


class TestExportCSV(TestCase):
    def test_export_csv(self):
        User.objects.create_user('lloyd', 'lloyd@example.com')
        User.objects.create_user('kratos', 'kratos@example.com')

        def generate_row(user):
            return (user.username, user.email)

        with patch('protected_assets.views.timezone') as mock_timezone:
            mock_timezone.now.return_value = aware_datetime(
                2014, 4, 1, 6, 5, 4)
            response = export_csv(
                User.objects.order_by('id'), ('username', 'email'),
                generate_row)

        # We're kind've testing strftime below, but the bug required the
        # CSV to match what the admin interface shows, so we want to
        # make sure it matches pretty closely, including the formatting
        # of dates.
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response['Content-Disposition'],
                         'attachment; filename=user_2014_04_01_06:05:04.csv')
        self.assertEqual(response['Cache-Control'], 'no-cache')

        reader = csv.reader(response)
        rows = list(reader)

        # Initial empty row shows up in the tests, but when I read the
        # CSV with LibreOffice or a text editor it doesn't exist, so
        # whatever.
        self.assertEqual(rows, [
            [],
            ['username', 'email'],
            ['lloyd', 'lloyd@example.com'],
            ['kratos', 'kratos@example.com'],
        ])


class TestExportSignedAgreementCSV(TestCase):
    @patch('protected_assets.views.SignedAgreement')
    def test_exportsignedagreement_csv(self, mock_signed_agreement_class):
        sa = Mock()
        sa.user.__unicode__ = lambda self: u'b\xf6rk'
        sa.user.profile.legal_entity = u'b\xf6rk b\xf6rk'
        MockQS = type('MockQuerySet', (list,), {'model': Mock()})
        mock_signed_agreement_class.objects.all.return_value = MockQS([sa])

        response = export_signedagreement_csv('request')
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response['Cache-Control'], 'no-cache')

        self.assertEqual(
            # csv.reader in python 2 does not properly handle unicode, so
            # we have to wrap it or we get encoding errors :(
            [[unicode(cell, 'utf-8') for cell in line]
             for line in csv.reader(response)], [
            [],
            [u'username', u'legal entity', u'timestamp', u'agreement', u'ip'],
            [u'b\xf6rk', u'b\xf6rk b\xf6rk',
             unicode(sa.timestamp.strftime.return_value),
             unicode(sa.agreement), unicode(sa.ip)],
        ])

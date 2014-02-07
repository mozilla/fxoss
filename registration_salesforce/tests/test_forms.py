from django.contrib.auth.models import User
from django.test import TestCase

from ..forms import UserRegistrationLeadForm


class UserRegistrationLeadFormTestCase(TestCase):

    def setUp(self):
        self.data = dict(
            first_name="Test",
            last_name="User",
            email="test@user.com",
            password1='asdfasdf',
            password2='asdfasdf',
            lead_source='mobilepartners.mozilla.org'
            )

    def test_valid_form(self):
        form = UserRegistrationLeadForm(self.data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = UserRegistrationLeadForm()
        self.assertFalse(form.is_valid())

    def test_clean_password1(self):
        self.data['password2'] = 'foobar'
        form = UserRegistrationLeadForm(self.data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)

    def test_clean_email(self):
        User.objects.create_user("Test", email="test@user.com")
        form = UserRegistrationLeadForm(self.data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


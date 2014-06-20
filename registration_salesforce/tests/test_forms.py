from django.test import TestCase

from ..forms import UserRegistrationLeadForm


class UserRegistrationLeadFormTestCase(TestCase):

    def test_valid_form(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@user.com',
            'password1': 'asdfasdf',
            'password2': 'asdfasdf',
            'legal_entity': 'test entity',
            'company': 'testco',
            'street': 'test st',
            'city': 'testville',
            'country': 'no for old men'}
        form = UserRegistrationLeadForm(data)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = UserRegistrationLeadForm({})
        self.assertFalse(form.is_valid())

    def test_required_fields(self):
        form = UserRegistrationLeadForm()
        self.assertEqual(
            form.Meta.required_fields,
            ('first_name', 'last_name', 'email', 'legal_entity', 'company',
             'street', 'city', 'country'))
        for field in form.Meta.required_fields:
            self.assertTrue(form.fields[field].required)
            self.assertEqual(form.fields[field].widget.attrs['class'],
                             'required')
            self.assertEqual(form.fields[field].widget.attrs['required'],
                             'required')
            self.assertEqual(form.fields[field].widget.attrs['aria-required'],
                             'true')

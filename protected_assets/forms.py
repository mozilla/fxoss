from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _


class AgreementForm(forms.Form):

    agree = forms.BooleanField(label=_('I agree to the licensing terms.'))

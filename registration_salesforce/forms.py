from datetime import datetime
from random import randrange

from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from mezzanine.accounts.forms import ProfileForm
from mezzanine.utils.models import get_user_model

from .models import Profile


User = get_user_model()


class HoneyPotWidget(widgets.CheckboxInput):
    """
    Render a checkbox to (hopefully) trick bots. Will be used on many pages.
    """

    def render(self, name, value, attrs=None):
        honeypot_txt = _(u'Check this box if you are not human.')
        # semi-randomized in case we have more than one per page.
        # this is maybe/probably overthought
        honeypot_id = 'super-priority-{}-{}'.format(
            str(randrange(1001)),
            str(datetime.now().strftime("%Y%m%d%H%M%S%f")))
        return mark_safe(
            '<div class="super-priority-field">'
            '<label for="%s" class="super-priority-check-label">%s</label>'
            '<input type="checkbox" name="superpriority" id="%s">'
            '</div>' % (honeypot_id, honeypot_txt, honeypot_id))


class UserRegistrationLeadForm(ProfileForm):
    """
    ModelForm for auth.User - used for signup and profile update.
    """
    superpriority = forms.BooleanField(required=False, widget=HoneyPotWidget)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        required_fields = ('first_name', 'last_name', 'email', 'legal_entity',
                           'company', 'street', 'city', 'country')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationLeadForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field in self.Meta.required_fields:
                self.fields[field].required = True
                self.fields[field].widget.attrs.update(
                    {'class': 'required',
                     'required': 'required',
                     'aria-required': 'true'})
            self.fields[field].widget.attrs['placeholder'] = (
                self.fields[field].label)

from datetime import datetime
from random import randrange

from django import forms
from django.forms import widgets
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from mezzanine.conf import settings
from mezzanine.core.forms import Html5Mixin
from mezzanine.utils.models import get_user_model
from mezzanine.utils.urls import slugify, unique_slug

from .models import Profile


User = get_user_model()


def create_or_update_profile(user, data):
    profile_kwargs = {field.name: data[field.name]
                      for field in Profile._meta.fields
                      if data.get(field.name)}

    if not Profile.objects.filter(user=user).update(**profile_kwargs):
        Profile.objects.create(user=user, **profile_kwargs)


class HoneyPotWidget(widgets.CheckboxInput):
    """Render a checkbox to (hopefully) trick bots. Will be used on many pages."""

    def render(self, name, value, attrs=None):
        honeypot_txt = _(u'Check this box if you are not human.')
        # semi-randomized in case we have more than one per page.
        # this is maybe/probably overthought
        honeypot_id = 'super-priority-%s-%s' % (str(randrange(1001)), str(datetime.now().strftime("%Y%m%d%H%M%S%f")))
        return mark_safe(
            '<div class="super-priority-field">'
            '<label for="%s" class="super-priority-check-label">%s</label>'
            '<input type="checkbox" name="superpriority" id="%s">'
            '</div>' % (honeypot_id, honeypot_txt, honeypot_id))


class UserRegistrationLeadForm(Html5Mixin, forms.ModelForm):
    """
    ModelForm for auth.User - used for signup and profile update.

    NOTE: Profile Model field injection as defined by ``AUTH_PROFILE_MODULE``
    is disabled in this implementation!
    """

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_("Password (again)"),
                                widget=forms.PasswordInput(render_value=False))
    first_name = forms.CharField(
        max_length=40,
        required=True,
        error_messages={
            'required': _('Please enter your first name.')
        },
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _('First Name'),
                'class': 'required',
                'required': 'required',
                'aria-required': 'true'
            }
        )
    )
    last_name = forms.CharField(
        max_length=80,
        required=True,
        error_messages={
            'required': _('Please enter your last name.')
        },
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _('Last Name'),
                'class': 'required',
                'required': 'required',
                'aria-required': 'true'
            }
        )
    )

    title = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _('Title')
            }
        )
    )
    company = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _('Company'),
            }
        )
    )
    email = forms.EmailField(
        max_length=80,
        required=True,
        error_messages={
            'required': _('Please enter your email address.'),
            'invalid': _('Please enter a valid email address')
        },
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _('Email'),
                'class': 'required',
                'required': 'required',
                'aria-required': 'true'
            }
        )
    )
    phone = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _('Phone')
            }
        )
    )
    mobile = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _('Mobile')
            }
        )
    )
    city = forms.CharField(
        required=False,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('City')
            }
        )
    )
    state = forms.CharField(
        required=False,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('State/Province')
            }
        )
    )
    country = forms.CharField(
        required=False,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Country')
            }
        )
    )

    industry = forms.ChoiceField(
        required=False,
        choices=Profile.INDUSTRY_CHOICES
    )

    type_of_device = forms.MultipleChoiceField(
        required=False,
        choices=Profile.DEVICE_CHOICES
    )

    mobile_product_interest = forms.MultipleChoiceField(
        required=False,
        choices=Profile.INTEREST_CHOICES
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': _('Description'),
                'rows': '',
                'cols': ''
            }
        )
    )

    lead_source = forms.CharField(
        initial="mobilepartners.mozilla.org",
        max_length=26,
        widget=forms.HiddenInput()
    )

    superpriority = forms.BooleanField(widget=HoneyPotWidget, required=False)
    if settings.DEBUG_SALESFORCE:
        debug = forms.IntegerField(
            required=False,
            help_text=_("set DEBUG_SALESFORCE=False to remove this field")
        )
        debugEmail = forms.EmailField(
            required=False,
            help_text=_("set DEBUG_SALESFORCE=False to remove this field")
        )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super(UserRegistrationLeadForm, self).__init__(*args, **kwargs)

        self._signup = self.instance.id is None
        user_fields = User._meta.get_all_field_names()
        try:
            self.fields["username"].help_text = _(
                        "Only letters, numbers, dashes or underscores please")
        except KeyError:
            pass
        for field in self.fields:
            # Make user fields required.
            if field in user_fields:
                self.fields[field].required = True
            # Disable auto-complete for password fields.
            # Password isn't required for profile update.
            if field.startswith("password"):
                self.fields[field].widget.attrs["autocomplete"] = "off"
                self.fields[field].widget.attrs.pop("required", "")
                if not self._signup:
                    self.fields[field].required = False
                    if field == "password1":
                        self.fields[field].help_text = _(
                        "Leave blank unless you want to change your password")

    def clean_password2(self):
        """
        Ensure the password fields are equal, and match the minimum
        length defined by ``ACCOUNTS_MIN_PASSWORD_LENGTH``.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1:
            errors = []
            if password1 != password2:
                errors.append(_("Passwords do not match"))
            if len(password1) < settings.ACCOUNTS_MIN_PASSWORD_LENGTH:
                errors.append(_("Password must be at least %s characters") %
                              settings.ACCOUNTS_MIN_PASSWORD_LENGTH)
            if errors:
                self._errors["password1"] = self.error_class(errors)
        return password2

    def clean_email(self):
        """
        Ensure the email address is not already registered.
        """
        email = self.cleaned_data.get("email")
        qs = User.objects.exclude(id=self.instance.id).filter(email=email)
        if not qs.exists():
            return email
        raise forms.ValidationError(_("This email is already registered"))

    def save(self, *args, **kwargs):
        """
        Create the new user. If no username is supplied (may be hidden
        via ``ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS`` or
        ``ACCOUNTS_NO_USERNAME``), we generate a unique username.
        """

        kwargs["commit"] = False
        user = super(UserRegistrationLeadForm, self).save(*args, **kwargs)
        try:
            self.cleaned_data["username"]
        except KeyError:
            if not self.instance.username:
                username = "%(first_name)s %(last_name)s" % self.cleaned_data
                if not username.strip():
                    username = self.cleaned_data["email"].split("@")[0]
                qs = User.objects.exclude(id=self.instance.id)
                user.username = unique_slug(qs, "username", slugify(username))
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        elif self._signup:
            try:
                user.set_unusable_password()
            except AttributeError:
                # This could happen if using a custom user model that
                # doesn't inherit from Django's AbstractBaseUser.
                pass
        user.save()

        if self._signup:
            settings.use_editable()
            if (settings.ACCOUNTS_VERIFICATION_REQUIRED or
                    settings.ACCOUNTS_APPROVAL_REQUIRED):
                user.is_active = False
                user.save()
            else:
                token = default_token_generator.make_token(user)
                user = authenticate(uidb36=int_to_base36(user.id),
                                    token=token,
                                    is_active=True)

        create_or_update_profile(user, self.cleaned_data)
        return user

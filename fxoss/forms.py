from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36
from django.utils.translation import ugettext as _

from mezzanine.conf import settings
from mezzanine.core.forms import Html5Mixin
from mezzanine.utils.models import get_user_model
from mezzanine.utils.urls import slugify, unique_slug

User = get_user_model()


class WebToLeadForm(Html5Mixin, forms.ModelForm):
    """
    ModelForm for auth.User - used for signup and profile update.
    If a Profile model is defined via ``AUTH_PROFILE_MODULE``, its
    fields are injected into the form.
    """

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

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_("Password (again)"),
                                widget=forms.PasswordInput(render_value=False))


    interests_standard = (
        ('Firefox for Desktop', 'Firefox for Desktop'),
        ('Firefox for Android', 'Firefox for Android'),
        ('Firefox Marketplace', 'Firefox Marketplace'),
        ('Firefox OS', 'Firefox OS'),
        ('Persona', 'Persona'),
        ('Marketing and Co-promotions', 'Marketing and Co-promotions'),
        ('Other', 'Other'),
    )

    interests_fx = (
        ('Firefox for Android', 'Firefox for Android'),
        ('Firefox Marketplace', 'Firefox Marketplace'),
        ('Firefox OS', 'Firefox OS'),
        ('Other', 'Other'),
    )

    title = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': 'Title'
            }
        )
    )
    company = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': 'Company',
            }
        )
    )
    URL = forms.URLField(
        max_length=80,
        required=False,
        error_messages={
            'invalid': 'Please supply a valid URL.'
        },
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': 'Website'
            }
        )
    )
    email = forms.EmailField(
        max_length=80,
        required=True,
        error_messages={
            'required': 'Please enter your email address.',
            'invalid': 'Please enter a valid email address'
        },
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': 'Email',
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
                'placeholder': 'Phone'
            }
        )
    )
    mobile = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': 'Mobile'
            }
        )
    )
    street = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Address',
                'rows': '',
                'cols': ''
            }
        )
    )
    city = forms.CharField(
        required=False,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'City'
            }
        )
    )
    state = forms.CharField(
        required=False,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'State/Province'
            }
        )
    )
    country = forms.CharField(
        required=False,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Country'
            }
        )
    )
    zip = forms.CharField(
        required=False,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Zip'
            }
        )
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Description',
                'rows': '',
                'cols': ''
            }
        )
    )
    # uncomment below to debug salesforce
    # debug = forms.IntegerField(required=False)
    # debugEmail = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")

    def __init__(self, *args, **kwargs):
        interest_set = kwargs.pop('interest_set', 'standard')
        interest_choices = self.interests_fx if (interest_set == 'fx') else self.interests_standard

        super(WebToLeadForm, self).__init__(*args, **kwargs)

        self.fields['interest'] = forms.MultipleChoiceField(
            choices=interest_choices,
            required=False,
            widget=forms.SelectMultiple(
                attrs={
                    'title': 'Interest',
                    'size': 7
                }
            )
        )

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

    def clean_username(self):
        """
        Ensure the username doesn't exist or contain invalid chars.
        We limit it to slugifiable chars since it's used as the slug
        for the user's profile view.
        """
        username = self.cleaned_data.get("username")
        if username.lower() != slugify(username).lower():
            raise forms.ValidationError(_("Username can only contain letters, "
                                          "numbers, dashes or underscores."))
        lookup = {"username__iexact": username}
        try:
            User.objects.exclude(id=self.instance.id).get(**lookup)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("This username is already registered"))

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
        if len(qs) == 0:
            return email
        raise forms.ValidationError(_("This email is already registered"))

    def save(self, *args, **kwargs):
        """
        Create the new user. If no username is supplied (may be hidden
        via ``ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS`` or
        ``ACCOUNTS_NO_USERNAME``), we generate a unique username.
        """

        kwargs["commit"] = False
        user = super(WebToLeadForm, self).save(*args, **kwargs)
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
        return user


from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db import models
from mezzanine.forms.models import Form
from mezzanine.pages.models import Page
from mezzanine.pages.models import RichTextPage
from mezzanine.pages.models import Link
from concurrency.api import apply_concurrency_check
from concurrency.fields import IntegerVersionField

from django.utils.translation import ugettext_lazy as _


apply_concurrency_check(Form, 'version', IntegerVersionField)
apply_concurrency_check(RichTextPage, 'version', IntegerVersionField)


@receiver(user_logged_in)
def add_just_logged_in_cookie(**kwargs):
    """Mark the request that a user logged in with."""
    kwargs['request'].just_logged_in = True



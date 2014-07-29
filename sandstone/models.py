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



# Notes field extension considerations
# ====================================
# For the Notes section that is now part of the site admin pages, whenever a new
# langauge code is added, this data model will need to be extended adding a notes
# field to capture data for that language.

# Within this file you need to add the following field definition for each class below:

# notes_<LANGUAGE-CODE> = models.TextField(verbose_name=_('description'), default='', blank=True)

# You would replace <LANGUAGE-CODE> with the language code in question using
# underscores instead of dashes if present.

# Using the Brazilian language code as an example, the line would look like the
# following:

# notes_pt_br = models.TextField(verbose_name=_('description'), default='', blank=True)

# Next create a new template schema migration for the sandstone app:

# $:-> ./manage.py schemamigration sandstone --auto

# Finally perform the migration:

# $:-> ./manage.py migrate sandstone --delete-ghost-migrations

# After the migration, no further steps are needed as the custom template and
# filters used will handle the task of displaying the correct notes field for the
# chosen language.

class PageNotes(models.Model):
    page = models.OneToOneField(Page, editable=False, related_name='page_extra_fields')
    notes = models.TextField(verbose_name=_('description'), default='', blank=True)
    notes_zh_cn = models.TextField(verbose_name=_('description'), default='', blank=True)

class FormNotes(models.Model):
    page = models.OneToOneField(Form, editable=False, related_name='form_extra_fields')
    notes = models.TextField(verbose_name=_('description'), default='', blank=True)
    notes_zh_cn = models.TextField(verbose_name=_('description'), default='', blank=True)

class LinkNotes(models.Model):
    page = models.OneToOneField(Link, editable=False, related_name='link_extra_fields')
    notes = models.TextField(verbose_name=_('description'), default='', blank=True)
    notes_zh_cn = models.TextField(verbose_name=_('description'), default='', blank=True)


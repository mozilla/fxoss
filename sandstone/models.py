from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db import models
from mezzanine.forms.models import Form
from mezzanine.pages.models import Page
from mezzanine.pages.models import RichTextPage
from mezzanine.generic.models import ThreadedComment
from concurrency.api import apply_concurrency_check
from concurrency.fields import IntegerVersionField


apply_concurrency_check(Form, 'version', IntegerVersionField)
apply_concurrency_check(RichTextPage, 'version', IntegerVersionField)


@receiver(user_logged_in)
def add_just_logged_in_cookie(**kwargs):
    """Mark the request that a user logged in with."""
    kwargs['request'].just_logged_in = True


class PageNotes(models.Model):
    page = models.OneToOneField(Page, editable=False, related_name='page_extra_fields')
    notes = models.TextField(verbose_name='description', default='', blank=True)
    notes_zh_cn = models.TextField(verbose_name='description', default='', blank=True)

class FormNotes(models.Model):
    page = models.OneToOneField(Form, editable=False, related_name='form_extra_fields')
    notes = models.TextField(verbose_name='description', default='', blank=True)
    notes_zh_cn = models.TextField(verbose_name='description', default='', blank=True)

class ThreadedCommentNotes(models.Model):
    page = models.OneToOneField(ThreadedComment, editable=False, related_name='threaded_comment_extra_fields')
    notes = models.TextField(verbose_name='description', default='', blank=True)
    notes_zh_cn = models.TextField(verbose_name='description', default='', blank=True)

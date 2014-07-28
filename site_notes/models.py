from django.db import models
from django.contrib.sites.models import Site
from django.contrib.redirects.models import Redirect
from django.contrib.auth.models import Group

from django.utils.translation import ugettext_lazy as _

class SiteNotes(models.Model):   
    page = models.OneToOneField(Site, editable=False, related_name='extra_fields')
    notes = models.TextField(verbose_name=_('description'), default='', blank=True)
    notes_zh_cn = models.TextField(verbose_name=_('description'), default='', blank=True)

class RedirectNotes(models.Model):
    page = models.OneToOneField(Redirect, editable=False, related_name='extra_fields')
    notes = models.TextField(verbose_name=_('description'), default='', blank=True)
    notes_zh_cn = models.TextField(verbose_name=_('description'), default='', blank=True)

class GroupNotes(models.Model):
    page = models.OneToOneField(Group, editable=False, related_name='extra_fields')
    notes = models.TextField(verbose_name=_('description'), default='', blank=True)
    notes_zh_cn = models.TextField(verbose_name=_('description'), default='', blank=True)

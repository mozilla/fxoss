from django.db import models
from django.contrib.sites.models import Site
from django.contrib.redirects.models import Redirect

class SiteNotes(models.Model):   
    page = models.OneToOneField(Site, editable=False, related_name='extra_fields')
    notes = models.TextField(default='', blank=True)

class RedirectNotes(models.Model):
    page = models.OneToOneField(Redirect, editable=False, related_name='extra_fields')
    notes = models.TextField(default='', blank=True)


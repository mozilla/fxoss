from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.managers import CurrentSiteManager


class TODOItem(models.Model):
    """Tracks translation/content updates needed across sites."""

    ACTION_CREATE = 1
    ACTION_EDIT = 2
    ACTION_DELETE = 3

    ACTION_CHOICES = (
        (ACTION_CREATE, _('Create')),
        (ACTION_EDIT, _('Edit')),
        (ACTION_DELETE, _('Delete')),
    )

    title = title = models.CharField(_('Title'), max_length=500)
    slug =  models.CharField(_('URL'), max_length=2000, blank=True, null=True)
    page = models.ForeignKey('pages.Page', null=True)
    action = models.IntegerField(_('Action'), choices=ACTION_CHOICES)
    description = models.TextField(_('Description'), blank=True)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Editor'),
        related_name='translation_edits')
    site = models.ForeignKey('sites.Site', editable=False)
    created = models.DateTimeField(null=True, editable=False, default=timezone.now)
    resolved = models.DateTimeField(null=True, editable=False)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, editable=False)

    objects = models.Manager()
    site_objects = CurrentSiteManager()

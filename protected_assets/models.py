from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Agreement(models.Model):
    """Record of user signing the user agreement."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        help_text=_('User which signed the agreement.'))
    timestamp = models.DateTimeField(default=now,
        help_text=_('Date and time the agreement was signed.'))
    ip = models.GenericIPAddressField(blank=True, null=True,
        help_text=_('IP address of the signing request.'))
    version = models.CharField(max_length=20, help_text=_('Version of the agreement which was signed.'))

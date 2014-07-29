from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Agreement(models.Model):
    """Marketing agreement that users can sign."""
    name = models.CharField(max_length=255, default='Prototype Branding Agreement')
    version = models.CharField(max_length=20, unique=True)
    created = models.DateTimeField(default=now, editable=False)

    def _agreement_filename(instance, filename):
        return now().strftime('uploads/agreements/%Y-%m-%d_%H:%M:%S_agreement.pdf')
    agreement_pdf = models.FileField(max_length=255, upload_to=_agreement_filename)

    @property
    def url(self):
        return self.agreement_pdf.url

    def __unicode__(self):
        return self.name + ' ' + self.version


class SignedAgreement(models.Model):
    """Record of user signing the user agreement."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        help_text=_('User which signed the agreement.'))
    timestamp = models.DateTimeField(default=now,
        help_text=_('Date and time the agreement was signed.'))
    ip = models.GenericIPAddressField(blank=True, null=True,
        help_text=_('IP address of the signing request.'))
    agreement = models.ForeignKey(Agreement, null=True,
                                  help_text=_('Version of the agreement which was signed.'))

    class Meta:
        ordering = ['-timestamp']

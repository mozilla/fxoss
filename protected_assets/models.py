from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


def _agreement_filename(instance, filename):
    """Custom upload location generator."""
    directory = 'uploads/agreements/{}/'.format(instance.language)
    return directory + now().strftime('%Y-%m-%d_%H:%M:%S_agreement.pdf')


class Agreement(models.Model):
    """Marketing agreement that users can sign."""
    name = models.CharField(
        max_length=255, default='Prototype Branding Agreement')
    version = models.CharField(max_length=20, unique=True)
    created = models.DateTimeField(default=now, editable=False)
    language = models.CharField(
        max_length=10, choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE)
    agreement_pdf = models.FileField(
        max_length=255, upload_to=_agreement_filename)
    translated_from = models.ForeignKey(
        'self', related_name='translations', blank=True, null=True,
        help_text=_('Translated from'))

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
    agreement = models.ForeignKey(
        Agreement, null=True,
        help_text=_('Version of the agreement which was signed.'))

    class Meta:
        ordering = ['-timestamp']
        unique_together = ('user', 'agreement')

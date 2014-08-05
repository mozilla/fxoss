from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


def _agreement_filename(instance, filename):
    """Custom upload location generator."""
    return now().strftime('uploads/agreements/%Y-%m-%d_%H:%M:%S_agreement.pdf')


class Agreement(models.Model):
    """Marketing agreement that users can sign."""
    name = models.CharField(max_length=255, default='Prototype Branding Agreement')
    version = models.CharField(max_length=20, unique=True)
    created = models.DateTimeField(default=now, editable=False)
    agreement_pdf = models.FileField(max_length=255, upload_to=_agreement_filename)

    @property
    def url(self):
        return self.agreement_pdf.url

    def __unicode__(self):
        return self.name + ' ' + self.version

    def localized_pdf(self, language):
        """Get the correct version of the PDF for the user's language choice."""
        result = self.agreement_pdf
        if language != settings.LANGUAGE_CODE:
            try:
                alternate = self.translations.get(language=language)
            except TranslatedAgreement.DoesNotExist:
                pass
            else:
                result = alternate.agreement_pdf
        return result


def _translated_filename(instance, filename):
    """Custom upload location generator."""
    directory = 'uploads/agreements/%s/' % instance.language
    return directory + now().strftime('%Y-%m-%d_%H:%M:%S_agreement.pdf')


class TranslatedAgreement(models.Model):
    """Translated version of the marketing agreement."""
    agreement = models.ForeignKey(Agreement, related_name='translations')
    language = models.CharField(max_length=10,
        choices=[l for l in settings.LANGUAGES if l[0] != settings.LANGUAGE_CODE])
    agreement_pdf = models.FileField(max_length=255, upload_to=_translated_filename)

    def __unicode__(self):
        return '%s (%s)' % (self.agreement, self.get_language_display())

    class Meta:
        unique_together = ('agreement', 'language')


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
        unique_together = ('user', 'agreement')

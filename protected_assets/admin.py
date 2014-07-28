from copy import deepcopy

from django.contrib import admin

from protected_assets.models import Agreement, SignedAgreement
from .models import AgreementNotes, SignedAgreementNotes

from django.utils.translation import ugettext_lazy as _

notes_template = 'protected_assets/stacked.html'

class SignedAgreementExpandedInline(admin.StackedInline):
    model = SignedAgreementNotes
    extra = 1
    template = notes_template
    can_delete = False
    verbose_name_plural = _('Notes')

class SignedAgreementAdmin(admin.ModelAdmin):
    inlines = [SignedAgreementExpandedInline, ]
    list_display = ('user', 'legal_entity', 'agreement',
                    'timestamp', 'ip', )
    list_filter = ('timestamp', 'agreement', )
    date_hierarchy = 'timestamp'
    change_list_template = (
        'protected_assets/admin/signedagreement_change_list.html')

    def legal_entity(self, signed_agreement):
        return signed_agreement.user.profile.legal_entity


class AgreementExpandedInline(admin.StackedInline):
    model = AgreementNotes
    extra = 1
    template = notes_template
    can_delete = False
    verbose_name_plural = _('Notes')

class AgreementAdmin(admin.ModelAdmin):
    inlines = [AgreementExpandedInline, ]
    list_display = ('name', 'version', 'created')


admin.site.register(SignedAgreement, SignedAgreementAdmin)
admin.site.register(Agreement, AgreementAdmin)

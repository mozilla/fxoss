from copy import deepcopy

from django.conf import settings
from django.contrib import admin

from protected_assets.models import Agreement, SignedAgreement


class SignedAgreementAdmin(admin.ModelAdmin):
    list_display = ('user', 'legal_entity', 'agreement',
                    'timestamp', 'ip', )
    list_filter = ('timestamp', 'agreement', )
    date_hierarchy = 'timestamp'
    change_list_template = (
        'protected_assets/admin/signedagreement_change_list.html')

    def legal_entity(self, signed_agreement):
        return signed_agreement.user.profile.legal_entity


class AgreementAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'language', 'created')


admin.site.register(SignedAgreement, SignedAgreementAdmin)
admin.site.register(Agreement, AgreementAdmin)

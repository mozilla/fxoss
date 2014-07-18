from copy import deepcopy

from django.contrib import admin

from mezzanine.pages.admin import LinkAdmin as BaseLinkAdmin
from mezzanine.pages.models import Link

from protected_assets.models import Agreement, SignedAgreement


class SignedAgreementAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user',  'timestamp', 
                       'ip', 'agreement', )
        }),
        ('Notes', {
            'classes': ('collapse-closed',),
            'fields': ('notes', )
        }),
    )
    list_display = ('user', 'legal_entity', 'agreement',
                    'timestamp', 'ip', )
    list_filter = ('timestamp', 'agreement', )
    date_hierarchy = 'timestamp'
    change_list_template = (
        'protected_assets/admin/signedagreement_change_list.html')

    def legal_entity(self, signed_agreement):
        return signed_agreement.user.profile.legal_entity


class LinkAdmin(BaseLinkAdmin):
    """
    Customization of LinkAdmin to allow making links only display to
    authenticated users.
    """
    fieldsets = deepcopy(BaseLinkAdmin.fieldsets)
    fieldsets[0][1]["fields"] += ("login_required", )


class AgreementAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'version', 'agreement_pdf',)
        }),
        ('Notes', {
            'classes': ('collapse-closed',),
            'fields': ('notes', )
        }),
    )
    list_display = ('name', 'version', 'created')

admin.site.unregister(Link)
admin.site.register(Link, LinkAdmin)
admin.site.register(SignedAgreement, SignedAgreementAdmin)
admin.site.register(Agreement, AgreementAdmin)

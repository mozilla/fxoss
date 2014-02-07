from copy import deepcopy

from django.contrib import admin

from mezzanine.pages.admin import  LinkAdmin as BaseLinkAdmin
from mezzanine.pages.models import Link


from .models import Agreement


class AgreementAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'version', 'ip', )
    list_filter = ('timestamp', 'version', )
    date_hierarchy = 'timestamp'


admin.site.register(Agreement, AgreementAdmin)


link_fieldsets = deepcopy(BaseLinkAdmin.fieldsets)
link_fieldsets[0][1]["fields"] += ("login_required", )


class LinkAdmin(BaseLinkAdmin):
    """Customization of LinkAdmin to allow making links only display to authenticated users."""

    fieldsets = link_fieldsets


admin.site.unregister(Link)
admin.site.register(Link, LinkAdmin)

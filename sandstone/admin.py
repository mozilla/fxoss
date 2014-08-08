import reversion

from concurrency import forms
from concurrency.admin import ConcurrencyActionMixin, ConcurrencyListEditableMixin
from concurrency.api import disable_concurrency
from concurrency.forms import VersionWidget

from copy import deepcopy

from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from mezzanine.accounts.admin import UserProfileAdmin
from mezzanine.core.models import SitePermission
from mezzanine.forms.admin import FormAdmin
from mezzanine.forms.models import Form
from mezzanine.pages.admin import PageAdmin, LinkAdmin
from mezzanine.pages.models import RichTextPage, Link

from translations.admin import TranslatableMixin


rt_page_fieldsets = deepcopy(PageAdmin.fieldsets)
rt_page_fieldsets[0][1]["fields"].insert(3, "intro")
rt_page_fieldsets[0][1]["fields"].insert(4, "inherit")
rt_page_fieldsets[0][1]["fields"].insert(5, "cta_title")
rt_page_fieldsets[0][1]["fields"].insert(6, "cta_body")
rt_page_fieldsets[0][1]["fields"].insert(7, "content")
rt_page_fieldsets[0][1]["fields"].insert(-1, "version")
# Add Notes field with its own collapsable section
rt_page_fieldsets += ((_("Notes"), {
    "fields": ("notes",),
    "classes": ("collapse-closed",)},),)

form_page_fieldsets = deepcopy(FormAdmin.fieldsets)
form_page_fieldsets[0][1]["fields"].insert(-1, "version")
# Add Notes field with its own collapsable section
form_page_fieldsets += ((_("Notes"), {
    "fields": ("notes",),
    "classes": ("collapse-closed",)},),)

link_page_fieldsets = deepcopy(LinkAdmin.fieldsets)
link_page_fieldsets[0][1]["fields"].insert(-1, "version")


# Allows django-reversion and django-concurrency to work together
class ConcurrencyReversionAdmin(reversion.VersionAdmin,
                                ConcurrencyActionMixin,
                                ConcurrencyListEditableMixin,):
    def render_revision_form(self, request, obj, version, context, revert=False, recover=False):
        with disable_concurrency(obj):
            return super(ConcurrencyReversionAdmin, self).render_revision_form(request, obj, version, context, revert, recover)


class SandstoneRichTextPageAdmin(TranslatableMixin, ConcurrencyReversionAdmin,
                                 PageAdmin):
    fieldsets = rt_page_fieldsets
    history_latest_first = True
    formfield_overrides = {forms.VersionField: {'widget': VersionWidget}}
    tranlsated_fields = ['title', 'intro', 'cta_title', 'cta_body', 'content']


class SandstoneFormAdmin(TranslatableMixin, ConcurrencyReversionAdmin,
                         FormAdmin):
    fieldsets = form_page_fieldsets
    history_latest_first = True
    formfield_overrides = {forms.VersionField: {'widget': VersionWidget}}
    tranlsated_fields = ['title', 'intro', 'cta_title', 'cta_body', 'content']


class SandstoneLinkAdmin(TranslatableMixin, LinkAdmin):
    """
    Customization of LinkAdmin to allow making links only display to
    authenticated users.
    """
    fieldsets = deepcopy(LinkAdmin.fieldsets)
    fieldsets[0][1]["fields"] += ("login_required", )
    # Add Notes field with its own collapsable section
    fieldsets += ((_("Notes"), {
        "fields": ("notes",),
        "classes": ("collapse-closed",)},),)
    tranlsated_fields = ['title', ]


def _remove_duplicate_permissions(user):
    """Delete duplicate SitePermission records, if any, for the user."""
    if user.pk:
        permissions = SitePermission.objects.filter(user=user)
        if permissions.count() > 1:
            permissions.exclude(id=permissions.order_by('pk')[0].pk).delete()


class SandstoneUserAdmin(UserProfileAdmin):
    """Customization of the User admin to prevent/clean up duplicate SitePermission records."""

    def save_related(self, request, form, formsets, change):
        super(SandstoneUserAdmin, self).save_related(request, form, formsets, change)
        _remove_duplicate_permissions(form.instance)


admin.site.unregister(Form)
admin.site.unregister(RichTextPage)
admin.site.unregister(Link)
admin.site.unregister(User)

admin.site.register(RichTextPage, SandstoneRichTextPageAdmin)
admin.site.register(Form, SandstoneFormAdmin)
admin.site.register(Link, SandstoneLinkAdmin)
admin.site.register(User, SandstoneUserAdmin)

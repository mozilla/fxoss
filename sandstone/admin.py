import reversion

from concurrency import forms
from concurrency.admin import ConcurrencyActionMixin, ConcurrencyListEditableMixin
from concurrency.api import disable_concurrency
from concurrency.forms import VersionWidget

from copy import deepcopy

from django.contrib import admin

from mezzanine.forms.admin import FormAdmin
from mezzanine.forms.models import Form
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage
from django.utils.translation import ugettext_lazy


rt_page_fieldsets = deepcopy(PageAdmin.fieldsets)
rt_page_fieldsets[0][1]["fields"].insert(3, "intro")
rt_page_fieldsets[0][1]["fields"].insert(4, "inherit")
rt_page_fieldsets[0][1]["fields"].insert(5, "cta_title")
rt_page_fieldsets[0][1]["fields"].insert(6, "cta_body")
rt_page_fieldsets[0][1]["fields"].insert(7, "content")
rt_page_fieldsets[0][1]["fields"].insert(-1, "version")
# Add Notes field with its own collapsable section
rt_page_fieldsets += ((ugettext_lazy("Notes"), {
    "fields": ("notes",),
    "classes": ("collapse-closed",)},),)

form_page_fieldsets = deepcopy(FormAdmin.fieldsets)
form_page_fieldsets[0][1]["fields"].insert(-1, "version")


# Allows django-reversion and django-concurrency to work together
class ConcurrencyReversionAdmin(reversion.VersionAdmin,
                                ConcurrencyActionMixin,
                                ConcurrencyListEditableMixin,):
    def render_revision_form(self, request, obj, version, context, revert=False, recover=False):
        with disable_concurrency(obj):
            return super(ConcurrencyReversionAdmin, self).render_revision_form(request, obj, version, context, revert, recover)


class SandstoneRichTextPageAdmin(ConcurrencyReversionAdmin,
                                 PageAdmin):
    fieldsets = rt_page_fieldsets
    history_latest_first = True
    formfield_overrides = {forms.VersionField: {'widget': VersionWidget}}


class SandstoneFormAdmin(ConcurrencyReversionAdmin,
                         FormAdmin):
    fieldsets = form_page_fieldsets
    history_latest_first = True
    formfield_overrides = {forms.VersionField: {'widget': VersionWidget}}


admin.site.unregister(Form)
admin.site.unregister(RichTextPage)

admin.site.register(RichTextPage, SandstoneRichTextPageAdmin)
admin.site.register(Form, SandstoneFormAdmin)

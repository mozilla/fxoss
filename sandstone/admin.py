from concurrency import forms
from concurrency.admin import ConcurrencyActionMixin, ConcurrencyListEditableMixin
from concurrency.forms import VersionWidget

from copy import deepcopy

from django.contrib import admin

from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage


rt_page_fieldsets = deepcopy(PageAdmin.fieldsets)
rt_page_fieldsets[0][1]["fields"].insert(3, "intro")
rt_page_fieldsets[0][1]["fields"].insert(4, "inherit")
rt_page_fieldsets[0][1]["fields"].insert(5, "cta_title")
rt_page_fieldsets[0][1]["fields"].insert(6, "cta_body")
rt_page_fieldsets[0][1]["fields"].insert(7, "content")
rt_page_fieldsets[0][1]["fields"].insert(8, "version")


class SandstoneRichTextPageAdmin(ConcurrencyActionMixin,
                                 ConcurrencyListEditableMixin,
                                 PageAdmin):
    fieldsets = rt_page_fieldsets
    formfield_overrides = {forms.VersionField: {'widget': VersionWidget}}

admin.site.unregister(RichTextPage)
admin.site.register(RichTextPage, SandstoneRichTextPageAdmin)

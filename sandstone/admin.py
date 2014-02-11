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


class SandstoneRichTextPageAdmin(PageAdmin):
    fieldsets = rt_page_fieldsets

admin.site.unregister(RichTextPage)
admin.site.register(RichTextPage, SandstoneRichTextPageAdmin)

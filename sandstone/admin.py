from copy import deepcopy

from django.contrib import admin

from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage


rt_page_fieldsets = deepcopy(PageAdmin.fieldsets)
rt_page_fieldsets[0][1]["fields"].insert(3, "subtitle")
rt_page_fieldsets[0][1]["fields"].insert(4, "intro")
rt_page_fieldsets[0][1]["fields"].insert(5, "content")
rt_page_fieldsets[0][1]["fields"].insert(6, "closing")


class SandstoneRichTextPageAdmin(PageAdmin):
    fieldsets = rt_page_fieldsets

admin.site.unregister(RichTextPage)
admin.site.register(RichTextPage, SandstoneRichTextPageAdmin)

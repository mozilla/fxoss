"""Registration of the Mezzanine models for translation."""
from copy import deepcopy

from django.contrib import admin

from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import Page, RichTextPage
from modeltranslation.admin import TranslationAdmin
from modeltranslation.translator import translator, TranslationOptions


class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'description', )


class RichTextPageTranslationOptions(PageTranslationOptions):
    fields = ('content', )


translator.register(Page, PageTranslationOptions)
translator.register(RichTextPage, RichTextPageTranslationOptions)


class TranslatedPageAdmin(PageAdmin, TranslationAdmin):
    pass


rich_text_fieldsets = deepcopy(TranslatedPageAdmin.fieldsets)
rich_text_fieldsets[0][1]["fields"] += ("content", )

class TranslatedRichTextPageAdmin(TranslatedPageAdmin):
    fieldsets = rich_text_fieldsets


admin.site.unregister(Page)
admin.site.unregister(RichTextPage)
admin.site.register(Page, TranslatedPageAdmin)
admin.site.register(RichTextPage, TranslatedRichTextPageAdmin)

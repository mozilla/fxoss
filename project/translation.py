"""Registration of the Mezzanine models for translation."""
from copy import deepcopy

from django.contrib import admin

from mezzanine.forms.models import Form, Field
from mezzanine.pages.admin import PageAdmin, LinkAdmin
from mezzanine.pages.models import Page, RichTextPage, Link
from modeltranslation.admin import TranslationAdmin
from modeltranslation.translator import translator, TranslationOptions


class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'description', )


class RichTextPageTranslationOptions(PageTranslationOptions):
    fields = ('content', )


class LinkTranslationOptions(TranslationOptions):
    fields = ('title', )


class FormTranslationOptions(RichTextPageTranslationOptions):
    fields = ('button_text', 'response', )


class FieldTranslationOptions(TranslationOptions):
    fields = ('label', 'choices', 'default', 'placeholder_text', 'help_text', )


translator.register(Page, PageTranslationOptions)
translator.register(RichTextPage, RichTextPageTranslationOptions)
translator.register(Link, LinkTranslationOptions)
translator.register(Form, FormTranslationOptions)
translator.register(Field, FieldTranslationOptions)


class TranslatedPageAdmin(PageAdmin, TranslationAdmin):
    """Combined Page admin class for Mezzanine and modeltranslation."""


rich_text_fieldsets = deepcopy(TranslatedPageAdmin.fieldsets)
rich_text_fieldsets[0][1]["fields"] += ("content", )

class TranslatedRichTextPageAdmin(TranslatedPageAdmin):
    fieldsets = rich_text_fieldsets


class TranslatedLinkAdmin(LinkAdmin, TranslationAdmin):
    """Combined Link admin class for Mezzanine and modeltranslation."""


admin.site.unregister(Page)
admin.site.unregister(RichTextPage)
admin.site.unregister(Link)
admin.site.register(Page, TranslatedPageAdmin)
admin.site.register(RichTextPage, TranslatedRichTextPageAdmin)
admin.site.register(Link, TranslatedLinkAdmin)

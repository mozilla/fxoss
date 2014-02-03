"""Registration of the Mezzanine models for translation."""

from mezzanine.forms.models import Form, Field
from mezzanine.pages.models import Page, RichTextPage, Link
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

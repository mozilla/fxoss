"""Registration of the Mezzanine models for translation."""
from copy import deepcopy

from django.contrib import admin
from django.utils.translation import get_language, get_language_from_request, override

from mezzanine.forms.admin import FormAdmin, FieldAdmin
from mezzanine.forms.models import Form, Field
from mezzanine.pages.admin import PageAdmin, LinkAdmin
from mezzanine.pages.models import Page, RichTextPage, Link
from modeltranslation import settings
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from modeltranslation.translator import translator, TranslationOptions
from modeltranslation.utils import build_localized_fieldname, get_translation_fields


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


def _get_translation_fields(field):
    """Instead of adding fields for every available language only
    fields for the default and selected language are added."""
    languages = [settings.DEFAULT_LANGUAGE, ]
    active = get_language().split('-')[0].lower()
    if active not in languages and active in settings.AVAILABLE_LANGUAGES:
        languages.append(active)
    return [build_localized_fieldname(field, l) for l in languages]


class SlimTranslationMixin(object):
    """Mixin for SlimTranslationAdmin to only show at most two languages: the base
    translation language (EN) and the selected language for the user."""

    def replace_orig_field(self, option):
        """Override of the default replace_orig_field for django-modeltranslation.
        This handles both the original replacement of the fields and the language
        switching case.
        """
        if option:
            option_clean = list(option)
            # Make one pass to replace translated field names with original names
            for opt in option:
                for field in self.trans_opts.fields:
                    tranlated = get_translation_fields(field)
                    if opt in get_translation_fields(field):
                        if field not in option_clean:
                            index = option_clean.index(opt)
                            option_clean[index:index + 1] = [field]
                        else:
                            option_clean.remove(opt)
            option_new = list(option_clean)               
            for opt in option_clean:
                if opt in self.trans_opts.fields:
                    index = option_new.index(opt)
                    option_new[index:index + 1] = _get_translation_fields(opt)
                elif isinstance(opt, (tuple, list)) and (
                        [o for o in opt if o in self.trans_opts.fields]):
                    index = option_new.index(opt)
                    option_new[index:index + 1] = self.replace_orig_field(opt)
            option = option_new
        return option

    def _do_get_form_or_formset(self, request, obj, **kwargs):
        """Activate the current language from the request before patching the fields."""
        language = get_language_from_request(request, check_path=True)
        with override(language):
            result = super(SlimTranslationMixin, self)._do_get_form_or_formset(request, obj, **kwargs)
        return result


class TranslatedPageAdmin(PageAdmin, SlimTranslationMixin, TranslationAdmin):
    """Combined Page admin class for Mezzanine and modeltranslation."""


rich_text_fieldsets = deepcopy(TranslatedPageAdmin.fieldsets)
rich_text_fieldsets[0][1]["fields"] += ("content", )

class TranslatedRichTextPageAdmin(TranslatedPageAdmin):
    fieldsets = rich_text_fieldsets


class TranslatedLinkAdmin(LinkAdmin, SlimTranslationMixin, TranslationAdmin):
    """Combined Link admin class for Mezzanine and modeltranslation."""


class TranslatedFieldAdmin(FieldAdmin, SlimTranslationMixin, TranslationTabularInline):
    """Inline admin for translated Fields."""

    fields = ['label', 'field_type', 'required', 'visible',
        'choices', 'default', 'help_text', '_order']


class TranslatedFormAdmin(FormAdmin, SlimTranslationMixin, TranslationAdmin):
    """Combined Form admin class for Mezzanine and modeltranslation."""

    inlines = (TranslatedFieldAdmin, )


admin.site.unregister(Page)
admin.site.unregister(RichTextPage)
admin.site.unregister(Link)
admin.site.unregister(Form)
admin.site.register(Page, TranslatedPageAdmin)
admin.site.register(RichTextPage, TranslatedRichTextPageAdmin)
admin.site.register(Link, TranslatedLinkAdmin)
admin.site.register(Form, TranslatedFormAdmin)

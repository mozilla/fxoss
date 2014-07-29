import reversion

from concurrency import forms
from concurrency.admin import ConcurrencyActionMixin, ConcurrencyListEditableMixin
from concurrency.api import disable_concurrency
from concurrency.forms import VersionWidget

from copy import deepcopy

from django.contrib import admin

from mezzanine.forms.admin import FormAdmin
from mezzanine.forms.models import Form
from mezzanine.pages.admin import PageAdmin, LinkAdmin
from mezzanine.pages.models import RichTextPage, Link
from .models import FormNotes, PageNotes, LinkNotes
from translations.admin import TranslatableMixin

from django.utils.translation import ugettext_lazy as _

rt_page_fieldsets = deepcopy(PageAdmin.fieldsets)
rt_page_fieldsets[0][1]["fields"].insert(3, "intro")
rt_page_fieldsets[0][1]["fields"].insert(4, "inherit")
rt_page_fieldsets[0][1]["fields"].insert(5, "cta_title")
rt_page_fieldsets[0][1]["fields"].insert(6, "cta_body")
rt_page_fieldsets[0][1]["fields"].insert(7, "content")
rt_page_fieldsets[0][1]["fields"].insert(-1, "version")

form_page_fieldsets = deepcopy(FormAdmin.fieldsets)
form_page_fieldsets[0][1]["fields"].insert(-1, "version")

# Allows django-reversion and django-concurrency to work together
class ConcurrencyReversionAdmin(reversion.VersionAdmin,
                                ConcurrencyActionMixin,
                                ConcurrencyListEditableMixin,):
    def render_revision_form(self, request, obj, version, context, revert=False, recover=False):
        with disable_concurrency(obj):
            return super(ConcurrencyReversionAdmin, self).render_revision_form(request, obj, version, context, revert, recover)


class PageExpandedInline(admin.StackedInline):
    model = PageNotes
    extra = 1
    template = 'inline/stacked.html'
    can_delete = False
    verbose_name_plural = _('Notes')

class SandstoneRichTextPageAdmin(TranslatableMixin, ConcurrencyReversionAdmin,
                                 PageAdmin):
    fieldsets = rt_page_fieldsets
    history_latest_first = True
    formfield_overrides = {forms.VersionField: {'widget': VersionWidget}}
    tranlsated_fields = ['title', 'intro', 'cta_title', 'cta_body', 'content']
    inlines = [PageExpandedInline, ]


class FormExpandedInline(admin.StackedInline):
    model = FormNotes
    extra = 1
    template = 'inline/stacked.html'
    can_delete = False
    verbose_name_plural = _('Notes')

class SandstoneFormAdmin(TranslatableMixin, ConcurrencyReversionAdmin,
                         FormAdmin):
    fieldsets = form_page_fieldsets
    history_latest_first = True
    formfield_overrides = {forms.VersionField: {'widget': VersionWidget}}
    tranlsated_fields = ['title', 'intro', 'cta_title', 'cta_body', 'content']
    inlines = [FormExpandedInline, ]


class LinkExpandedInline(admin.StackedInline):
    model = LinkNotes
    extra = 1
    template = 'inline/stacked.html'
    can_delete = False
    verbose_name_plural = _('Notes')

class SandstoneLinkAdmin(TranslatableMixin, LinkAdmin):
    """
    Customization of LinkAdmin to allow making links only display to
    authenticated users.
    """
    fieldsets = deepcopy(LinkAdmin.fieldsets)
    fieldsets[0][1]["fields"] += ("login_required", )
    tranlsated_fields = ['title', ]
    inlines = [LinkExpandedInline, ]


admin.site.unregister(Form)
admin.site.unregister(RichTextPage)
admin.site.unregister(Link)

admin.site.register(RichTextPage, SandstoneRichTextPageAdmin)
admin.site.register(Form, SandstoneFormAdmin)
admin.site.register(Link, SandstoneLinkAdmin)

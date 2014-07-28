from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.redirects.models import Redirect
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from .models import RedirectNotes
from .models import SiteNotes
from .models import GroupNotes

from django.utils.translation import ugettext_lazy as _

notes_template = 'site_notes/stacked.html'

class SiteExpandedInline(admin.StackedInline):
    model = SiteNotes
    extra = 1
    template = notes_template
    can_delete = False
    verbose_name_plural = _('Notes')


class SiteNotesAdmin(admin.ModelAdmin):
    inlines = [SiteExpandedInline, ]


class RedirectExpandedInline(admin.StackedInline):
    model = RedirectNotes
    extra = 1
    template = notes_template
    can_delete = False
    verbose_name_plural = _('Notes')


class RedirectNotesAdmin(admin.ModelAdmin):
    inlines = [RedirectExpandedInline, ]


class CommentExpandedInline(admin.StackedInline):
    model = RedirectNotes
    extra = 1
    template = notes_template
    can_delete = False
    verbose_name_plural = _('Notes')


class CommentNotesAdmin(admin.ModelAdmin):
    inlines = [CommentExpandedInline, ]


class GroupNotesInline(admin.StackedInline):
    model = GroupNotes
    extra = 1
    template = notes_template
    can_delete = False
    verbose_name_plural = _('Notes')


class GroupAdmin(GroupAdmin):
    inlines = (GroupNotesInline, )


admin.site.unregister(Site)
admin.site.unregister(Redirect)
admin.site.unregister(Group)

admin.site.register(Site, SiteNotesAdmin)
admin.site.register(Redirect, RedirectNotesAdmin)
admin.site.register(Group, GroupAdmin)

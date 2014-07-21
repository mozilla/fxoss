from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin
from django.contrib.redirects.admin import RedirectAdmin
from django.contrib.sites.models import Site
from django.contrib.redirects.models import Redirect
from .models import RedirectNotes, SiteNotes

class SiteExpandedInline(admin.StackedInline):
    model = SiteNotes
    extra = 1
    template = 'site_notes/stacked.html'
    can_delete = False
    verbose_name_plural = 'Notes'


class SiteNotesAdmin(admin.ModelAdmin):
    inlines = [SiteExpandedInline, ]


class RedirectExpandedInline(admin.StackedInline):
    model = RedirectNotes
    extra = 1
    template = 'site_notes/stacked.html'
    can_delete = False
    verbose_name_plural = 'Notes'


class RedirectNotesAdmin(admin.ModelAdmin):
    inlines = [RedirectExpandedInline, ]


admin.site.unregister(Site)
admin.site.unregister(Redirect)

admin.site.register(Site, SiteNotesAdmin)
admin.site.register(Redirect, RedirectNotesAdmin)

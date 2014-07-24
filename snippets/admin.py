from django.contrib import admin

from .models import TinyMCESnippet, TinyMCESnippetNotes

notes_template = 'snippets/stacked.html'

class TinyMCEExpandedInline(admin.StackedInline):
    model = TinyMCESnippetNotes
    extra = 1
    template = notes_template
    can_delete = False
    verbose_name_plural = 'Notes'

class TinyMCESnippetAdmin(admin.ModelAdmin):
    inlines = [TinyMCEExpandedInline, ]
    list_display = ('title', 'description', )


admin.site.register(TinyMCESnippet, TinyMCESnippetAdmin)

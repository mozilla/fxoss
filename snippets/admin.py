from django.contrib import admin

from .models import TinyMCESnippet


class TinyMCESnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', )


admin.site.register(TinyMCESnippet, TinyMCESnippetAdmin)

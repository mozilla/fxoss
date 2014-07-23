from django.contrib import admin

from .models import TinyMCESnippet


class TinyMCESnippetAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'description',)
        }),
        ('Notes', {
            'classes': ('collapse-closed',),
            'fields': ('notes', )
        }),
    )
    list_display = ('title', 'description', )


admin.site.register(TinyMCESnippet, TinyMCESnippetAdmin)

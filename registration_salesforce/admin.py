from django.contrib import admin
from django.contrib.auth.models import User

from mezzanine.core.admin import SitePermissionUserAdmin

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(SitePermissionUserAdmin):
    inlines = SitePermissionUserAdmin.inlines + [ProfileInline, ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, UserNotes

from django.utils.translation import ugettext_lazy as _

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserNotesInline(admin.StackedInline):
    model = UserNotes
    extra = 1
    template = 'registration_salesforce/stacked.html'
    can_delete = False
    verbose_name_plural = _('Notes')


class UserAdmin(UserAdmin):
    inlines = (ProfileInline, UserNotesInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

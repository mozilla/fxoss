from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group


from .models import GroupNotes, Profile, UserNotes


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserNotesInline(admin.StackedInline):
    model = UserNotes
    extra = 1
    template = 'registration_salesforce/stacked.html'
    can_delete = False
    verbose_name_plural = 'Notes'


class UserAdmin(UserAdmin):
    inlines = (ProfileInline, UserNotesInline, )


class GroupNotesInline(admin.StackedInline):
    model = GroupNotes
    extra = 1
    template = 'registration_salesforce/stacked.html'
    can_delete = False
    verbose_name_plural = 'Notes'


class GroupAdmin(GroupAdmin):
    inlines = (GroupNotesInline, )


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)

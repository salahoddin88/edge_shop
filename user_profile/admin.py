from django.contrib import admin

from user_profile.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile']


admin.site.register(UserProfile, UserProfileAdmin)
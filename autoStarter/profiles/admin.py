from django.contrib import admin
from profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'phone', 'country', 'region', 'locality']


admin.site.register(Profile, ProfileAdmin)

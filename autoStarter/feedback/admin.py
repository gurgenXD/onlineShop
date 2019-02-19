from django.contrib import admin
from feedback.models import FeedBack


class FeedBackAdmin(admin.ModelAdmin):
    list_display = ['phone_or_email', 'name']


admin.site.register(FeedBack, FeedBackAdmin)

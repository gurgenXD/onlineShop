from django.contrib import admin
from callback.models import CallBack


class CallBackAdmin(admin.ModelAdmin):
    list_display = ['phone', 'call_time']
    list_filter = ['call_time']


admin.site.register(CallBack, CallBackAdmin)

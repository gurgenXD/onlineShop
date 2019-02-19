from django.contrib import admin
from static_strings.models import MailToString, MailFromString


admin.site.register(MailToString)
admin.site.register(MailFromString)

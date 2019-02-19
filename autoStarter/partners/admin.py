from django.contrib import admin
from partners.models import Partner


class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'partner_url']


admin.site.register(Partner, PartnerAdmin)

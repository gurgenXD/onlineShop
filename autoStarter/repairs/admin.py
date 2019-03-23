from django.contrib import admin
from repairs.models import Repair


class RepairAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'repair_date', 'repair_time', 'car']


admin.site.register(Repair, RepairAdmin)
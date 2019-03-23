from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from landing.models import AboutUs, Partner, Brand, Slide, InfoBlock, OurPros, TopMenuPoint


class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'partner_url']


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand_url']


class TopMenuPointAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['point', 'my_order']


admin.site.register(Brand, BrandAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(AboutUs)
admin.site.register(Slide)
admin.site.register(InfoBlock)
admin.site.register(OurPros)
admin.site.register(TopMenuPoint, TopMenuPointAdmin)

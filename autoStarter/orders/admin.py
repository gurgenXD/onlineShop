from django.contrib import admin
from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'total_price', 'delivery', 'payment', 'created', 'updated']
    extends = ['saved']
    list_filter = ['created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
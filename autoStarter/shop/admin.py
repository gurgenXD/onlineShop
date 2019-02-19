from django.contrib import admin
from django import forms
from shop.models import Image, Product, Category, SubCategory, Car, CarBrand, CarModel, Manufacturer, Feature, FeatureValue


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 0


class FeatureValueInline(admin.TabularInline):
    model = FeatureValue
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    inlines = [SubCategoryInline]


class ProductAdmin(admin.ModelAdmin):
    exclude = ['price', 'category']
    list_display = ['name', 'subcategory', 'category', 'price_without_sale', 'sale', 'price', 'stock', 'purchased',
                    'is_active']
    list_filter = ['category', 'subcategory', 'is_active']
    readonly_fields = ['purchased']
    list_editable = ['price_without_sale', 'sale', 'stock', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [FeatureValueInline, ImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer)
admin.site.register(Feature)
admin.site.register(Car)
admin.site.register(CarModel)
admin.site.register(CarBrand)

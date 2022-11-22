from django.contrib import admin

from .models import *


class ItemAdmin(admin.ModelAdmin):
    list_filter = ('name', 'description', 'price')
    list_display = ('id', 'name', 'description', 'price', 'price_id')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'discount')
    list_display_links = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('discount', 'discount_stripe_id',)
    list_display_links = ('discount',)
    list_filter = ('discount',)
    search_fields = ('discount',)


class TaxAdmin(admin.ModelAdmin):
    list_display = ('type_tax', 'tax_rate', 'tax_rate_id',)
    list_display_links = ('type_tax',)
    list_filter = ('type_tax', 'tax_rate',)
    search_fields = ('type_tax', 'tax_rate',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Tax, TaxAdmin)

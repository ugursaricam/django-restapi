from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_number','product_name', 'price', 'stock', 'category', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ('category', 'is_available')
    list_editable = ('price', 'stock', 'is_available')
    search_fields = ('product_name', 'description')
    filter_horizontal = ('allowed_users',)

admin.site.register(Product, ProductAdmin)

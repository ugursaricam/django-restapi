from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('product_name', 'product_number')  # 'description' alanını kaldırdık
    filter_horizontal = ('allowed_users',)

admin.site.register(Product, ProductAdmin)

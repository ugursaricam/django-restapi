from django.contrib import admin
from .models import Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['ordered', 'product', 'quantity', 'product_price', 'created_at', 'user']
    can_delete = False
    extra = 0
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','company_number', 'company_name', 'full_name', 'email', 'is_ordered', 'created_at', 'csv_exported']
    list_filter = ['company_name','created_at']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)


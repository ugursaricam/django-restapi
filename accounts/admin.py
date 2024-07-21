from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from django.utils.html import format_html

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('company_number','company_name', 'full_name', 'email', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('company_name', 'full_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('company_number',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)

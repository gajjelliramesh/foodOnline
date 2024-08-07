from django.contrib import admin

from vendor.models import Vendor
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomVendorAdmin(UserAdmin):
    list_display = ("user", "vendor_name", "is_approved", "created_at")
    ordering = ("-user",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Vendor, CustomVendorAdmin)

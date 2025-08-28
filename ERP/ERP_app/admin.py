from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *



# ---- Custom Admin Site Branding ----
admin.site.site_header = "ERP Inventory & Sales Management"
admin.site.site_title = "ERP Admin Portal"
admin.site.index_title = "Welcome to ERP Dashboard"


# ✅ Custom User Admin (shows role field also)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "role")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "role", "password1", "password2", "is_staff", "is_active"),
        }),
    )
    search_fields = ("username", "email", "role")
    ordering = ("username",)


# ✅ Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "stock")
    search_fields = ("name", "category")
    list_filter = ("category",)


# ✅ Customer Admin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone")
    search_fields = ("name", "email", "phone")


# ✅ Sale Admin
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "customer", "quantity", "total_price", "date")
    list_filter = ("date", "product", "customer")
    search_fields = ("product__name", "customer__name")
    date_hierarchy = "date"


# ✅ Register Custom User
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)

@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ('title', 'chart_type', 'value', 'created_at')
    readonly_fields = ('value', 'created_at')  # value auto-calculated


# invoice
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "user_type", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("User Type", {"fields": ("user_type",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("User Type", {"fields": ("user_type",)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

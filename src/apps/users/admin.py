from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ["email", "full_name", "is_active", "is_staff"]
    search_fields = ["email", "last_name"]
    list_filter = ["is_active", "is_staff"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)

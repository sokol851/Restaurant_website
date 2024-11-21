from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "is_active",
        "first_name",
        "last_name",
    )
    list_filter = (
        "email",
        "is_active",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

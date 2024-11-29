from django.contrib import admin

from reservations.models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "restaurant",
        "date",
        "time",
        "available",
    )
    list_filter = (
        "restaurant",
        "number",
        "date",
        "time",
        "available",
    )
    ordering = (
        "restaurant",
        "number",
        "date",
        "time",
        "available",
    )
    search_fields = (
        "restaurant",
        "number",
        "date",
    )

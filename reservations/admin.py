from django.contrib import admin

from reservations.models import Table, Reservation


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "restaurant",
        "is_datetime",
        "available",
    )
    list_filter = (
        "restaurant",
        "number",
        "is_datetime",
        "available",
    )
    ordering = (
        "restaurant",
        "number",
        "is_datetime",
        "available",
    )
    search_fields = (
        "restaurant",
        "number",
        "datetime",
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "table",
        "user",
        "phone",
        "comment",
        "is_confirmed",
    )
    list_filter = (
        "table",
        "user",
        "phone",
        "is_confirmed",
    )
    ordering = (
        "create_at",
        "is_confirmed",
    )
    search_fields = (
        "table",
        "id",
        "user",
        "phone",
        "create_at",
    )

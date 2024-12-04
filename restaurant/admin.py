from django.contrib import admin

from restaurant.models import (Description, HistoryRestaurant,
                               MissionsRestaurant, Restaurant, Services,
                               StaffRestaurant)


@admin.register(StaffRestaurant)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "position",
        "date_employment",
        "is_published",
    )
    list_filter = (
        "last_name",
        "position",
        "date_employment",
        "is_published",
    )
    search_fields = (
        "first_name",
        "last_name",
        "position",
    )


@admin.register(MissionsRestaurant)
class MissionsAdmin(admin.ModelAdmin):
    list_display = (
        "mission",
        "description",
        "serial_number",
    )
    list_filter = (
        "mission",
        "serial_number",
    )
    search_fields = ("mission",)
    ordering = ("serial_number",)


@admin.register(HistoryRestaurant)
class HistoryAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "activity",
    )
    list_filter = ("year",)
    search_fields = (
        "activity",
        "year",
    )
    ordering = ("-year",)


@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "is_published",
    )
    list_filter = ("is_published",)


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = (
        "service",
        "is_published",
    )
    list_filter = ("is_published",)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
    )
    list_filter = (
        "name",
        "city",
    )

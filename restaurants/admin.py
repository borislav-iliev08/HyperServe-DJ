from django.contrib import admin

from restaurants.models import Perks, Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuisine_type', 'address')
    search_fields = ('name', 'address', 'cuisine_type')
    filter_horizontal = ('perks',)


@admin.register(Perks)
class PerksAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
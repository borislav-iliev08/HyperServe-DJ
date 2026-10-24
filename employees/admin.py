from django.contrib import admin

from employees.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'restaurant', 'email', 'phone_number')
    list_filter = ('position', 'restaurant')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'restaurant__name')
    list_select_related = ('restaurant',)
    ordering = ('last_name', 'first_name')
    autocomplete_fields = ('restaurant',)
from django.contrib import admin

from reviews.models import EmployeeReview, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'restaurant', 'author', 'rating', 'created_at', 'is_flagged')
    list_filter = ('rating', 'is_flagged', 'created_at')
    search_fields = ('title', 'content', 'author', 'restaurant__name')
    list_select_related = ('restaurant',)
    ordering = ('-created_at',)
    autocomplete_fields = ('restaurant',)
    readonly_fields = ('created_at', 'is_flagged')


@admin.register(EmployeeReview)
class EmployeeReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'employee', 'author', 'rating', 'created_at', 'is_flagged')
    list_filter = ('rating', 'is_flagged', 'created_at')
    search_fields = ('title', 'content', 'author', 'employee__first_name', 'employee__last_name')
    list_select_related = ('employee',)
    ordering = ('-created_at',)
    autocomplete_fields = ('employee',)
    readonly_fields = ('created_at', 'is_flagged')
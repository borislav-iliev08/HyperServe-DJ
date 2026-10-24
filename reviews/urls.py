from django.urls import path
from employees.views import EmployeeReviewDeleteView, EmployeeReviewDetailView, EmployeeReviewEditView, EmployeeReviewsListView
from reviews.views import (
    ReviewListView,
    ReviewCreateView,
    ReviewDetailView,
    ReviewEditView,
    ReviewDeleteView,
)

urlpatterns = [
    path('', ReviewListView.as_view(), name='reviews-list'),
    path('create/', ReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('<int:pk>/edit/', ReviewEditView.as_view(), name='review-edit'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),

    path('employee-reviews/', EmployeeReviewsListView.as_view(), name='employee-reviews-list'),
    path('employee-reviews/<int:pk>/', EmployeeReviewDetailView.as_view(), name='employee-review-detail'),
    path('employee-reviews/<int:pk>/edit/', EmployeeReviewEditView.as_view(), name='employee-review-edit'),
    path('employee-reviews/<int:pk>/delete/', EmployeeReviewDeleteView.as_view(), name='employee-review-delete'),
]
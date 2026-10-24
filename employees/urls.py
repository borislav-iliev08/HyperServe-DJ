from django.urls import path

from employees.views import EmployeeReviewCreateView, EmployeesCreateView, EmployeesDeleteView, EmployeesDetailsView, EmployeesEditView, EmployeesListView

urlpatterns = [
    path('', EmployeesListView.as_view(), name='employees-list'),
    path('create/', EmployeesCreateView.as_view(), name='employee-create'),
    path('<int:employee_pk>/reviews/create/', EmployeeReviewCreateView.as_view(), name='employee-review-create'),
    path('<int:pk>/', EmployeesDetailsView.as_view(), name='employee-detail'),
    path('<int:pk>/edit/', EmployeesEditView.as_view(), name='employee-edit'),
    path('<int:pk>/delete/', EmployeesDeleteView.as_view(), name='employee-delete'),
]
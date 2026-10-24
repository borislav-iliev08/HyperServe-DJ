"""
URL configuration for hyperservedj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve

from .views import custom_404, HomeView
from employees.views import EmployeeReviewDeleteView, EmployeeReviewDetailView, EmployeeReviewEditView, EmployeeReviewsListView

urlpatterns = [
    path('static/<path:path>', serve, {'document_root': settings.BASE_DIR / 'templates' / 'static'}),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('',HomeView.as_view(),name='home'),
    path('admin/', admin.site.urls),
    path('reviews/',include('reviews.urls')),
    path('restaurants/',include('restaurants.urls')),
    path('employees/',include('employees.urls')),
    path('employee-reviews/<int:pk>/delete/', EmployeeReviewDeleteView.as_view(), name='employee-review-delete'),
    path('employee-reviews/<int:pk>/edit/', EmployeeReviewEditView.as_view(), name='employee-review-edit'),
    path('employee-reviews/<int:pk>/', EmployeeReviewDetailView.as_view(), name='employee-review-detail'),
    path('employee-reviews/', EmployeeReviewsListView.as_view(), name='employee-reviews-list'),

]
handler404 = custom_404
from django.urls import include, path
from restaurants.views import (RestaurantCreateView,RestaurantDeleteView,RestaurantDetailView,RestaurantListView,RestaurantUpdateView,)

urlpatterns = [
    path('', RestaurantListView.as_view(), name='restaurants-list'),
    path('create/', RestaurantCreateView.as_view(), name='restaurant-create'),
    path('<slug:slug>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('<slug:slug>/edit/', RestaurantUpdateView.as_view(), name='restaurant-edit'),
    path('<slug:slug>/delete/', RestaurantDeleteView.as_view(), name='restaurant-delete'),
]
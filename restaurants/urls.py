from django.urls import path
from django.views import View

from restaurants.views import (
    RestaurantCreateView,
    RestaurantDeleteView,
    RestaurantDetailView,
    RestaurantListView,
    RestaurantUpdateView,
    CreatePerkView,
)

urlpatterns = [
    path('', RestaurantListView.as_view(), name='restaurants-list'),
    path('create/', RestaurantCreateView.as_view(), name='restaurant-create'),
    path('perk_create/', CreatePerkView.as_view(), name='perks-create'),
    path('<slug:slug>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('<slug:slug>/edit/', RestaurantUpdateView.as_view(), name='restaurant-edit'),
    path('<slug:slug>/delete/', RestaurantDeleteView.as_view(), name='restaurant-delete'),
]
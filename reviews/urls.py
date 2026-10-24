from django.urls import path

from reviews.views import ReviewDeleteView, ReviewDetailView, ReviewListView, ReviewCreateView, ReviewEditView

urlpatterns = [
    path('', ReviewListView.as_view(), name='reviews-list'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('create/',ReviewCreateView.as_view(),name='review-create'),
    path('<int:pk>/edit/',ReviewEditView.as_view(),name='review-edit'),
]
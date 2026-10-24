from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve

from .views import custom_404, HomeView

urlpatterns = [
    path('static/<path:path>', serve, {'document_root': settings.BASE_DIR / 'templates' / 'static'}),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),

    path('reviews/', include('reviews.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('employees/', include('employees.urls')),
]


handler404 = custom_404
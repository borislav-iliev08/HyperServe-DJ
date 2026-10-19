from django.urls import path
from restaurants import views

urlpatterns=[
    path('',views.index,name='home_test')

]
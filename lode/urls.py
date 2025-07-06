"""
URL configuration for lode app.
"""
from django.urls import path
from . import views

app_name = 'lode'

urlpatterns = [
    path('', views.index, name='index'),
    path('numbers/', views.numbers, name='numbers'),
    path('history/', views.history, name='history'),
] 
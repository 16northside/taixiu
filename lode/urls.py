"""
URL configuration for lode app.
"""
from django.urls import path
from . import views
from .views import PlaceBetView

app_name = 'lode'

urlpatterns = [
    path('', views.index, name='index'),
    path('numbers/', views.numbers, name='numbers'),
    path('history/', views.history, name='history'),
    path('place-bet/', PlaceBetView.as_view(), name='place-bet'),
] 
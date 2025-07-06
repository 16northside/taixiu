"""
URL configuration for bongda app.
"""
from django.urls import path
from . import views

app_name = 'bongda'

urlpatterns = [
    path('', views.index, name='index'),
    path('matches/', views.matches, name='matches'),
    path('results/', views.results, name='results'),
] 
from django.contrib import admin
from django.urls import path, include
from . import views  # Thêm import views

urlpatterns = [
    path('', views.home, name='home'),  # Thêm route cho trang chủ
    path('admin/', admin.site.urls),
    path('api/taixiu/', include('taixiu.urls')),
    path('api/bongda/', include('bongda.urls')),
    path('api/lode/', include('lode.urls')),
    path('api/users/', include('users.urls')),
]

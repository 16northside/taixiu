from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Thêm import views

urlpatterns = [
    path('', views.home, name='home'),  # Thêm route cho trang chủ
    path('admin-panel/', views.admin_panel, name='admin_panel'),  # Thêm route cho admin panel
    path('admin/', admin.site.urls),
    path('api/taixiu/', include('taixiu.urls')),
    path('api/bongda/', include('bongda.urls')),
    path('api/lode/', include('lode.urls')),
    path('api/users/', include('users.urls')),
]

# Serve static files trong development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

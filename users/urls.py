from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register, user_info, change_password
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', user_info, name='user_info'),
    path('change-password/', change_password, name='change_password'),
    
    # Admin APIs
    path('admin/users/', views.admin_user_list, name='admin_user_list'),
    path('admin/add-balance/', views.admin_add_balance, name='admin_add_balance'),
    path('admin/bulk-add-balance/', views.admin_bulk_add_balance, name='admin_bulk_add_balance'),
    path('admin/balance-logs/', views.admin_balance_logs, name='admin_balance_logs'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
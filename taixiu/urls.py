from rest_framework.routers import DefaultRouter
from .views import TaiXiuBetViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'bets', TaiXiuBetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

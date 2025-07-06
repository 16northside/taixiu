from rest_framework import viewsets
from .models import TaiXiuBet
from .serializers import TaiXiuBetSerializer

class TaiXiuBetViewSet(viewsets.ModelViewSet):
    queryset = TaiXiuBet.objects.all()
    serializer_class = TaiXiuBetSerializer

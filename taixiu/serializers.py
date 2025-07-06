from rest_framework import serializers
from .models import TaiXiuBet

class TaiXiuBetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaiXiuBet
        fields = '__all__'
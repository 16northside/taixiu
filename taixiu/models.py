from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class TaiXiuBet(models.Model):
    BET_CHOICES = [
        ('tai', 'Tài'),
        ('xiu', 'Xỉu')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    choice = models.CharField(choices=BET_CHOICES, max_length=10)
    result = models.CharField(max_length=10, blank=True, null=True)  # tai / xiu
    created_at = models.DateTimeField(auto_now_add=True)

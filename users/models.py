from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # Số dư tài khoản
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Model để log các thay đổi balance
class BalanceLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Số tiền')
    balance_before = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Số dư trước')
    balance_after = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Số dư sau')
    reason = models.CharField(max_length=255, verbose_name='Lý do')
    admin_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='balance_logs', verbose_name='Admin thực hiện')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian')
    
    class Meta:
        verbose_name = 'Log thay đổi số dư'
        verbose_name_plural = 'Log thay đổi số dư'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.amount:,.0f} VNĐ - {self.reason}"

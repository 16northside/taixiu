from django.db import models

# Create your models here.

class Team(models.Model):
    """Model cho đội bóng"""
    name = models.CharField(max_length=100, verbose_name="Tên đội")
    logo = models.URLField(blank=True, null=True, verbose_name="Logo đội")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Đội bóng"
        verbose_name_plural = "Đội bóng"

    def __str__(self):
        return self.name

class Match(models.Model):
    """Model cho trận đấu"""
    STATUS_CHOICES = [
        ('upcoming', 'Sắp diễn ra'),
        ('live', 'Đang diễn ra'),
        ('finished', 'Đã kết thúc'),
        ('cancelled', 'Đã hủy'),
    ]

    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches', verbose_name="Đội nhà")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches', verbose_name="Đội khách")
    match_date = models.DateTimeField(verbose_name="Ngày giờ trận đấu")
    home_score = models.IntegerField(default=0, verbose_name="Tỷ số đội nhà")
    away_score = models.IntegerField(default=0, verbose_name="Tỷ số đội khách")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming', verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Trận đấu"
        verbose_name_plural = "Trận đấu"
        ordering = ['-match_date']

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.match_date.strftime('%d/%m/%Y %H:%M')}"

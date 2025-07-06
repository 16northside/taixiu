from django.db import models

# Create your models here.

class LodeResult(models.Model):
    """Model cho kết quả lô đề"""
    REGION_CHOICES = [
        ('mien_bac', 'Miền Bắc'),
        ('mien_trung', 'Miền Trung'),
        ('mien_nam', 'Miền Nam'),
    ]

    date = models.DateField(verbose_name="Ngày xổ số")
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default='mien_bac', verbose_name="Miền")
    numbers = models.JSONField(verbose_name="Các số kết quả")  # Lưu dạng list các số
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Kết quả lô đề"
        verbose_name_plural = "Kết quả lô đề"
        ordering = ['-date']
        unique_together = ['date', 'region']

    def __str__(self):
        return f"Lô đề {self.region} - {self.date.strftime('%d/%m/%Y')}"

class LodeNumber(models.Model):
    """Model cho số lô đề"""
    number = models.IntegerField(verbose_name="Số lô đề")
    frequency = models.IntegerField(default=0, verbose_name="Tần suất xuất hiện")
    last_appearance = models.DateField(blank=True, null=True, verbose_name="Lần xuất hiện cuối")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Số lô đề"
        verbose_name_plural = "Số lô đề"
        ordering = ['number']

    def __str__(self):
        return f"Số {self.number:02d}"

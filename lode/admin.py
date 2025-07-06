from django.contrib import admin
from .models import LodeResult, LodeNumber

# Register your models here.

@admin.register(LodeResult)
class LodeResultAdmin(admin.ModelAdmin):
    list_display = ['date', 'region', 'numbers', 'created_at']
    list_filter = ['region', 'date']
    date_hierarchy = 'date'
    ordering = ['-date']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(LodeNumber)
class LodeNumberAdmin(admin.ModelAdmin):
    list_display = ['number', 'frequency', 'last_appearance']
    list_filter = ['last_appearance']
    search_fields = ['number']
    ordering = ['number']
    readonly_fields = ['created_at', 'updated_at']

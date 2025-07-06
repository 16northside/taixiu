from django.contrib import admin
from .models import Team, Match

# Register your models here.

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['created_at']
    ordering = ['name']

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['home_team', 'away_team', 'match_date', 'home_score', 'away_score', 'status']
    list_filter = ['status', 'match_date', 'home_team', 'away_team']
    search_fields = ['home_team__name', 'away_team__name']
    date_hierarchy = 'match_date'
    ordering = ['-match_date']

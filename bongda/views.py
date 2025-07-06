from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

def index(request):
    """Trang chủ của app bongda"""
    return JsonResponse({
        'message': 'Chào mừng đến với API Bóng Đá',
        'endpoints': {
            'matches': '/api/bongda/matches/',
            'results': '/api/bongda/results/'
        }
    })

@api_view(['GET'])
def matches(request):
    """API lấy danh sách trận đấu"""
    # Dữ liệu mẫu - sau này sẽ lấy từ database
    matches_data = [
        {
            'id': 1,
            'home_team': 'Manchester United',
            'away_team': 'Liverpool',
            'date': '2024-01-15',
            'time': '20:00',
            'status': 'upcoming'
        },
        {
            'id': 2,
            'home_team': 'Arsenal',
            'away_team': 'Chelsea',
            'date': '2024-01-16',
            'time': '19:30',
            'status': 'upcoming'
        }
    ]
    return Response({
        'success': True,
        'data': matches_data
    })

@api_view(['GET'])
def results(request):
    """API lấy kết quả trận đấu"""
    # Dữ liệu mẫu - sau này sẽ lấy từ database
    results_data = [
        {
            'id': 1,
            'home_team': 'Manchester City',
            'away_team': 'Tottenham',
            'home_score': 2,
            'away_score': 1,
            'date': '2024-01-14',
            'status': 'finished'
        },
        {
            'id': 2,
            'home_team': 'Barcelona',
            'away_team': 'Real Madrid',
            'home_score': 0,
            'away_score': 0,
            'date': '2024-01-13',
            'status': 'finished'
        }
    ]
    return Response({
        'success': True,
        'data': results_data
    })

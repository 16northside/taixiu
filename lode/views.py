from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random

# Create your views here.

def index(request):
    """Trang chủ của app lode"""
    return JsonResponse({
        'message': 'Chào mừng đến với API Lô Đề',
        'endpoints': {
            'numbers': '/api/lode/numbers/',
            'history': '/api/lode/history/'
        }
    })

@api_view(['GET'])
def numbers(request):
    """API lấy số lô đề hiện tại"""
    # Dữ liệu mẫu - sau này sẽ lấy từ database
    numbers_data = {
        'current_numbers': [
            random.randint(0, 99) for _ in range(10)
        ],
        'date': '2024-01-15',
        'region': 'Miền Bắc'
    }
    return Response({
        'success': True,
        'data': numbers_data
    })

@api_view(['GET'])
def history(request):
    """API lấy lịch sử kết quả lô đề"""
    # Dữ liệu mẫu - sau này sẽ lấy từ database
    history_data = [
        {
            'date': '2024-01-14',
            'numbers': [12, 34, 56, 78, 90, 23, 45, 67, 89, 1],
            'region': 'Miền Bắc'
        },
        {
            'date': '2024-01-13',
            'numbers': [11, 22, 33, 44, 55, 66, 77, 88, 99, 0],
            'region': 'Miền Bắc'
        }
    ]
    return Response({
        'success': True,
        'data': history_data
    })

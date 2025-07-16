from django.shortcuts import render
from django.http import HttpResponse
import os

def home(request):
    """Serve giao diện người dùng chính"""
    return render(request, 'index.html')

def admin_panel(request):
    """Serve trang admin panel"""
    return render(request, 'admin.html') 
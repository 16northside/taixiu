import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'white88_backend.settings')
django.setup()

from django.contrib.auth.models import User

def check_user():
    username = 'leviethai2'
    email = 'sdfjkds@gmail.com'
    
    print(f"🔍 Kiểm tra tài khoản: {username}")
    print(f"📧 Email: {email}")
    print("-" * 50)
    
    # Kiểm tra username
    try:
        user_by_username = User.objects.get(username=username)
        print(f"❌ Username '{username}' đã tồn tại!")
        print(f"   - ID: {user_by_username.id}")
        print(f"   - Email: {user_by_username.email}")
        print(f"   - Ngày tạo: {user_by_username.date_joined}")
        print(f"   - Active: {user_by_username.is_active}")
    except User.DoesNotExist:
        print(f"✅ Username '{username}' chưa tồn tại")
    
    print()
    
    # Kiểm tra email
    try:
        user_by_email = User.objects.get(email=email)
        print(f"❌ Email '{email}' đã tồn tại!")
        print(f"   - Username: {user_by_email.username}")
        print(f"   - ID: {user_by_email.id}")
        print(f"   - Ngày tạo: {user_by_email.date_joined}")
    except User.DoesNotExist:
        print(f"✅ Email '{email}' chưa tồn tại")
    
    print()
    
    # Thống kê tổng quan
    total_users = User.objects.count()
    print(f"📊 Tổng số users trong hệ thống: {total_users}")
    
    # Liệt kê 5 users gần nhất
    print("\n👥 5 users gần nhất:")
    recent_users = User.objects.order_by('-date_joined')[:5]
    for user in recent_users:
        print(f"   - {user.username} ({user.email}) - {user.date_joined}")

if __name__ == "__main__":
    check_user() 
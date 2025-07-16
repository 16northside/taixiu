#!/usr/bin/env python
"""
Script để tạo superuser mặc định cho White88 Admin Panel
Chạy: python create_admin.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'white88_backend.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.management import execute_from_command_line

def create_superuser():
    """Tạo superuser mặc định nếu chưa tồn tại"""
    
    # Thông tin admin mặc định
    username = 'admin'
    email = 'admin@white88.com'
    password = 'admin123456'
    
    try:
        # Kiểm tra xem user đã tồn tại chưa
        if User.objects.filter(username=username).exists():
            print(f"✅ User '{username}' đã tồn tại!")
            return
        
        # Tạo superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        print("🎉 Tạo superuser thành công!")
        print(f"👤 Username: {username}")
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")
        print("\n🔗 Truy cập Admin Panel:")
        print("   - Django Admin: http://localhost:8000/admin/")
        print("   - Custom Admin Panel: http://localhost:8000/admin-panel/")
        print("\n⚠️  Lưu ý: Hãy đổi mật khẩu sau khi đăng nhập lần đầu!")
        
    except Exception as e:
        print(f"❌ Lỗi khi tạo superuser: {e}")

def create_test_users():
    """Tạo một số test users để demo"""
    
    test_users = [
        {'username': 'user1', 'email': 'user1@test.com', 'password': 'test123'},
        {'username': 'user2', 'email': 'user2@test.com', 'password': 'test123'},
        {'username': 'user3', 'email': 'user3@test.com', 'password': 'test123'},
    ]
    
    created_count = 0
    for user_data in test_users:
        if not User.objects.filter(username=user_data['username']).exists():
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            created_count += 1
            print(f"✅ Tạo test user: {user_data['username']}")
    
    if created_count > 0:
        print(f"\n🎯 Đã tạo {created_count} test users")
        print("💡 Bạn có thể dùng các users này để test chức năng thêm tiền")
    else:
        print("ℹ️  Các test users đã tồn tại")

if __name__ == '__main__':
    print("🚀 White88 - Tạo Admin User")
    print("=" * 40)
    
    # Tạo superuser
    create_superuser()
    
    print("\n" + "=" * 40)
    
    # Tạo test users
    print("📝 Tạo test users...")
    create_test_users()
    
    print("\n" + "=" * 40)
    print("✨ Hoàn thành! Bạn có thể chạy server với lệnh:")
    print("   python manage.py runserver")
    print("\n🎯 Sau đó truy cập:")
    print("   - http://localhost:8000/ (Trang chủ)")
    print("   - http://localhost:8000/admin-panel/ (Admin Panel)")
    print("   - http://localhost:8000/admin/ (Django Admin)") 
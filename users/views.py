from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import transaction
from .models import Profile, BalanceLog
from .serializers import UserSerializer, ProfileSerializer, BalanceLogSerializer, RegisterSerializer
from django.contrib.auth.decorators import login_required, user_passes_test
from decimal import Decimal

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Đăng ký thành công!'}, status=status.HTTP_201_CREATED)
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    # Tự động tạo profile nếu user chưa có
    profile, created = Profile.objects.get_or_create(user=user)
    return Response({
        'username': user.username,
        'email': user.email,
        'balance': profile.balance
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not user.check_password(old_password):
        return Response({'success': False, 'message': 'Mật khẩu cũ không đúng!'}, status=status.HTTP_400_BAD_REQUEST)
    if not new_password or len(new_password) < 6:
        return Response({'success': False, 'message': 'Mật khẩu mới phải có ít nhất 6 ký tự!'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({'success': True, 'message': 'Đổi mật khẩu thành công!'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_user_list(request):
    """API để lấy danh sách users cho admin"""
    users = User.objects.all().order_by('username')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_add_balance(request):
    """API để thêm tiền cho user"""
    user_id = request.data.get('user_id')
    amount = request.data.get('amount')
    reason = request.data.get('reason', 'Thêm tiền thủ công')
    
    if not user_id or not amount:
        return Response({
            'error': 'Thiếu thông tin user_id hoặc amount'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=user_id)
        amount = Decimal(str(amount))
        
        if amount <= 0:
            return Response({
                'error': 'Số tiền phải lớn hơn 0'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            profile = user.profile
            old_balance = profile.balance
            profile.balance += amount
            profile.save()
            
            # Tạo log
            balance_log = BalanceLog.objects.create(
                user=user,
                amount=amount,
                balance_before=old_balance,
                balance_after=profile.balance,
                reason=reason,
                admin_user=request.user
            )
        
        return Response({
            'success': True,
            'message': f'Đã thêm {amount:,.0f} VNĐ cho user {user.username}',
            'user': UserSerializer(user).data,
            'balance_log': BalanceLogSerializer(balance_log).data
        })
        
    except User.DoesNotExist:
        return Response({
            'error': 'User không tồn tại'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_bulk_add_balance(request):
    """API để thêm tiền hàng loạt"""
    user_ids = request.data.get('user_ids', [])
    amount = request.data.get('amount')
    reason = request.data.get('reason', 'Thêm tiền hàng loạt')
    
    if not user_ids or not amount:
        return Response({
            'error': 'Thiếu thông tin user_ids hoặc amount'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        amount = Decimal(str(amount))
        if amount <= 0:
            return Response({
                'error': 'Số tiền phải lớn hơn 0'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        users = User.objects.filter(id__in=user_ids)
        if not users.exists():
            return Response({
                'error': 'Không tìm thấy users nào'
            }, status=status.HTTP_404_NOT_FOUND)
        
        balance_logs = []
        with transaction.atomic():
            for user in users:
                profile = user.profile
                old_balance = profile.balance
                profile.balance += amount
                profile.save()
                
                # Tạo log
                balance_log = BalanceLog.objects.create(
                    user=user,
                    amount=amount,
                    balance_before=old_balance,
                    balance_after=profile.balance,
                    reason=reason,
                    admin_user=request.user
                )
                balance_logs.append(balance_log)
        
        return Response({
            'success': True,
            'message': f'Đã thêm {amount:,.0f} VNĐ cho {users.count()} users',
            'users_count': users.count(),
            'balance_logs': BalanceLogSerializer(balance_logs, many=True).data
        })
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_balance_logs(request):
    """API để lấy lịch sử thay đổi balance"""
    logs = BalanceLog.objects.all().order_by('-created_at')
    serializer = BalanceLogSerializer(logs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard(request):
    """API để lấy thống kê cho admin dashboard"""
    total_users = User.objects.count()
    total_balance = sum([user.profile.balance for user in User.objects.all()])
    recent_logs = BalanceLog.objects.all().order_by('-created_at')[:10]
    
    return Response({
        'total_users': total_users,
        'total_balance': total_balance,
        'recent_logs': BalanceLogSerializer(recent_logs, many=True).data
    })
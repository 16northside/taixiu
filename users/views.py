from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer
from .models import Profile
from django.contrib.auth.models import User

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
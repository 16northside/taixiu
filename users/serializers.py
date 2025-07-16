from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, BalanceLog

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password','email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email',''),
            password=validated_data['password']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['balance']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'profile']
        read_only_fields = ['id', 'date_joined']

class BalanceLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    admin_user = UserSerializer(read_only=True)
    
    class Meta:
        model = BalanceLog
        fields = ['id', 'user', 'amount', 'balance_before', 'balance_after', 'reason', 'admin_user', 'created_at']
        read_only_fields = ['id', 'created_at']
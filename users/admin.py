from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Profile, BalanceLog

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Thông tin tài khoản'
    fields = ('balance',)
    readonly_fields = ('balance',)

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_balance', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    def get_balance(self, obj):
        try:
            return f"{obj.profile.balance:,.0f} VNĐ"
        except Profile.DoesNotExist:
            return "0 VNĐ"
    get_balance.short_description = 'Số dư'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add-balance/', self.admin_site.admin_view(self.add_balance_view), name='add-balance'),
            path('bulk-add-balance/', self.admin_site.admin_view(self.bulk_add_balance_view), name='bulk-add-balance'),
        ]
        return custom_urls + urls
    
    def add_balance_view(self, request):
        """Trang thêm tiền cho user cụ thể"""
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            amount = request.POST.get('amount')
            reason = request.POST.get('reason', 'Thêm tiền thủ công')
            
            try:
                user = User.objects.get(id=user_id)
                amount = float(amount)
                
                with transaction.atomic():
                    profile = user.profile
                    profile.balance += amount
                    profile.save()
                    
                    # Tạo log cho việc thêm tiền
                    BalanceLog.objects.create(
                        user=user,
                        amount=amount,
                        balance_before=profile.balance - amount,
                        balance_after=profile.balance,
                        reason=reason,
                        admin_user=request.user
                    )
                
                messages.success(request, f'Đã thêm {amount:,.0f} VNĐ cho user {user.username}')
                return redirect('admin:auth_user_changelist')
                
            except (User.DoesNotExist, ValueError) as e:
                messages.error(request, f'Lỗi: {str(e)}')
        
        users = User.objects.all().order_by('username')
        return render(request, 'admin/users/add_balance.html', {
            'users': users,
            'title': 'Thêm tiền cho User'
        })
    
    def bulk_add_balance_view(self, request):
        """Trang thêm tiền hàng loạt"""
        if request.method == 'POST':
            user_ids = request.POST.getlist('user_ids')
            amount = request.POST.get('amount')
            reason = request.POST.get('reason', 'Thêm tiền hàng loạt')
            
            try:
                amount = float(amount)
                users = User.objects.filter(id__in=user_ids)
                
                with transaction.atomic():
                    for user in users:
                        profile = user.profile
                        old_balance = profile.balance
                        profile.balance += amount
                        profile.save()
                        
                        # Tạo log cho việc thêm tiền
                        BalanceLog.objects.create(
                            user=user,
                            amount=amount,
                            balance_before=old_balance,
                            balance_after=profile.balance,
                            reason=reason,
                            admin_user=request.user
                        )
                
                messages.success(request, f'Đã thêm {amount:,.0f} VNĐ cho {users.count()} users')
                return redirect('admin:auth_user_changelist')
                
            except ValueError as e:
                messages.error(request, f'Lỗi: {str(e)}')
        
        users = User.objects.all().order_by('username')
        return render(request, 'admin/users/bulk_add_balance.html', {
            'users': users,
            'title': 'Thêm tiền hàng loạt'
        })

class BalanceLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'balance_before', 'balance_after', 'reason', 'admin_user', 'created_at')
    list_filter = ('created_at', 'admin_user', 'reason')
    search_fields = ('user__username', 'user__email', 'reason')
    readonly_fields = ('user', 'amount', 'balance_before', 'balance_after', 'admin_user', 'created_at')
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False  # Không cho phép thêm thủ công
    
    def has_change_permission(self, request, obj=None):
        return False  # Không cho phép chỉnh sửa

# Đăng ký models
admin.site.unregister(User)  # Hủy đăng ký User mặc định
admin.site.register(User, UserAdmin)  # Đăng ký lại với UserAdmin tùy chỉnh
admin.site.register(BalanceLog, BalanceLogAdmin)

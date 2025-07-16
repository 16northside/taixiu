# Hướng dẫn sử dụng Admin Panel - White88

## Tổng quan

Admin Panel là hệ thống quản lý toàn diện cho White88, cho phép admin thực hiện các thao tác quản lý user và balance một cách dễ dàng và an toàn.

## Tính năng chính

### 1. Dashboard

- **Thống kê tổng quan**: Hiển thị tổng số users, tổng số dư, users hoạt động, tổng giao dịch
- **Giao dịch gần đây**: Xem 10 giao dịch thay đổi balance mới nhất
- **Giao diện trực quan**: Sử dụng biểu đồ và card để hiển thị thông tin

### 2. Quản lý Users

- **Danh sách users**: Xem tất cả users trong hệ thống
- **Tìm kiếm**: Tìm kiếm user theo username hoặc email
- **Thông tin chi tiết**: Hiển thị thông tin user và số dư hiện tại
- **Thêm tiền nhanh**: Nút thêm tiền trực tiếp từ danh sách users

### 3. Thêm tiền cho User

- **Chọn user**: Dropdown để chọn user cụ thể
- **Nhập số tiền**: Input số tiền cần thêm
- **Lý do**: Ghi chú lý do thêm tiền
- **Xác nhận**: Hiển thị thông tin user và số dư trước khi thêm

### 4. Thêm tiền hàng loạt

- **Chọn nhiều users**: Checkbox để chọn nhiều users cùng lúc
- **Select all**: Chọn tất cả users
- **Số tiền đồng nhất**: Thêm cùng một số tiền cho tất cả users được chọn
- **Lý do chung**: Ghi chú lý do cho tất cả giao dịch

### 5. Lịch sử giao dịch

- **Xem tất cả giao dịch**: Danh sách đầy đủ các thay đổi balance
- **Thông tin chi tiết**: User, số tiền, số dư trước/sau, lý do, admin thực hiện, thời gian
- **Sắp xếp**: Theo thời gian mới nhất

## Cách sử dụng

### Truy cập Admin Panel

1. **URL**: `http://localhost:8000/admin-panel/`
2. **Yêu cầu**: Phải đăng nhập với tài khoản admin (is_staff=True)

### Thêm tiền cho User

1. Vào tab "Thêm tiền"
2. Chọn user từ dropdown
3. Nhập số tiền cần thêm
4. Ghi lý do (tùy chọn)
5. Nhấn "Thêm tiền"

### Thêm tiền hàng loạt

1. Vào tab "Thêm tiền hàng loạt"
2. Chọn các users cần thêm tiền (hoặc dùng "Chọn tất cả")
3. Nhập số tiền cho mỗi user
4. Ghi lý do chung
5. Nhấn "Thêm tiền hàng loạt"

### Xem lịch sử giao dịch

1. Vào tab "Lịch sử giao dịch"
2. Xem danh sách tất cả giao dịch
3. Thông tin hiển thị: User, số tiền, số dư trước/sau, lý do, admin, thời gian

## Bảo mật

### Authentication

- Chỉ admin users (is_staff=True) mới có thể truy cập
- Sử dụng Django's built-in authentication system
- Session-based authentication

### Authorization

- API endpoints được bảo vệ bởi `@permission_classes([IsAdminUser])`
- Chỉ admin mới có thể thực hiện các thao tác thay đổi balance

### Logging

- Tất cả thay đổi balance được log trong model `BalanceLog`
- Lưu trữ: user, số tiền, số dư trước/sau, lý do, admin thực hiện, thời gian
- Không thể xóa hoặc chỉnh sửa log

## API Endpoints

### Admin APIs

- `GET /api/users/admin/users/` - Lấy danh sách users
- `POST /api/users/admin/add-balance/` - Thêm tiền cho user
- `POST /api/users/admin/bulk-add-balance/` - Thêm tiền hàng loạt
- `GET /api/users/admin/balance-logs/` - Lấy lịch sử giao dịch
- `GET /api/users/admin/dashboard/` - Lấy thống kê dashboard

### Request/Response Examples

#### Thêm tiền cho user

```json
POST /api/users/admin/add-balance/
{
    "user_id": 1,
    "amount": 100000,
    "reason": "Thêm tiền thủ công"
}

Response:
{
    "success": true,
    "message": "Đã thêm 100,000 VNĐ cho user username",
    "user": {...},
    "balance_log": {...}
}
```

#### Thêm tiền hàng loạt

```json
POST /api/users/admin/bulk-add-balance/
{
    "user_ids": [1, 2, 3],
    "amount": 50000,
    "reason": "Thêm tiền hàng loạt"
}

Response:
{
    "success": true,
    "message": "Đã thêm 50,000 VNĐ cho 3 users",
    "users_count": 3,
    "balance_logs": [...]
}
```

## Cấu trúc Database

### Models

#### Profile

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
```

#### BalanceLog

```python
class BalanceLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_before = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.CharField(max_length=255)
    admin_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Troubleshooting

### Lỗi thường gặp

1. **"Lỗi kết nối API"**

   - Kiểm tra server Django có đang chạy không
   - Kiểm tra URL API có đúng không
   - Kiểm tra CORS settings

2. **"User không tồn tại"**

   - Kiểm tra user_id có đúng không
   - Đảm bảo user đã được tạo trong database

3. **"Số tiền không hợp lệ"**
   - Đảm bảo số tiền là số dương
   - Kiểm tra định dạng số

### Debug

1. **Console logs**: Mở Developer Tools để xem console logs
2. **Network tab**: Kiểm tra API requests/responses
3. **Django logs**: Xem logs trong terminal chạy Django server

## Phát triển thêm

### Tính năng có thể thêm

1. **Export data**: Xuất danh sách users/giao dịch ra Excel/CSV
2. **Filtering**: Lọc giao dịch theo thời gian, user, admin
3. **Pagination**: Phân trang cho danh sách dài
4. **Real-time updates**: WebSocket để cập nhật real-time
5. **Charts**: Biểu đồ thống kê chi tiết
6. **User management**: Thêm/sửa/xóa users
7. **Role-based access**: Phân quyền chi tiết hơn

### Cải thiện UI/UX

1. **Dark mode**: Chế độ tối
2. **Mobile responsive**: Tối ưu cho mobile
3. **Keyboard shortcuts**: Phím tắt
4. **Drag & drop**: Kéo thả để chọn users
5. **Auto-save**: Tự động lưu form

## Kết luận

Admin Panel cung cấp một giao diện hoàn chỉnh và dễ sử dụng để quản lý users và balance trong hệ thống White88. Với các tính năng bảo mật và logging đầy đủ, admin có thể thực hiện các thao tác một cách an toàn và có thể theo dõi được.

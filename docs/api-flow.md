# Tài liệu luồng API & Giải thích mã nguồn White88

> **Cập nhật:** 2024-07-07

---

## 1. Tổng quan hệ thống

- Ứng dụng White88 gồm các module: User/Auth, Tài Xỉu, Bóng Đá, Lô Đề, Admin Dashboard.
- Backend sử dụng Django + Django REST Framework.
- Phân quyền rõ ràng: User thường, Admin.
- Sử dụng JWT cho xác thực (login, token refresh).

---

## 2. Luồng API User & Auth

### 2.1. Đăng ký tài khoản

- **Endpoint:** `POST /api/users/register/`
- **Request:** `{ username, email, password }`
- **Xử lý:**
  - Nhận dữ liệu, validate qua `RegisterSerializer`.
  - Nếu hợp lệ, tạo user mới, trả về `{ success: true, message }`.
  - Nếu lỗi, trả về `{ success: false, errors }`.

### 2.2. Đăng nhập (JWT)

- **Endpoint:** `POST /api/users/login/`
- **Request:** `{ username, password }`
- **Xử lý:**
  - Sử dụng `TokenObtainPairView` của DRF SimpleJWT.
  - Trả về `{ access, refresh }` token nếu thành công.

### 2.3. Lấy thông tin user

- **Endpoint:** `GET /api/users/me/`
- **Yêu cầu:** Header `Authorization: Bearer <token>`
- **Xử lý:**
  - Lấy user từ request, tự động tạo profile nếu chưa có.
  - Trả về `{ username, email, balance }`.

### 2.4. Đổi mật khẩu

- **Endpoint:** `POST /api/users/change-password/`
- **Yêu cầu:** Header `Authorization: Bearer <token>`
- **Request:** `{ old_password, new_password }`
- **Xử lý:**
  - Kiểm tra mật khẩu cũ, validate mật khẩu mới.
  - Đổi mật khẩu, trả về `{ success, message }`.

---

## 3. Luồng API Admin

### 3.1. Lấy danh sách user

- **Endpoint:** `GET /api/users/admin/users/`
- **Yêu cầu:** Admin, JWT
- **Xử lý:**
  - Trả về danh sách user (serialize).

### 3.2. Thêm tiền cho user

- **Endpoint:** `POST /api/users/admin/add-balance/`
- **Yêu cầu:** Admin, JWT
- **Request:** `{ user_id, amount, reason }`
- **Xử lý:**
  - Kiểm tra user, validate amount.
  - Cộng tiền vào balance, tạo log giao dịch.
  - Trả về thông tin user và log.

### 3.3. Thêm tiền hàng loạt

- **Endpoint:** `POST /api/users/admin/bulk-add-balance/`
- **Request:** `{ user_ids, amount, reason }`
- **Xử lý:**
  - Lặp qua danh sách user, cộng tiền, tạo log cho từng user.

### 3.4. Lấy lịch sử thay đổi balance

- **Endpoint:** `GET /api/users/admin/balance-logs/`
- **Xử lý:**
  - Trả về danh sách log cộng/trừ tiền.

### 3.5. Dashboard thống kê

- **Endpoint:** `GET /api/users/admin/dashboard/`
- **Xử lý:**
  - Trả về tổng số user, tổng số dư, 10 log gần nhất.

---

## 4. Luồng API Game: Tài Xỉu

### 4.1. Đặt cược tài xỉu

- **Endpoint:** `POST /api/taixiu/bets/`
- **Yêu cầu:** JWT
- **Request:** `{ ... }` (theo model TaiXiuBet)
- **Xử lý:**
  - Sử dụng `TaiXiuBetViewSet` (ModelViewSet): CRUD cho bảng cược tài xỉu.
  - Validate, lưu cược, trả về thông tin bet.

### 4.2. Lấy danh sách cược

- **Endpoint:** `GET /api/taixiu/bets/`
- **Xử lý:**
  - Trả về danh sách tất cả cược tài xỉu.

---

## 5. Luồng API Game: Bóng Đá

### 5.1. Lấy danh sách trận đấu

- **Endpoint:** `GET /api/bongda/matches/`
- **Xử lý:**
  - Trả về danh sách trận đấu (dữ liệu mẫu hoặc từ DB).

### 5.2. Lấy kết quả trận đấu

- **Endpoint:** `GET /api/bongda/results/`
- **Xử lý:**
  - Trả về kết quả các trận đã diễn ra.

---

## 6. Luồng API Game: Lô Đề

### 6.1. Lấy số lô đề hiện tại

- **Endpoint:** `GET /api/lode/numbers/`
- **Xử lý:**
  - Trả về 10 số ngẫu nhiên, ngày, miền (dữ liệu mẫu hoặc từ DB).

### 6.2. Lấy lịch sử kết quả lô đề

- **Endpoint:** `GET /api/lode/history/`
- **Xử lý:**
  - Trả về danh sách kết quả các ngày trước.

---

## 7. Giải thích chi tiết từng dòng lệnh chính

### 7.1. User/Auth

- `@api_view(['POST'])` định nghĩa API nhận POST.
- `@permission_classes([IsAuthenticated])` yêu cầu JWT hợp lệ.
- `serializer = RegisterSerializer(data=request.data)` kiểm tra dữ liệu đầu vào.
- `user.set_password(new_password)` đổi mật khẩu an toàn (hash).
- `Profile.objects.get_or_create(user=user)` tự động tạo profile nếu chưa có.

### 7.2. Admin

- `@permission_classes([IsAdminUser])` chỉ cho phép admin truy cập.
- `with transaction.atomic():` đảm bảo cộng tiền/log là 1 giao dịch an toàn.
- `BalanceLog.objects.create(...)` lưu lại lịch sử cộng tiền.

### 7.3. Game

- `ModelViewSet` cho phép CRUD tự động với model (Tài Xỉu).
- `@api_view(['GET'])` định nghĩa API GET đơn giản (Bóng Đá, Lô Đề).
- Dữ liệu trả về dạng `{ success: True, data: ... }`.

---

## 8. Authentication & Phân quyền

- Đăng nhập trả về JWT, các API cần xác thực phải gửi header `Authorization: Bearer <token>`.
- Các API admin yêu cầu user phải có quyền admin (`is_staff=True`).

---

## 9. Ví dụ mẫu request/response

### Đăng ký user

```http
POST /api/users/register/
{
  "username": "nam88",
  "email": "nam88@gmail.com",
  "password": "123456"
}
=> { "success": true, "message": "Đăng ký thành công!" }
```

### Đăng nhập lấy token

```http
POST /api/users/login/
{
  "username": "nam88",
  "password": "123456"
}
=> { "access": "...", "refresh": "..." }
```

### Lấy số lô đề

```http
GET /api/lode/numbers/
=> { "success": true, "data": { "current_numbers": [12,34,...], "date": "2024-01-15", "region": "Miền Bắc" } }
```

---

## 10. Ghi chú

- Các API mẫu có thể trả về dữ liệu mẫu nếu chưa kết nối DB thực tế.
- Có thể mở rộng thêm các API khác theo nhu cầu.

---

**Mọi thắc mắc về luồng API hoặc mã nguồn, liên hệ admin để được giải đáp chi tiết!**

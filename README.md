# White88 Backend

Backend API cho ứng dụng White88 với các tính năng: Tài Xỉu, Bóng Đá, và Lô Đề.

## Cài đặt

1. Cài đặt dependencies:

```bash
pip install -r requirements.txt
```

2. Chạy migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. Tạo superuser (tùy chọn):

```bash
python manage.py createsuperuser
```

4. Chạy server:

```bash
python manage.py runserver
```

## API Endpoints

### Tài Xỉu

- `GET /api/taixiu/` - Trang chủ Tài Xỉu
- `GET /api/taixiu/game/` - Thông tin game hiện tại
- `POST /api/taixiu/bet/` - Đặt cược

### Bóng Đá

- `GET /api/bongda/` - Trang chủ Bóng Đá
- `GET /api/bongda/matches/` - Danh sách trận đấu
- `GET /api/bongda/results/` - Kết quả trận đấu

### Lô Đề

- `GET /api/lode/` - Trang chủ Lô Đề
- `GET /api/lode/numbers/` - Số lô đề hiện tại
- `GET /api/lode/history/` - Lịch sử kết quả

## Admin Panel

Truy cập Django Admin tại: `http://localhost:8000/admin/`

## Cấu trúc Project

```
white88/
├── bongda/          # App Bóng Đá
├── lode/            # App Lô Đề
├── taixiu/          # App Tài Xỉu
├── users/           # App Users
└── white88_backend/ # Project settings
```

## Models

### Bóng Đá

- `Team`: Đội bóng
- `Match`: Trận đấu

### Lô Đề

- `LodeResult`: Kết quả lô đề
- `LodeNumber`: Số lô đề

### Tài Xỉu

- `Game`: Thông tin game
- `Bet`: Thông tin cược

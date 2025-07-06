# White88 Frontend

Giao diện người dùng cho ứng dụng White88 được xây dựng bằng Vue.js 3.

## Tính năng

- **Tài Xỉu**: Hiển thị thông tin game và trạng thái
- **Bóng Đá**: Danh sách trận đấu và kết quả
- **Lô Đề**: Số hiện tại và lịch sử kết quả

## Cách sử dụng

1. Đảm bảo backend Django đang chạy trên `http://127.0.0.1:8000/`

2. Mở file `index.html` trong trình duyệt web

3. Hoặc sử dụng live server:

   ```bash
   # Nếu có Python
   python -m http.server 8080

   # Nếu có Node.js
   npx live-server
   ```

## Cấu trúc

```
frontend/
├── index.html      # File HTML chính
├── styles.css      # CSS styles
├── app.js          # Vue.js logic
└── README.md       # Hướng dẫn này
```

## API Endpoints

Frontend gọi các API sau từ backend:

- `GET /api/taixiu/` - Thông tin Tài Xỉu
- `GET /api/bongda/matches/` - Trận đấu
- `GET /api/bongda/results/` - Kết quả
- `GET /api/lode/numbers/` - Số lô đề
- `GET /api/lode/history/` - Lịch sử

## Tùy chỉnh

- Thay đổi màu sắc trong `styles.css`
- Thêm tính năng mới trong `app.js`
- Cập nhật giao diện trong `index.html`

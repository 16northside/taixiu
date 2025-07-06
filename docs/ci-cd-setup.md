# Hướng dẫn thiết lập CI/CD cho White88

## Tổng quan

Hệ thống CI/CD này sử dụng GitHub Actions để tự động hóa quá trình test, build và deploy cho cả backend Django và frontend Vue.js.

## Cấu trúc CI/CD

### 1. Backend CI/CD (`.github/workflows/backend-ci.yml`)

**Trigger:**

- Push/Pull Request vào branches `main` hoặc `develop`
- Chỉ khi có thay đổi trong các file Python hoặc backend

**Jobs:**

- **Test**: Chạy unit tests với PostgreSQL, security checks
- **Lint**: Kiểm tra code style với flake8, black, isort
- **Build**: Tạo build artifact cho deployment

### 2. Frontend CI/CD (`.github/workflows/frontend-ci.yml`)

**Trigger:**

- Push/Pull Request vào branches `main` hoặc `develop`
- Chỉ khi có thay đổi trong thư mục `frontend/`

**Jobs:**

- **Lint**: Kiểm tra code style với ESLint
- **Test**: Chạy unit tests với Vitest
- **Build**: Tạo build artifact cho deployment

### 3. Deploy (`.github/workflows/deploy.yml`)

**Trigger:**

- Khi cả backend và frontend CI thành công
- Chỉ trên branch `main`

**Jobs:**

- **Deploy**: Deploy lên server production

## Thiết lập GitHub Secrets

### 1. Secrets cho VPS/Server deployment

```bash
# SSH connection
HOST=your-server-ip
USERNAME=your-username
SSH_KEY=your-private-ssh-key
PORT=22

# Django settings
SECRET_KEY=your-django-secret-key

# Notification
SLACK_WEBHOOK=your-slack-webhook-url
```

### 2. Secrets cho Heroku deployment

```bash
HEROKU_API_KEY=your-heroku-api-key
HEROKU_APP_NAME=your-app-name
HEROKU_EMAIL=your-email
```

### 3. Secrets cho Railway deployment

```bash
RAILWAY_TOKEN=your-railway-token
RAILWAY_SERVICE=your-service-name
```

## Cài đặt trên Server

### 1. Chuẩn bị server

```bash
# Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# Cài đặt dependencies
sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx postgresql postgresql-contrib git curl

# Tạo user cho ứng dụng
sudo useradd -m -s /bin/bash white88
sudo usermod -aG sudo white88
```

### 2. Cài đặt PostgreSQL

```bash
# Tạo database và user
sudo -u postgres psql

CREATE DATABASE white88_db;
CREATE USER white88_user WITH PASSWORD 'white88_password';
GRANT ALL PRIVILEGES ON DATABASE white88_db TO white88_user;
\q
```

### 3. Clone và setup project

```bash
# Clone repository
sudo mkdir -p /var/www
sudo chown white88:white88 /var/www
cd /var/www
git clone https://github.com/your-username/white88.git
cd white88

# Setup backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# Setup frontend
cd frontend
npm install
npm run build
```

### 4. Cài đặt systemd services

```bash
# Copy service files
sudo cp systemd/white88-backend.service /etc/systemd/system/
sudo cp systemd/white88-frontend.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable white88-backend
sudo systemctl enable white88-frontend

# Start services
sudo systemctl start white88-backend
sudo systemctl start white88-frontend
```

### 5. Cấu hình Nginx

```bash
# Copy nginx config
sudo cp nginx/nginx.conf /etc/nginx/sites-available/white88
sudo ln -s /etc/nginx/sites-available/white88 /etc/nginx/sites-enabled/

# Test và restart nginx
sudo nginx -t
sudo systemctl restart nginx
```

## Sử dụng Docker

### 1. Build và chạy với Docker Compose

```bash
# Build images
docker-compose build

# Chạy services
docker-compose up -d

# Xem logs
docker-compose logs -f
```

### 2. Deploy với Docker

```bash
# Build production images
docker build -t white88-backend .
docker build -t white88-frontend ./frontend

# Push to registry (optional)
docker tag white88-backend your-registry/white88-backend:latest
docker push your-registry/white88-backend:latest
```

## Monitoring và Logging

### 1. Systemd logs

```bash
# Xem logs backend
sudo journalctl -u white88-backend -f

# Xem logs frontend
sudo journalctl -u white88-frontend -f
```

### 2. Application logs

```bash
# Backend logs
tail -f /var/log/white88/deploy.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 3. Health checks

```bash
# Kiểm tra backend
curl http://localhost:8000/api/health/

# Kiểm tra frontend
curl http://localhost:3000/

# Kiểm tra nginx
curl http://localhost/
```

## Backup và Recovery

### 1. Database backup

```bash
# Tạo backup script
sudo nano /usr/local/bin/backup-db.sh

#!/bin/bash
BACKUP_DIR="/var/backups/white88"
DATE=$(date +%Y%m%d_%H%M%S)
sudo -u postgres pg_dump white88_db > $BACKUP_DIR/db_backup_$DATE.sql

# Chạy backup hàng ngày
sudo crontab -e
# Thêm dòng: 0 2 * * * /usr/local/bin/backup-db.sh
```

### 2. Application backup

```bash
# Backup toàn bộ ứng dụng
sudo /var/www/white88/deploy.sh backup

# Restore từ backup
sudo /var/www/white88/deploy.sh rollback
```

## Troubleshooting

### 1. Lỗi thường gặp

**Backend không start:**

```bash
# Kiểm tra logs
sudo journalctl -u white88-backend -n 50

# Kiểm tra permissions
sudo chown -R www-data:www-data /var/www/white88
```

**Frontend không build:**

```bash
# Kiểm tra Node.js version
node --version

# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Database connection error:**

```bash
# Kiểm tra PostgreSQL
sudo systemctl status postgresql

# Test connection
psql -h localhost -U white88_user -d white88_db
```

### 2. Performance optimization

**Backend:**

- Tăng số workers trong gunicorn
- Sử dụng Redis cache
- Optimize database queries

**Frontend:**

- Enable gzip compression
- Minify assets
- Use CDN for static files

## Security

### 1. Firewall

```bash
# Cấu hình UFW
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. SSL/TLS

```bash
# Cài đặt Certbot
sudo apt install certbot python3-certbot-nginx

# Tạo certificate
sudo certbot --nginx -d your-domain.com
```

### 3. Environment variables

```bash
# Tạo file .env
sudo nano /var/www/white88/.env

SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://white88_user:password@localhost:5432/white88_db
```

## Kết luận

Hệ thống CI/CD này cung cấp:

- ✅ Tự động test và build
- ✅ Deploy tự động
- ✅ Rollback khi có lỗi
- ✅ Monitoring và logging
- ✅ Backup và recovery
- ✅ Security best practices

Để bắt đầu sử dụng, hãy:

1. Push code lên GitHub
2. Cấu hình GitHub Secrets
3. Setup server theo hướng dẫn
4. Test deployment

Mọi thắc mắc vui lòng liên hệ team development!

#!/bin/bash

# Script deploy tự động cho White88
set -e

echo "🚀 Bắt đầu deploy White88..."

# Biến môi trường
APP_NAME="white88"
APP_DIR="/var/www/$APP_NAME"
BACKUP_DIR="/var/backups/$APP_NAME"
LOG_FILE="/var/log/$APP_NAME/deploy.log"

# Tạo thư mục log nếu chưa có
mkdir -p /var/log/$APP_NAME

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# Backup function
backup() {
    log "📦 Tạo backup..."
    BACKUP_NAME="${APP_NAME}_backup_$(date +%Y%m%d_%H%M%S)"
    sudo cp -r $APP_DIR $BACKUP_DIR/$BACKUP_NAME
    log "✅ Backup đã tạo: $BACKUP_DIR/$BACKUP_NAME"
}

# Stop services
stop_services() {
    log "🛑 Dừng services..."
    sudo systemctl stop $APP_NAME-backend || true
    sudo systemctl stop $APP_NAME-frontend || true
    sudo systemctl stop nginx || true
}

# Start services
start_services() {
    log "▶️ Khởi động services..."
    sudo systemctl start $APP_NAME-backend
    sudo systemctl start $APP_NAME-frontend
    sudo systemctl start nginx
}

# Update code
update_code() {
    log "📥 Cập nhật code..."
    cd $APP_DIR
    git fetch origin
    git reset --hard origin/main
    log "✅ Code đã được cập nhật"
}

# Update backend
update_backend() {
    log "🔧 Cập nhật backend..."
    cd $APP_DIR
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Run migrations
    python manage.py migrate
    
    # Collect static files
    python manage.py collectstatic --noinput
    
    log "✅ Backend đã được cập nhật"
}

# Update frontend
update_frontend() {
    log "🎨 Cập nhật frontend..."
    cd $APP_DIR/frontend
    
    # Install dependencies
    npm install
    
    # Build
    npm run build
    
    log "✅ Frontend đã được cập nhật"
}

# Health check
health_check() {
    log "🏥 Kiểm tra sức khỏe ứng dụng..."
    
    # Wait for services to start
    sleep 10
    
    # Check backend
    if curl -f http://localhost:8000/api/health/ > /dev/null 2>&1; then
        log "✅ Backend hoạt động bình thường"
    else
        log "❌ Backend không phản hồi"
        return 1
    fi
    
    # Check frontend
    if curl -f http://localhost:3000/ > /dev/null 2>&1; then
        log "✅ Frontend hoạt động bình thường"
    else
        log "❌ Frontend không phản hồi"
        return 1
    fi
    
    log "🎉 Deploy thành công!"
}

# Rollback function
rollback() {
    log "🔄 Rollback về phiên bản trước..."
    
    # Find latest backup
    LATEST_BACKUP=$(ls -t $BACKUP_DIR | head -1)
    
    if [ -z "$LATEST_BACKUP" ]; then
        log "❌ Không tìm thấy backup để rollback"
        return 1
    fi
    
    # Stop services
    stop_services
    
    # Restore from backup
    sudo rm -rf $APP_DIR
    sudo cp -r $BACKUP_DIR/$LATEST_BACKUP $APP_DIR
    
    # Start services
    start_services
    
    log "✅ Rollback thành công từ: $LATEST_BACKUP"
}

# Main deploy process
main() {
    log "=== BẮT ĐẦU DEPLOY ==="
    
    # Check if running as root
    if [ "$EUID" -ne 0 ]; then
        log "❌ Script phải chạy với quyền root"
        exit 1
    fi
    
    # Backup current version
    backup
    
    # Stop services
    stop_services
    
    # Update code
    update_code
    
    # Update backend
    update_backend
    
    # Update frontend
    update_frontend
    
    # Start services
    start_services
    
    # Health check
    if health_check; then
        log "=== DEPLOY THÀNH CÔNG ==="
    else
        log "❌ Health check thất bại, thực hiện rollback..."
        rollback
        log "=== DEPLOY THẤT BẠI ==="
        exit 1
    fi
}

# Handle arguments
case "$1" in
    "deploy")
        main
        ;;
    "rollback")
        rollback
        ;;
    "health")
        health_check
        ;;
    *)
        echo "Usage: $0 {deploy|rollback|health}"
        exit 1
        ;;
esac 
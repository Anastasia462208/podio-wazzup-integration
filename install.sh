#!/bin/bash
# Скрипт быстрой установки интеграции Podio-Wazzup

set -e

echo "🚀 Установка интеграции Podio-Wazzup"
echo "===================================="

# Обновление системы
echo "📦 Обновление системы..."
apt update && apt upgrade -y

# Установка зависимостей
echo "📦 Установка зависимостей..."
apt install python3 python3-pip python3-venv nginx supervisor curl -y

# Создание рабочей директории
echo "📁 Создание рабочей директории..."
mkdir -p /opt/podio-wazzup-integration
cd /opt/podio-wazzup-integration

# Создание виртуального окружения
echo "🐍 Настройка Python окружения..."
python3 -m venv venv
source venv/bin/activate

# Установка Python пакетов
pip install flask requests

# Создание конфигурации Nginx
echo "🌐 Настройка Nginx..."
cat > /etc/nginx/sites-available/podio-wazzup << 'EOF'
server {
    listen 80;
    server_name 84.21.189.73;
    
    location /webhook/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location / {
        return 200 "Podio-Wazzup Integration Server";
        add_header Content-Type text/plain;
    }
}
EOF

# Активация конфигурации Nginx
ln -sf /etc/nginx/sites-available/podio-wazzup /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
systemctl enable nginx

# Создание конфигурации Supervisor
echo "🔄 Настройка автозапуска..."
cat > /etc/supervisor/conf.d/podio-wazzup.conf << 'EOF'
[program:podio-wazzup-integration]
command=/opt/podio-wazzup-integration/venv/bin/python /opt/podio-wazzup-integration/hybrid_integration.py
directory=/opt/podio-wazzup-integration
user=root
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/podio-wazzup-integration.log
environment=PYTHONPATH="/opt/podio-wazzup-integration"
EOF

# Создание базовых файлов конфигурации
echo "⚙️ Создание базовой конфигурации..."
cat > /opt/podio-wazzup-integration/integration_config.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Конфигурация для интеграции Podio-Wazzup
"""

# Podio API настройки
PODIO_CONFIG = {
    'client_id': 'wazzup-integration',
    'client_secret': 'FHN19OHsXbcWT74ns9qNt3goMK5JOSKCiPwqkKQQY3omYbRhEYuyQo7nG3k3LEzY',
    'username': 'blinpavlin0@gmail.com',
    'password': '326848atlantida!A',
    
    # App IDs (обновите после получения реальных значений)
    'messages_app_id': 'UNKNOWN',
    'contacts_app_id': 'UNKNOWN',
    'deals_app_id': 'UNKNOWN',
    
    'space_url': 'shturm-j361z6sagw/chat',
}

# Wazzup API настройки
WAZZUP_CONFIG = {
    'api_token': '1aab54ad811540da85bedbc685f938d6',
    'base_url': 'https://api.wazzup24.com/v3',
}

# Настройки интеграции
INTEGRATION_CONFIG = {
    'polling_interval': 120,  # 2 минуты
    'send_commands': ['@send', '@отправить', '@wazzup', '@клиент'],
    'exclude_commands': ['@nosend', '@internal', '@не_отправлять'],
    'auto_send_comments': True,
    'auto_send_roles': ['manager', 'admin', 'user'],
    'max_message_length': 4000,
    'log_level': 'INFO',
    'log_file': '/var/log/podio-wazzup-integration.log',
}

# База данных
DATABASE_CONFIG = {
    'db_path': '/opt/podio-wazzup-integration/integration_data.db',
    'backup_interval': 86400,
    'cleanup_days': 30,
}
EOF

# Настройка прав доступа
chown -R root:root /opt/podio-wazzup-integration
chmod +x /opt/podio-wazzup-integration/*.py

# Создание директории для логов
touch /var/log/podio-wazzup-integration.log
chown root:root /var/log/podio-wazzup-integration.log

echo "✅ Базовая установка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Скопируйте файлы интеграции в /opt/podio-wazzup-integration/"
echo "2. Получите App ID из Podio: python3 get_podio_apps.py"
echo "3. Обновите integration_config.py с правильными App ID"
echo "4. Запустите интеграцию: supervisorctl start podio-wazzup-integration"
echo "5. Настройте webhooks в Wazzup на: http://84.21.189.73/webhook/wazzup"
echo ""
echo "🔍 Полезные команды:"
echo "- Статус: supervisorctl status"
echo "- Логи: tail -f /var/log/podio-wazzup-integration.log"
echo "- Тест: curl http://84.21.189.73/webhook/test"

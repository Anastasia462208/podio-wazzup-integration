# 📦 Установка Podio-Wazzup Integration

## 🚀 Быстрая установка на сервере

### 1. Подключитесь к серверу
```bash
ssh root@84.21.189.73
# Пароль: bzyC5P24f8yf
```

### 2. Клонируйте репозиторий
```bash
git clone https://github.com/Anastasia462208/podio-wazzup-integration.git
cd podio-wazzup-integration
```

### 3. Запустите автоматическую установку
```bash
chmod +x install.sh
./install.sh
```

### 4. Настройте конфигурацию
```bash
cp config.example.py config.py
nano config.py
```

**Обновите следующие параметры:**
```python
# Podio API (уже настроено)
PODIO_CONFIG = {
    'client_id': 'wazzup-integration',
    'client_secret': 'FHN19OHsXbcWT74ns9qNt3goMK5JOSKCiPwqkKQQY3omYbRhEYuyQo7nG3k3LEzY',
    'username': 'blinpavlin0@gmail.com',
    'password': '326848atlantida!A',
    
    # Получите App ID с помощью скрипта
    'messages_app_id': 'ПОЛУЧИТЕ_С_ПОМОЩЬЮ_СКРИПТА',
    'contacts_app_id': 'ПОЛУЧИТЕ_С_ПОМОЩЬЮ_СКРИПТА',
    'deals_app_id': 'ПОЛУЧИТЕ_С_ПОМОЩЬЮ_СКРИПТА',
}

# Wazzup API (уже настроено)
WAZZUP_CONFIG = {
    'api_token': '1aab54ad811540da85bedbc685f938d6',
    'base_url': 'https://api.wazzup24.com/v3',
}
```

### 5. Получите App ID из Podio
```bash
cd /opt/podio-wazzup-integration
source venv/bin/activate
python3 get_podio_apps.py
```

### 6. Обновите config.py с полученными App ID

### 7. Запустите интеграцию
```bash
supervisorctl start podio-wazzup-integration
supervisorctl status
```

### 8. Настройте Webhooks в Wazzup
В настройках Wazzup укажите URL:
```
http://84.21.189.73/webhook/wazzup
```

## ✅ Проверка работы

### Проверьте статус сервисов
```bash
# Статус интеграции
supervisorctl status podio-wazzup-integration

# Статус Nginx
systemctl status nginx

# Просмотр логов
tail -f /var/log/podio-wazzup-integration.log
```

### Тестовый запрос
```bash
curl -X POST http://84.21.189.73/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

Должен вернуть: `{"status": "ok", "received": {"test": true}}`

## 🔧 Управление

### Команды Supervisor
```bash
# Запуск
supervisorctl start podio-wazzup-integration

# Остановка
supervisorctl stop podio-wazzup-integration

# Перезапуск
supervisorctl restart podio-wazzup-integration

# Статус
supervisorctl status
```

### Просмотр логов
```bash
# Логи интеграции
tail -f /var/log/podio-wazzup-integration.log

# Логи Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Проверка базы данных
```bash
cd /opt/podio-wazzup-integration
sqlite3 integration_data.db "SELECT * FROM wazzup_messages LIMIT 5;"
```

## 🧪 Тестирование

### 1. Отправьте сообщение в WhatsApp
Отправьте любое сообщение на номер, подключенный к Wazzup

### 2. Проверьте логи
```bash
tail -f /var/log/podio-wazzup-integration.log
```

Должны увидеть:
```
📥 Получено сообщение: message-id-123
✅ Сообщение сохранено
✅ Создан новый контакт для whatsapp:+1234567890
```

### 3. Проверьте Podio
В Podio должны появиться:
- Новый контакт
- Новая сделка
- Комментарий с сообщением

### 4. Отправьте ответ из Podio
В комментарии к сделке напишите:
```
@send Здравствуйте! Спасибо за обращение.
```

Через 1-2 минуты клиент должен получить сообщение.

## 🆘 Устранение неполадок

### Интеграция не запускается
```bash
# Проверьте логи
tail -f /var/log/podio-wazzup-integration.log

# Проверьте конфигурацию
python3 -c "from config import *; print('Config OK')"

# Проверьте зависимости
source venv/bin/activate
pip list
```

### Webhooks не работают
```bash
# Проверьте Nginx
nginx -t
systemctl status nginx

# Проверьте доступность
curl http://84.21.189.73/webhook/test

# Проверьте firewall
ufw status
```

### Сообщения не отправляются
```bash
# Проверьте Wazzup API
curl -H "Authorization: Bearer 1aab54ad811540da85bedbc685f938d6" \
  https://api.wazzup24.com/v3/channels

# Проверьте App ID в Podio
python3 get_podio_apps.py
```

## 📞 Поддержка

При возникновении проблем:
1. Соберите логи: `tail -100 /var/log/podio-wazzup-integration.log`
2. Проверьте статус всех сервисов
3. Создайте issue в GitHub с описанием проблемы и логами

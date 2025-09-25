# 🚀 Podio-Wazzup Integration

Интеграция между Podio CRM и Wazzup для автоматизации общения с клиентами через мессенджеры.

## ✨ Возможности

- 📥 **Автоматическое получение сообщений** из WhatsApp, Telegram, Instagram через Wazzup
- 📤 **Отправка ответов** из Podio в любой мессенджер
- 👥 **Автоматическое создание контактов** и сделок для новых клиентов
- 💬 **Удобные команды** для менеджеров (@send, @отправить)
- 🤖 **Готовность к ИИ-интеграции** с Manus для умных ответов
- 📊 **Полное логирование** и отслеживание всех сообщений

## 🏗️ Архитектура

**Гибридный подход:**
- **Webhooks** для мгновенного получения входящих сообщений из Wazzup
- **Polling** для надежной обработки исходящих сообщений из Podio
- **SQLite база данных** для отслеживания обработанных сообщений
- **Flask веб-сервер** для приема webhooks

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/YOUR_USERNAME/podio-wazzup-integration.git
cd podio-wazzup-integration
```

### 2. Автоматическая установка
```bash
chmod +x install.sh
./install.sh
```

### 3. Настройка конфигурации
```bash
cp config.example.py config.py
nano config.py  # Укажите ваши API ключи
```

### 4. Получение App ID из Podio
```bash
python3 get_podio_apps.py
```

### 5. Запуск интеграции
```bash
python3 main.py
```

## ⚙️ Конфигурация

### Podio API
```python
PODIO_CONFIG = {
    'client_id': 'your-client-id',
    'client_secret': 'your-client-secret',
    'username': 'your-email@example.com',
    'password': 'your-password',
    'messages_app_id': 'your-app-id',  # Получите с помощью get_podio_apps.py
}
```

### Wazzup API
```python
WAZZUP_CONFIG = {
    'api_token': 'your-wazzup-token',
    'base_url': 'https://api.wazzup24.com/v3',
}
```

## 📋 Требования

- Python 3.8+
- Flask
- Requests
- SQLite3
- Nginx (для production)
- Supervisor (для автозапуска)

## 🔧 Установка в production

### Ubuntu/Debian
```bash
# Клонирование репозитория
git clone https://github.com/YOUR_USERNAME/podio-wazzup-integration.git
cd podio-wazzup-integration

# Запуск автоматической установки
sudo ./install.sh

# Настройка конфигурации
sudo nano /opt/podio-wazzup-integration/config.py

# Запуск сервиса
sudo supervisorctl start podio-wazzup-integration
```

### Настройка Wazzup Webhooks
В настройках Wazzup укажите URL для webhooks:
```
http://your-server-ip/webhook/wazzup
```

## 💬 Использование

### Для менеджеров в Podio:

**Отправка сообщения клиенту:**
```
@send Здравствуйте! Ваш заказ готов к выдаче.
```

**Внутренние заметки (не отправляются):**
```
@nosend Клиент очень требовательный, нужно быть осторожнее
```

**Автоматическая отправка:**
Включите в настройках - все комментарии менеджеров будут автоматически отправляться клиентам.

### Для новых клиентов:
Система автоматически:
1. Получает сообщение из мессенджера
2. Создает контакт в Podio
3. Создает сделку
4. Добавляет сообщение как комментарий
5. Назначает ответственного менеджера

## 🤖 ИИ-интеграция

Готова к интеграции с Manus AI:
```python
# В комментарии к сделке
@manus проанализируй этот диалог и предложи ответ
```

ИИ проанализирует всю историю общения и предложит персонализированный ответ.

## 📊 Мониторинг

### Просмотр логов
```bash
tail -f /var/log/podio-wazzup-integration.log
```

### Статус сервиса
```bash
sudo supervisorctl status podio-wazzup-integration
```

### Проверка базы данных
```bash
sqlite3 integration_data.db "SELECT * FROM wazzup_messages LIMIT 10;"
```

## 🔍 API Endpoints

- `POST /webhook/wazzup` - Прием webhooks от Wazzup
- `GET /webhook/test` - Тестовый endpoint
- `GET /status` - Статус интеграции
- `GET /stats` - Статистика сообщений

## 🛠️ Разработка

### Структура проекта
```
podio-wazzup-integration/
├── main.py                 # Основной скрипт
├── config.py              # Конфигурация
├── podio_api.py           # Podio API класс
├── wazzup_api.py          # Wazzup API класс
├── message_tracker.py     # Отслеживание сообщений
├── get_podio_apps.py      # Получение App ID
├── install.sh             # Скрипт установки
├── requirements.txt       # Python зависимости
└── docs/                  # Документация
```

### Запуск в режиме разработки
```bash
python3 main.py --debug
```

## 📝 Changelog

### v1.0.0
- ✅ Базовая интеграция Podio-Wazzup
- ✅ Гибридная архитектура (webhooks + polling)
- ✅ Автоматическое создание контактов и сделок
- ✅ Система команд для менеджеров
- ✅ Полное логирование и мониторинг

### Планируется в v1.1.0
- 🔄 Интеграция с Manus AI
- 📊 Веб-интерфейс для мониторинга
- 📱 Поддержка файлов и медиа
- 🔔 Уведомления в Telegram для админов

## 🤝 Поддержка

При возникновении проблем:
1. Проверьте логи: `tail -f /var/log/podio-wazzup-integration.log`
2. Убедитесь в правильности API ключей
3. Проверьте доступность webhooks: `curl http://your-server/webhook/test`
4. Создайте issue в GitHub с описанием проблемы

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## 👨‍💻 Автор

Создано для автоматизации общения с клиентами через мессенджеры.

---

⭐ **Поставьте звезду, если проект оказался полезным!**

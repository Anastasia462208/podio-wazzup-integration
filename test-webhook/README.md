# 🧪 Podio-Wazzup Test Webhook Server

Тестовый webhook сервер для проверки интеграции Podio и Wazzup.

## 🚀 Быстрый запуск

### Локально:
```bash
npm install
npm start
```

### GitHub Codespaces:
1. Откройте репозиторий в Codespaces
2. Перейдите в папку `test-webhook`
3. Запустите `npm install && npm start`
4. Используйте публичный URL Codespaces для webhook

## 📡 Endpoints

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/` | GET | Главная страница с информацией |
| `/webhook/wazzup` | POST | Основной webhook для Wazzup |
| `/webhook/test` | POST | Тестовый endpoint |
| `/status` | GET | Статус сервера |
| `/logs` | GET | Последние 50 логов |
| `/send-message` | POST | Симуляция отправки сообщения |

## 🔧 Настройка Wazzup Webhook

### 1. Получите публичный URL:
- **Локально**: `http://localhost:3000`
- **Codespaces**: `https://your-codespace-url.github.dev`
- **Heroku/Railway**: Ваш deployment URL

### 2. Настройте webhook в Wazzup:
```bash
curl -X PATCH https://api.wazzup24.com/v3/webhooks \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "webhooksUri": "https://your-url.com/webhook/wazzup",
    "subscriptions": {
      "messagesAndStatuses": true,
      "contactsAndDealsCreation": false
    }
  }'
```

### 3. Проверьте настройки:
```bash
curl -X GET https://api.wazzup24.com/v3/webhooks \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

## 🧪 Тестирование

### Тест webhook endpoint:
```bash
curl -X POST http://localhost:3000/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

### Симуляция Wazzup webhook:
```bash
curl -X POST http://localhost:3000/webhook/wazzup \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{
      "messageId": "test-123",
      "chatId": "79161234567",
      "chatType": "whatsapp",
      "text": "Тестовое сообщение",
      "contact": {
        "name": "Тестовый пользователь"
      },
      "dateTime": "2025-09-25T15:30:00.000Z",
      "type": "text",
      "isEcho": false
    }]
  }'
```

### Симуляция отправки сообщения:
```bash
curl -X POST http://localhost:3000/send-message \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "79161234567",
    "text": "Привет! Это тестовое сообщение",
    "chatType": "whatsapp"
  }'
```

## 📊 Мониторинг

### Просмотр логов:
```bash
curl http://localhost:3000/logs
```

### Статус сервера:
```bash
curl http://localhost:3000/status
```

## 🔗 Интеграция с реальными системами

Этот тестовый сервер симулирует:
- ✅ Получение webhook от Wazzup
- ✅ Логирование всех запросов
- ✅ Обработку разных типов сообщений
- 🔄 Создание элементов в Podio (симуляция)
- 🔄 Отправку сообщений через Wazzup API (симуляция)

Для продакшн использования замените симуляции на реальные API вызовы к Podio и Wazzup.

## 🌐 Deployment

### GitHub Codespaces:
1. Форкните репозиторий
2. Откройте в Codespaces
3. Запустите сервер
4. Используйте публичный URL

### Railway/Heroku:
1. Подключите GitHub репозиторий
2. Укажите папку `test-webhook`
3. Установите переменную `PORT`
4. Deploy!

### Собственный сервер:
1. Клонируйте репозиторий
2. Установите Node.js
3. Запустите `npm install && npm start`
4. Настройте reverse proxy (nginx)

## 🎯 Следующие шаги

1. ✅ Протестируйте webhook с Wazzup
2. 🔄 Добавьте реальную интеграцию с Podio API
3. 🔄 Добавьте отправку сообщений через Wazzup API
4. 📊 Добавьте базу данных для отслеживания
5. 🔐 Добавьте аутентификацию и безопасность

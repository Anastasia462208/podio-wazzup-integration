#!/usr/bin/env node
/**
 * Тестовый webhook сервер для интеграции Podio-Wazzup
 * Для тестирования на GitHub Codespaces или локально
 */

const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Логирование всех запросов
app.use((req, res, next) => {
    const timestamp = new Date().toISOString();
    const logEntry = `${timestamp} - ${req.method} ${req.url} - ${JSON.stringify(req.body)}\n`;
    
    console.log(logEntry);
    
    // Сохранение в файл
    fs.appendFileSync('webhook-logs.txt', logEntry);
    
    next();
});

// Главная страница
app.get('/', (req, res) => {
    res.json({
        status: 'Podio-Wazzup Test Webhook Server',
        timestamp: new Date().toISOString(),
        endpoints: {
            webhook: '/webhook/wazzup',
            test: '/webhook/test',
            logs: '/logs',
            status: '/status'
        }
    });
});

// Webhook endpoint для Wazzup
app.post('/webhook/wazzup', (req, res) => {
    const data = req.body;
    const timestamp = new Date().toISOString();
    
    console.log('🔔 Wazzup Webhook received:', JSON.stringify(data, null, 2));
    
    // Обработка тестового запроса
    if (data.test === true) {
        console.log('✅ Test webhook received from Wazzup');
        return res.status(200).json({ status: 'test received' });
    }
    
    // Обработка сообщений
    if (data.messages && Array.isArray(data.messages)) {
        data.messages.forEach(message => {
            console.log(`📥 Message from ${message.contact?.name || 'Unknown'}: ${message.text}`);
            
            // Здесь будет интеграция с Podio
            processMessage(message);
        });
    }
    
    // Обработка статусов
    if (data.statuses && Array.isArray(data.statuses)) {
        data.statuses.forEach(status => {
            console.log(`📊 Status update: ${status.messageId} -> ${status.status}`);
        });
    }
    
    res.status(200).json({ 
        status: 'received',
        timestamp: timestamp,
        processed: {
            messages: data.messages?.length || 0,
            statuses: data.statuses?.length || 0
        }
    });
});

// Тестовый endpoint
app.post('/webhook/test', (req, res) => {
    console.log('🧪 Test endpoint called:', req.body);
    res.json({ 
        status: 'test endpoint working',
        received: req.body,
        timestamp: new Date().toISOString()
    });
});

// Получение логов
app.get('/logs', (req, res) => {
    try {
        const logs = fs.readFileSync('webhook-logs.txt', 'utf8');
        const lines = logs.split('\n').filter(line => line.trim()).slice(-50); // Последние 50 строк
        
        res.json({
            logs: lines,
            total_lines: lines.length
        });
    } catch (error) {
        res.json({ logs: [], error: 'No logs yet' });
    }
});

// Статус сервера
app.get('/status', (req, res) => {
    res.json({
        status: 'running',
        uptime: process.uptime(),
        timestamp: new Date().toISOString(),
        memory: process.memoryUsage(),
        version: '1.0.0'
    });
});

// Симуляция отправки в Podio
function processMessage(message) {
    console.log('🔄 Processing message for Podio integration...');
    
    // Симуляция создания элемента в Podio
    const podioItem = {
        title: `Сообщение от ${message.contact?.name || 'Неизвестно'}`,
        text: message.text,
        chatId: message.chatId,
        chatType: message.chatType,
        timestamp: message.dateTime,
        messageId: message.messageId
    };
    
    console.log('📝 Would create Podio item:', JSON.stringify(podioItem, null, 2));
    
    // Здесь будет реальный API вызов к Podio
    // createPodioItem(podioItem);
}

// Симуляция отправки в Wazzup
app.post('/send-message', (req, res) => {
    const { chatId, text, chatType = 'whatsapp' } = req.body;
    
    console.log(`📤 Simulating message send to ${chatType}:${chatId}: ${text}`);
    
    // Здесь будет реальный API вызов к Wazzup
    // sendWazzupMessage(chatId, text, chatType);
    
    res.json({
        status: 'message sent (simulated)',
        chatId,
        text,
        chatType,
        timestamp: new Date().toISOString()
    });
});

// Обработка ошибок
app.use((error, req, res, next) => {
    console.error('❌ Server error:', error);
    res.status(500).json({ 
        error: 'Internal server error',
        message: error.message 
    });
});

// Запуск сервера
app.listen(PORT, () => {
    console.log(`🚀 Podio-Wazzup Test Webhook Server running on port ${PORT}`);
    console.log(`📍 Webhook URL: http://localhost:${PORT}/webhook/wazzup`);
    console.log(`🧪 Test URL: http://localhost:${PORT}/webhook/test`);
    console.log(`📊 Status URL: http://localhost:${PORT}/status`);
    console.log(`📋 Logs URL: http://localhost:${PORT}/logs`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('🛑 Server shutting down...');
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('🛑 Server shutting down...');
    process.exit(0);
});

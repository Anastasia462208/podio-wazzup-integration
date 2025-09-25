#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Гибридная интеграция Podio-Wazzup
- Минимальные webhooks для получения сообщений из Wazzup
- Polling для обработки комментариев Podio и отправки ответов
"""

from flask import Flask, request, jsonify
import requests
import sqlite3
import json
import time
import logging
import threading
from datetime import datetime, timedelta
from config import PODIO_CONFIG, WAZZUP_CONFIG, INTEGRATION_CONFIG, DATABASE_CONFIG

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, INTEGRATION_CONFIG['log_level']),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask приложение для webhooks
app = Flask(__name__)

class PodioAPI:
    """Класс для работы с Podio API"""
    
    def __init__(self):
        self.access_token = None
        self.token_expires = None
        
    def authenticate(self):
        """Аутентификация в Podio"""
        url = "https://api.podio.com/oauth/token"
        data = {
            'grant_type': 'password',
            'client_id': PODIO_CONFIG['client_id'],
            'client_secret': PODIO_CONFIG['client_secret'],
            'username': PODIO_CONFIG['username'],
            'password': PODIO_CONFIG['password']
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                self.token_expires = datetime.now() + timedelta(seconds=token_data.get('expires_in', 3600))
                logger.info("✅ Успешная аутентификация в Podio")
                return True
            else:
                logger.error(f"❌ Ошибка аутентификации Podio: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Исключение при аутентификации Podio: {e}")
            return False
    
    def ensure_authenticated(self):
        """Проверка и обновление токена при необходимости"""
        if not self.access_token or datetime.now() >= self.token_expires:
            return self.authenticate()
        return True
    
    def get_headers(self):
        """Получение заголовков для API запросов"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def create_item(self, app_id, fields):
        """Создание нового элемента в приложении"""
        if not self.ensure_authenticated():
            return None
            
        url = f"https://api.podio.com/item/app/{app_id}/"
        data = {
            'fields': fields
        }
        
        try:
            response = requests.post(url, headers=self.get_headers(), json=data)
            if response.status_code == 200:
                item_data = response.json()
                logger.info(f"✅ Создан элемент {item_data.get('item_id')} в приложении {app_id}")
                return item_data
            else:
                logger.error(f"❌ Ошибка создания элемента: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"❌ Исключение при создании элемента: {e}")
            return None
    
    def add_comment_to_item(self, app_id, item_id, comment_text):
        """Добавление комментария к элементу"""
        if not self.ensure_authenticated():
            return False
            
        url = f"https://api.podio.com/comment/app/{app_id}/{item_id}/"
        data = {
            'value': comment_text,
            'external_id': f"wazzup_{int(time.time())}"
        }
        
        try:
            response = requests.post(url, headers=self.get_headers(), json=data)
            if response.status_code == 200:
                logger.info(f"✅ Комментарий добавлен к элементу {item_id}")
                return True
            else:
                logger.error(f"❌ Ошибка добавления комментария: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Исключение при добавлении комментария: {e}")
            return False

class WazzupAPI:
    """Класс для работы с Wazzup API"""
    
    def __init__(self):
        self.api_token = WAZZUP_CONFIG['api_token']
        self.base_url = WAZZUP_CONFIG['base_url']
    
    def get_headers(self):
        """Получение заголовков для API запросов"""
        return {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
    
    def send_message(self, channel_id, chat_id, text, chat_type='whatsapp'):
        """Отправка сообщения"""
        url = f"{self.base_url}/message"
        data = {
            'channelId': channel_id,
            'chatId': chat_id,
            'text': text,
            'chatType': chat_type
        }
        
        try:
            response = requests.post(url, headers=self.get_headers(), json=data)
            if response.status_code == 201:  # Wazzup возвращает 201 для успешной отправки
                result = response.json()
                logger.info(f"✅ Сообщение отправлено в {chat_type} чат {chat_id}")
                return result
            else:
                logger.error(f"❌ Ошибка отправки сообщения: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"❌ Исключение при отправке сообщения: {e}")
            return None
    
    def setup_webhooks(self, webhook_url):
        """Настройка webhooks"""
        url = f"{self.base_url}/webhooks"
        data = {
            'webhooksUri': webhook_url,
            'subscriptions': {
                'messagesAndStatuses': True,
                'contactsAndDealsCreation': False,
                'channelsUpdates': False,
                'templateStatus': False
            }
        }
        
        try:
            response = requests.patch(url, headers=self.get_headers(), json=data)
            if response.status_code == 200:
                logger.info(f"✅ Webhooks настроены на {webhook_url}")
                return True
            else:
                logger.error(f"❌ Ошибка настройки webhooks: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ Исключение при настройке webhooks: {e}")
            return False

class MessageTracker:
    """Класс для отслеживания обработанных сообщений"""
    
    def __init__(self):
        self.db_path = DATABASE_CONFIG['db_path']
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Таблица для сообщений Wazzup
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS wazzup_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id TEXT UNIQUE,
                    channel_id TEXT,
                    chat_id TEXT,
                    chat_type TEXT,
                    sender_name TEXT,
                    text TEXT,
                    content_uri TEXT,
                    message_type TEXT,
                    status TEXT,
                    datetime TEXT,
                    is_echo BOOLEAN,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    podio_item_id TEXT
                )
            ''')
            
            # Таблица для контактов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id TEXT UNIQUE,
                    chat_type TEXT,
                    name TEXT,
                    phone TEXT,
                    username TEXT,
                    podio_contact_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица для сделок
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS deals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contact_id INTEGER,
                    podio_item_id TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (contact_id) REFERENCES contacts (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ База данных инициализирована")
            
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации базы данных: {e}")
    
    def save_wazzup_message(self, message_data):
        """Сохранение сообщения из Wazzup"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO wazzup_messages 
                (message_id, channel_id, chat_id, chat_type, sender_name, text, 
                 content_uri, message_type, status, datetime, is_echo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                message_data.get('messageId'),
                message_data.get('channelId'),
                message_data.get('chatId'),
                message_data.get('chatType'),
                message_data.get('contact', {}).get('name', 'Unknown'),
                message_data.get('text', ''),
                message_data.get('contentUri', ''),
                message_data.get('type', 'text'),
                message_data.get('status', 'unknown'),
                message_data.get('dateTime'),
                message_data.get('isEcho', False)
            ))
            
            conn.commit()
            conn.close()
            logger.info(f"✅ Сообщение {message_data.get('messageId')} сохранено")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения сообщения: {e}")
            return False
    
    def get_or_create_contact(self, chat_id, chat_type, name=None):
        """Получение или создание контакта"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Ищем существующий контакт
            cursor.execute("SELECT * FROM contacts WHERE chat_id = ? AND chat_type = ?", (chat_id, chat_type))
            contact = cursor.fetchone()
            
            if contact:
                conn.close()
                return contact[0]  # Возвращаем ID контакта
            
            # Создаем новый контакт
            cursor.execute('''
                INSERT INTO contacts (chat_id, chat_type, name)
                VALUES (?, ?, ?)
            ''', (chat_id, chat_type, name or 'Unknown'))
            
            contact_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Создан новый контакт {contact_id} для {chat_type}:{chat_id}")
            return contact_id
            
        except Exception as e:
            logger.error(f"❌ Ошибка работы с контактом: {e}")
            return None

# Глобальные объекты
podio = PodioAPI()
wazzup = WazzupAPI()
tracker = MessageTracker()

@app.route('/webhook/wazzup', methods=['POST'])
def wazzup_webhook():
    """Обработчик webhooks от Wazzup"""
    try:
        data = request.get_json()
        
        # Обработка тестового запроса
        if data.get('test'):
            logger.info("📥 Получен тестовый webhook от Wazzup")
            return jsonify({'status': 'ok'}), 200
        
        # Обработка сообщений
        messages = data.get('messages', [])
        
        for message in messages:
            logger.info(f"📥 Получено сообщение: {message.get('messageId')}")
            
            # Пропускаем исходящие сообщения (отправленные нами)
            if message.get('isEcho') or message.get('status') != 'inbound':
                continue
            
            # Сохраняем сообщение
            tracker.save_wazzup_message(message)
            
            # Получаем или создаем контакт
            chat_id = message.get('chatId')
            chat_type = message.get('chatType')
            sender_name = message.get('contact', {}).get('name', 'Unknown')
            
            contact_id = tracker.get_or_create_contact(chat_id, chat_type, sender_name)
            
            if contact_id:
                # TODO: Создать сделку в Podio или добавить комментарий к существующей
                logger.info(f"✅ Сообщение обработано для контакта {contact_id}")
            
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        logger.error(f"❌ Ошибка обработки webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/webhook/test', methods=['GET', 'POST'])
def test_webhook():
    """Тестовый endpoint для проверки webhooks"""
    if request.method == 'POST':
        data = request.get_json()
        logger.info(f"📥 Тестовый webhook: {data}")
        return jsonify({'status': 'ok', 'received': data}), 200
    else:
        return jsonify({'status': 'webhook server is running'}), 200

def run_polling_loop():
    """Основной цикл polling для обработки комментариев Podio"""
    logger.info("🔄 Запуск polling цикла для Podio")
    
    while True:
        try:
            # TODO: Реализовать получение новых комментариев из Podio
            # и отправку их через Wazzup API
            
            logger.info("🔍 Проверка новых комментариев в Podio...")
            
            # Пауза между проверками
            time.sleep(INTEGRATION_CONFIG['polling_interval'])
            
        except Exception as e:
            logger.error(f"❌ Ошибка в polling цикле: {e}")
            time.sleep(30)  # Короткая пауза при ошибке

def main():
    """Основная функция"""
    logger.info("🚀 Запуск гибридной интеграции Podio-Wazzup")
    
    # Проверяем подключения
    if not podio.authenticate():
        logger.error("❌ Не удалось подключиться к Podio")
        return
    
    # Настраиваем webhooks для Wazzup (если нужно)
    webhook_url = "https://your-server.com/webhook/wazzup"  # Замените на ваш URL
    # wazzup.setup_webhooks(webhook_url)
    
    # Запускаем polling в отдельном потоке
    polling_thread = threading.Thread(target=run_polling_loop, daemon=True)
    polling_thread.start()
    
    # Запускаем Flask сервер для webhooks
    logger.info("🌐 Запуск webhook сервера на порту 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()

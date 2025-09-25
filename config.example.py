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
    
    # App IDs (пока используем тестовые значения, обновим после получения реальных)
    'messages_app_id': 'UNKNOWN',  # Приложение для сообщений (Wazz)
    'contacts_app_id': 'UNKNOWN',  # Приложение для контактов (если есть)
    'deals_app_id': 'UNKNOWN',     # Приложение для сделок (если есть)
    
    # Рабочая область
    'space_url': 'shturm-j361z6sagw/chat',
}

# Wazzup API настройки
WAZZUP_CONFIG = {
    'api_token': '1aab54ad811540da85bedbc685f938d6',
    'base_url': 'https://api.wazzup24.com/v3',
}

# Настройки интеграции
INTEGRATION_CONFIG = {
    # Интервал опроса в секундах
    'polling_interval': 120,  # 2 минуты
    
    # Команды для отправки сообщений
    'send_commands': ['@send', '@отправить', '@wazzup', '@клиент'],
    
    # Команды для исключения из отправки
    'exclude_commands': ['@nosend', '@internal', '@не_отправлять'],
    
    # Автоматическая отправка комментариев (без команд)
    'auto_send_comments': True,
    
    # Роли пользователей, чьи комментарии отправляются автоматически
    'auto_send_roles': ['manager', 'admin', 'user'],
    
    # Максимальная длина сообщения
    'max_message_length': 4000,
    
    # Логирование
    'log_level': 'INFO',
    'log_file': '/home/ubuntu/podio_wazzup_integration.log',
}

# База данных для отслеживания обработанных сообщений
DATABASE_CONFIG = {
    'db_path': '/home/ubuntu/integration_data.db',
    'backup_interval': 86400,  # 24 часа
    'cleanup_days': 30,  # Удалять записи старше 30 дней
}

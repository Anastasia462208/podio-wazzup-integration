#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для получения информации о приложениях в Podio
"""

import requests
import json
import sys

def authenticate_podio(client_id, client_secret, username, password):
    """Аутентификация в Podio"""
    url = "https://api.podio.com/oauth/token"
    data = {
        'grant_type': 'password',
        'client_id': client_id,
        'client_secret': client_secret,
        'username': username,
        'password': password
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Успешная аутентификация в Podio")
            return token_data['access_token']
        else:
            print(f"❌ Ошибка аутентификации: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Исключение при аутентификации: {e}")
        return None

def get_workspaces(access_token):
    """Получение списка рабочих областей"""
    url = "https://api.podio.com/space/"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            workspaces = response.json()
            print(f"✅ Найдено {len(workspaces)} рабочих областей")
            return workspaces
        else:
            print(f"❌ Ошибка получения рабочих областей: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Исключение при получении рабочих областей: {e}")
        return []

def get_apps_in_workspace(access_token, space_id):
    """Получение приложений в рабочей области"""
    url = f"https://api.podio.com/app/space/{space_id}/"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            apps = response.json()
            return apps
        else:
            print(f"❌ Ошибка получения приложений: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Исключение при получении приложений: {e}")
        return []

def main():
    """Основная функция"""
    print("🚀 Получение информации о приложениях Podio")
    
    # Данные для подключения
    client_id = 'wazzup-integration'
    client_secret = 'FHN19OHsXbcWT74ns9qNt3goMK5JOSKCiPwqkKQQY3omYbRhEYuyQo7nG3k3LEzY'
    username = 'blinpavlin0@gmail.com'
    password = '326848atlantida!A'
    
    # Аутентификация
    access_token = authenticate_podio(client_id, client_secret, username, password)
    if not access_token:
        print("❌ Не удалось получить токен доступа")
        return
    
    # Получение рабочих областей
    workspaces = get_workspaces(access_token)
    
    print("\n📋 Информация о рабочих областях и приложениях:")
    print("=" * 60)
    
    for workspace in workspaces:
        space_id = workspace['space_id']
        space_name = workspace['name']
        
        print(f"\n🏢 Рабочая область: {space_name} (ID: {space_id})")
        
        # Получение приложений в этой рабочей области
        apps = get_apps_in_workspace(access_token, space_id)
        
        if apps:
            print(f"   📱 Приложения ({len(apps)}):")
            for app in apps:
                app_id = app['app_id']
                app_name = app['config']['name']
                item_name = app['config']['item_name']
                
                print(f"      • {app_name}")
                print(f"        App ID: {app_id}")
                print(f"        Item Name: {item_name}")
                print(f"        URL: https://podio.com/{workspace['url']}/apps/{app_id}")
                print()
        else:
            print("   📱 Приложений не найдено")
    
    print("\n✅ Готово! Используйте App ID из списка выше для настройки интеграции.")

if __name__ == "__main__":
    main()

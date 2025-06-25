#!/usr/bin/env python3
"""
🔧 Configurador de Webhook para Telegram Bot
Este script configura el webhook en Telegram para el deployment de Render
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RENDER_URL = input("🌐 Ingresa la URL de tu app en Render (ej: https://mi-bot.onrender.com): ").strip()

if not BOT_TOKEN:
    print("❌ BOT_TOKEN no encontrado en .env")
    sys.exit(1)

if not RENDER_URL:
    print("❌ URL de Render requerida")
    sys.exit(1)

# Configurar webhook
webhook_url = f"{RENDER_URL}/webhook"
telegram_api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"

print(f"🔧 Configurando webhook...")
print(f"📍 URL: {webhook_url}")

try:
    response = requests.post(telegram_api_url, json={'url': webhook_url})
    result = response.json()
    
    if result.get('ok'):
        print("✅ Webhook configurado correctamente")
        print(f"📋 Descripción: {result.get('description', 'N/A')}")
    else:
        print(f"❌ Error configurando webhook: {result.get('description', 'Error desconocido')}")
        
except Exception as e:
    print(f"❌ Error de conexión: {e}")

# Verificar webhook
print("\n🔍 Verificando webhook...")
try:
    verify_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    response = requests.get(verify_url)
    result = response.json()
    
    if result.get('ok'):
        webhook_info = result.get('result', {})
        print(f"📍 URL configurada: {webhook_info.get('url', 'Ninguna')}")
        print(f"🔄 Último error: {webhook_info.get('last_error_message', 'Ninguno')}")
        print(f"📊 Mensajes pendientes: {webhook_info.get('pending_update_count', 0)}")
    else:
        print(f"❌ Error verificando webhook: {result.get('description', 'Error desconocido')}")
        
except Exception as e:
    print(f"❌ Error verificando webhook: {e}")

print("\n🎯 Si el webhook está configurado correctamente, el bot debería responder ahora.")
print("💡 Si sigue sin funcionar, usa polling temporal con el script reset_to_polling.py")

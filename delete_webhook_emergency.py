#!/usr/bin/env python3
"""
🔧 ELIMINADOR DE WEBHOOK DIRECTO
Script de emergencia para eliminar webhook cuando no se puede acceder al .env
"""

import sys
import requests

print("🚨 ELIMINADOR DE WEBHOOK DE EMERGENCIA")
print("=" * 50)

# Pedir token directamente
BOT_TOKEN = input("🔑 Ingresa tu BOT_TOKEN: ").strip()

if not BOT_TOKEN:
    print("❌ Token requerido")
    sys.exit(1)

print("\n🔄 Eliminando webhook...")

try:
    # Eliminar webhook
    telegram_api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
    response = requests.post(telegram_api_url)
    result = response.json()
    
    if result.get('ok'):
        print("✅ Webhook eliminado correctamente")
        print("🔄 Ahora el bot puede usar polling")
    else:
        print(f"❌ Error eliminando webhook: {result.get('description', 'Error desconocido')}")
        
except Exception as e:
    print(f"❌ Error de conexión: {e}")

print("\n🔍 Verificando estado actual...")
try:
    verify_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    response = requests.get(verify_url)
    result = response.json()
    
    if result.get('ok'):
        webhook_info = result.get('result', {})
        webhook_url = webhook_info.get('url', '')
        
        if webhook_url:
            print(f"⚠️  Webhook aún activo: {webhook_url}")
        else:
            print("✅ Sin webhook configurado - polling disponible")
            
        print(f"📊 Mensajes pendientes: {webhook_info.get('pending_update_count', 0)}")
    else:
        print(f"❌ Error verificando: {result.get('description', 'Error desconocido')}")
        
except Exception as e:
    print(f"❌ Error verificando: {e}")

print("\n🎯 Si no hay webhook configurado, el deployment debería funcionar ahora.")

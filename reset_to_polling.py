#!/usr/bin/env python3
"""
🔄 Reset a Polling - Solución temporal
Este script elimina el webhook y permite que el bot use polling
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ BOT_TOKEN no encontrado en .env")
    sys.exit(1)

print("🔄 Eliminando webhook para usar polling...")

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

print("\n📝 NOTA: Después de esto, necesitarás:")
print("1. Cambiar Render a polling mode")
print("2. O reconfigurar el webhook correctamente")
print("3. El bot debería responder mientras tanto")

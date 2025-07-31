#!/bin/bash
# Script para mantener el bot corriendo en GitHub Codespaces

echo "🚀 Iniciando Bot Mentor en GitHub Codespaces..."

# Verificar variables de entorno
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ Error: TELEGRAM_BOT_TOKEN no configurado"
    echo "💡 Configura con: gh secret set TELEGRAM_BOT_TOKEN"
    exit 1
fi

# Mantener el proceso activo
while true; do
    echo "🔄 Iniciando bot..."
    python launch_bot.py
    
    echo "⚠️  Bot se detuvo. Reiniciando en 10 segundos..."
    sleep 10
done

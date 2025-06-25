# 🤖 Telegram Bot Mentor

Bot de Telegram para la Fundación que funciona 24/7 en la nube.

## 📋 Estado del Proyecto

✅ **COMPLETADO:**
- Limpieza y optimización del código
- Funcionamiento local confirmado
- Deployment en Render configurado
- Variables de entorno protegidas

## 🚨 Problema Identificado en Render

El bot funciona correctamente pero el deployment queda en "in progress" porque:

**PROBLEMA:** El servicio está configurado como "Web Service" cuando debe ser "Background Worker"

**CAUSA:** Los bots con polling no abren puertos HTTP, pero Render Web Services esperan al menos un puerto abierto.

**SOLUCIÓN:** Cambiar a Background Worker en Render Dashboard.

## 🛠️ Instrucciones para Corregir el Deployment

### Opción 1: Cambiar Configuración Manualmente

1. Ve a tu Dashboard de Render
2. Selecciona el servicio "telegram-bot-mentor"
3. Ve a Settings
4. En "Service Type", cámbialo de "Web Service" a "Background Worker"
5. Guarda los cambios
6. El servicio se redesplegarà automáticamente

### Opción 2: Usar render.yaml (Recomendado)

1. Este repositorio ya incluye `render.yaml` con la configuración correcta
2. En Render Dashboard, elimina el servicio actual
3. Crea un nuevo servicio conectado a este repositorio
4. Render detectará automáticamente el `render.yaml` y creará un Background Worker

### Variables de Entorno Requeridas

En Render Dashboard, configura:
```
TELEGRAM_BOT_TOKEN = tu_token_del_bot
ENVIRONMENT = production
```

## 🔧 Configuración del render.yaml

```yaml
services:
  - type: worker  # Background Worker para bots con polling
    name: telegram-bot-mentor
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python launch_bot.py
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        sync: false  # Se configura manualmente en Dashboard
      - key: ENVIRONMENT
        value: production
```

## 📊 Verificación de Funcionamiento

Una vez corregida la configuración:

1. **Estado del Servicio:** Debe mostrar "Active" (no "In Progress")
2. **Logs:** Deberían mostrar "Bot iniciado correctamente en modo polling"
3. **Funcionalidad:** Todos los comandos del bot deben responder

## 🤖 Comandos del Bot

- `/start` - Mensaje de bienvenida
- `/info` - Información sobre la fundación
- `/contacto` - Datos de contacto
- `/ayuda` - Lista de comandos disponibles

## 🔍 Solución de Problemas

### Si el bot no responde:
1. Verifica que `TELEGRAM_BOT_TOKEN` esté configurado correctamente
2. Revisa los logs en Render Dashboard
3. Asegúrate de que el servicio esté en estado "Active"

### Si hay errores de webhook:
1. El bot usa polling, no webhooks
2. Si aparecen errores de webhook, ejecuta el script de limpieza:
   ```bash
   python delete_webhook_emergency.py
   ```

## 🚀 Próximos Pasos

1. **Inmediato:** Cambiar configuración en Render a Background Worker
2. **Opcional:** Migrar a webhooks para mejor rendimiento
3. **Mejoras:** Agregar más comandos y funcionalidades

---

**Autor:** Desarrollo para Fundación  
**Última actualización:** Diciembre 2024  
**Estado:** Listo para producción (requiere cambio de configuración en Render)

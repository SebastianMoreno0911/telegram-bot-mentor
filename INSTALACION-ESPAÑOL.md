# 🤖 **INSTALACIÓN COMPLETA - BOT MENTOR SEBASTIÁN**

## 🚀 **Guía Única para Configurar tu Mentor Personal 24/7**

---

## 📋 **PASO 1: REQUISITOS PREVIOS**

### **🐍 1. Instalar Python 3.8+**

1. **Descargar:** https://www.python.org/downloads/
2. **✅ CRÍTICO:** Marcar "Add Python to PATH" durante instalación
3. **Verificar:**
   ```bash
   python --version
   pip --version
   ```

### **📱 2. Crear Bot de Telegram**

1. **Abrir Telegram** → buscar `@BotFather`
2. **Enviar:** `/newbot`
3. **Configurar:**
   - Nombre: `Bot Mentor Sebastián`
   - Username: `sebastian_mentor_bot` (debe terminar en \_bot)
4. **🔑 GUARDAR TOKEN:** `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`

### **🆔 3. Obtener tu Chat ID (Opcional)**

1. **Buscar:** `@userinfobot` en Telegram
2. **Enviar:** `/start`
3. **Copiar:** Tu User ID (ej: `123456789`)

---

## ⚙️ **PASO 2: INSTALACIÓN Y CONFIGURACIÓN**

### **📁 Ubicación del proyecto**

```bash
cd "C:\Users\sebas\Desktop\Fundacion\telegram-bot-mentor"
```

### **📦 Instalar dependencias**

```bash
pip install -r requirements.txt
```

### **🔧 Configurar variables de entorno**

1. **Crear archivo de configuración:**

   ```bash
   copy .env.example .env
   ```

2. **Editar `.env`** con tus datos:

   ```bash
   # 📱 TELEGRAM (OBLIGATORIO)
   BOT_TOKEN=TU_TOKEN_DE_BOTFATHER_AQUI
   CHAT_ID=TU_CHAT_ID_AQUI

   # ⏰ HORARIOS (OPCIONAL)
   DAILY_REMINDER_TIME=09:00
   WEEKLY_REMINDER_TIME=18:00
   ```

---

## � **PASO 3: SUBIR A GITHUB (Para deployment gratuito)**

### **🐙 Crear repositorio en GitHub**

1. **Ir a GitHub:** https://github.com/new
2. **Nombre:** `telegram-bot-mentor`
3. **Descripción:** `Bot mentor para desarrollo web - 12 semanas hacia Job Ready Developer`
4. **Público** (para mejores límites gratuitos)
5. **Crear repositorio**

### **💻 Subir código desde terminal**

**🎯 CLAVE:** Ejecutar desde DENTRO de la carpeta `telegram-bot-mentor` para subir solo el bot

```bash
# PASO 1: Navegar a la carpeta del bot (MUY IMPORTANTE)
cd "C:\Users\sebas\Desktop\Fundacion\telegram-bot-mentor"

# PASO 2: Configurar Git (primera vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"

# PASO 3: Verificar ubicación correcta
pwd
# Debe mostrar: /c/Users/sebas/Desktop/Fundacion/telegram-bot-mentor

# PASO 4: Inicializar repositorio EN LA CARPETA DEL BOT
git init

# PASO 5: Agregar SOLO archivos del bot (no carpetas padre)
git add .
git commit -m "🚀 Bot mentor completado - listo para deployment"

# PASO 6: Conectar con GitHub (cambiar URL por la tuya)
git remote add origin https://github.com/TU_USUARIO/telegram-bot-mentor.git
git branch -M main
git push -u origin main
```

**✅ RESULTADO ESPERADO:** Tu repositorio GitHub contendrá como raíz:

```
telegram-bot-mentor/  (raíz del repositorio)
├── bot_final.py
├── launch_bot.py
├── config.py
├── database.py
├── evidence_manager.py
├── requirements.txt
├── .env.example
├── Procfile
├── runtime.txt
├── railway.json
├── .gitignore
├── INSTALACION-ESPAÑOL.md
└── PENDIENTES-CHECKLIST.md
```

**✅ ¡Listo! Solo el contenido del bot está en GitHub, sin carpetas padre innecesarias**

---

## 🚀 **PASO 4: DEPLOYMENT 24/7 GRATIS**

### **🖥️ Para uso LOCAL (pruebas):**

```bash
python launch_bot.py
```

### **☁️ Para DEPLOYMENT 24/7 GRATIS (recomendado):**

#### **� Render (GRATIS PARA SIEMPRE - Recomendado #1)**

1. **Crear cuenta:** https://render.com/
2. **Conectar GitHub** (crear repositorio primero)
3. **New Web Service** → Connect Repository
4. **Configuración:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python launch_bot.py`
   - **Environment:** Python 3
5. **Variables de entorno:** Agregar BOT_TOKEN, CHAT_ID
6. **Deploy GRATIS** ✅

**💰 Límites gratuitos:** 750 horas/mes, sleep después de 15 min inactividad

#### **� Railway (GRATIS - Plan Hobby)**

1. **Crear cuenta:** https://railway.app/
2. **Deploy from GitHub** → Tu repositorio
3. **Variables de entorno:** BOT_TOKEN, CHAT_ID
4. **Deploy automático** ✅

**💰 Límites gratuitos:** $5 USD/mes de créditos gratis

#### **🐙 GitHub Codespaces (100% GRATIS - Opción Premium)**

1. **Subir a GitHub** (público o privado)
2. **Code** → **Codespaces** → **Create codespace**
3. **En la terminal:**
   ```bash
   pip install -r requirements.txt
   python launch_bot.py
   ```
4. **Mantener pestaña abierta** para que funcione 24/7

**💰 Límites gratuitos:** 120 horas núcleo/mes (más que suficiente)

#### **☁️ Replit (GRATIS con limitaciones)**

1. **Crear cuenta:** https://replit.com/
2. **Import from GitHub** → Tu repositorio
3. **Run** automáticamente
4. **Configurar Always On** (gratis limitado)

**💰 Límites gratuitos:** Always On limitado, pero funcional

---

## ✅ **PASO 4: VERIFICAR FUNCIONAMIENTO**

### **1. Probar Bot en Telegram**

```bash
/start      ← Debe responder con bienvenida
/semana     ← Ver semana actual
/progreso   ← Tus estadísticas
/evidencia  ← Enviar evidencias
```

### **2. Comandos Completos Disponibles**

#### **📚 Básicos:**

- `/start` - Inicializar bot
- `/help` - Ayuda completa
- `/semana` - Contenido semana actual
- `/progreso` - Estadísticas personales
- `/motivacion` - Boost de energía

#### **📝 Seguimiento:**

- `/estudie [horas]` - Registrar tiempo
- `/completar` - Marcar tarea completada
- `/objetivo` - Ver objetivos semanales

#### **🆕 Sistema de Evidencias:**

- `/evidencia` - Enviar capturas, URLs, repos
- `/examen` - Tomar quiz semanal obligatorio
- `/validacion` - Ver estado de validación
- `/estado` - Progreso completo de semana

---

## 🎯 **FUNCIONALIDADES ÚNICAS**

### **📸 Sistema de Evidencias REAL**

- **Capturas obligatorias** del proyecto funcionando
- **URLs verificables** automáticamente (Netlify/Vercel)
- **Repositorios GitHub** con validación de código
- **Explicaciones técnicas** de conceptos
- **🔒 NO AVANZAS** sin evidencias válidas

### **📝 Exámenes Semanales**

- **Quiz automático** con preguntas técnicas
- **70% mínimo** para aprobar
- **3 intentos máximo** por examen
- **Recuperación automática** si repruebas

### **📱 Notificaciones Inteligentes**

- **Telegram:** Interacción completa
- **Recordatorios automáticos** diarios y semanales
- **Alertas de progreso** y motivación personalizada

### **⚡ Anti-Engaño**

- **URLs verificables** en tiempo real
- **Repos de GitHub** con código revisable
- **Timeboxing** para evitar copiar
- **Preguntas** sobre tu propio código

---

## 🛠️ **SOLUCIÓN DE PROBLEMAS**

### **❌ Error: "No module named 'telegram'"**

```bash
pip install python-telegram-bot==20.7
```

### **❌ Error: "BOT_TOKEN not found"**

1. Verificar que `.env` existe
2. Sin espacios: `BOT_TOKEN=123456:ABC...`
3. Reiniciar bot

### **❌ Bot no responde**

1. Token correcto en `.env`
2. Bot ejecutándose en consola
3. Internet funcionando

---

## 📂 **ESTRUCTURA FINAL LIMPIA**

```
telegram-bot-mentor/
├── 🚀 launch_bot.py           ← EJECUTAR ESTE ARCHIVO
├── 🤖 bot_final.py            ← Lógica principal
├── ⚙️ config.py               ← Configuración y exámenes
├── 🗄️ database.py            ← Base de datos SQLite
├── 📸 evidence_manager.py     ← Sistema de evidencias
├── 📦 requirements.txt        ← Dependencias
├── 🔧 .env                    ← Tu configuración
├── 📋 .env.example            ← Plantilla
└── ☁️ Archivos cloud/         ← Para deployment
    ├── Procfile, runtime.txt, railway.json
```

---

## 🎉 **¡LISTO PARA USAR!**

Tu bot mentor está configurado con:

- ✅ **Seguimiento estricto** semanal
- ✅ **Evidencias reales** obligatorias
- ✅ **Exámenes** de validación
- ✅ **Notificaciones inteligentes** por Telegram
- ✅ **Deployment 24/7** en la nube
- ✅ **Sistema anti-engaño**

**🚀 ¡12 semanas hacia Job Ready Developer!** 💪

---

### **📞 Contacto de Emergencia**

Si algo no funciona:

1. Revisar logs en consola
2. Verificar archivo `.env`
3. Comprobar conexión a internet
4. Reiniciar bot: `Ctrl+C` → `python launch_bot.py`

---

## 🚀 **PASO 3: EJECUTAR EL BOT**

### **🖥️ Para uso LOCAL (pruebas):**

```bash
python launch_bot.py
```

### **☁️ Para DEPLOYMENT 24/7 GRATIS (recomendado):**

#### **� Render (GRATIS PARA SIEMPRE - Recomendado #1)**

1. **Crear cuenta:** https://render.com/
2. **Conectar GitHub** (crear repositorio primero)
3. **New Web Service** → Connect Repository
4. **Configuración:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python launch_bot.py`
   - **Environment:** Python 3
5. **Variables de entorno:** Agregar BOT_TOKEN, CHAT_ID
6. **Deploy GRATIS** ✅

**💰 Límites gratuitos:** 750 horas/mes, sleep después de 15 min inactividad

#### **� Railway (GRATIS - Plan Hobby)**

1. **Crear cuenta:** https://railway.app/
2. **Deploy from GitHub** → Tu repositorio
3. **Variables de entorno:** BOT_TOKEN, CHAT_ID
4. **Deploy automático** ✅

**💰 Límites gratuitos:** $5 USD/mes de créditos gratis

#### **🐙 GitHub Codespaces (100% GRATIS - Opción Premium)**

1. **Subir a GitHub** (público o privado)
2. **Code** → **Codespaces** → **Create codespace**
3. **En la terminal:**
   ```bash
   pip install -r requirements.txt
   python launch_bot.py
   ```
4. **Mantener pestaña abierta** para que funcione 24/7

**💰 Límites gratuitos:** 120 horas núcleo/mes (más que suficiente)

#### **☁️ Replit (GRATIS con limitaciones)**

1. **Crear cuenta:** https://replit.com/
2. **Import from GitHub** → Tu repositorio
3. **Run** automáticamente
4. **Configurar Always On** (gratis limitado)

**💰 Límites gratuitos:** Always On limitado, pero funcional

---

## ✅ **PASO 4: VERIFICAR FUNCIONAMIENTO**

### **1. Probar Bot en Telegram**

```bash
/start      ← Debe responder con bienvenida
/semana     ← Ver semana actual
/progreso   ← Tus estadísticas
/evidencia  ← Enviar evidencias
```

### **2. Comandos Completos Disponibles**

#### **📚 Básicos:**

- `/start` - Inicializar bot
- `/help` - Ayuda completa
- `/semana` - Contenido semana actual
- `/progreso` - Estadísticas personales
- `/motivacion` - Boost de energía

#### **📝 Seguimiento:**

- `/estudie [horas]` - Registrar tiempo
- `/completar` - Marcar tarea completada
- `/objetivo` - Ver objetivos semanales

#### **🆕 Sistema de Evidencias:**

- `/evidencia` - Enviar capturas, URLs, repos
- `/examen` - Tomar quiz semanal obligatorio
- `/validacion` - Ver estado de validación
- `/estado` - Progreso completo de semana

---

## 🎯 **FUNCIONALIDADES ÚNICAS**

### **📸 Sistema de Evidencias REAL**

- **Capturas obligatorias** del proyecto funcionando
- **URLs verificables** automáticamente (Netlify/Vercel)
- **Repositorios GitHub** con validación de código
- **Explicaciones técnicas** de conceptos
- **🔒 NO AVANZAS** sin evidencias válidas

### **📝 Exámenes Semanales**

- **Quiz automático** con preguntas técnicas
- **70% mínimo** para aprobar
- **3 intentos máximo** por examen
- **Recuperación automática** si repruebas

### **📱 Notificaciones Inteligentes**

- **Telegram:** Interacción completa
- **Recordatorios automáticos** diarios y semanales
- **Alertas de progreso** y motivación personalizada

### **⚡ Anti-Engaño**

- **URLs verificables** en tiempo real
- **Repos de GitHub** con código revisable
- **Timeboxing** para evitar copiar
- **Preguntas** sobre tu propio código

---

## 🛠️ **SOLUCIÓN DE PROBLEMAS**

### **❌ Error: "No module named 'telegram'"**

```bash
pip install python-telegram-bot==20.7
```

### **❌ Error: "BOT_TOKEN not found"**

1. Verificar que `.env` existe
2. Sin espacios: `BOT_TOKEN=123456:ABC...`
3. Reiniciar bot

### **❌ Bot no responde**

1. Token correcto en `.env`
2. Bot ejecutándose en consola
3. Internet funcionando

---

## 📂 **ESTRUCTURA FINAL LIMPIA**

```
telegram-bot-mentor/
├── 🚀 launch_bot.py           ← EJECUTAR ESTE ARCHIVO
├── 🤖 bot_final.py            ← Lógica principal
├── ⚙️ config.py               ← Configuración y exámenes
├── 🗄️ database.py            ← Base de datos SQLite
├── 📸 evidence_manager.py     ← Sistema de evidencias
├── 📦 requirements.txt        ← Dependencias
├── 🔧 .env                    ← Tu configuración
├── 📋 .env.example            ← Plantilla
└── ☁️ Archivos cloud/         ← Para deployment
    ├── Procfile, runtime.txt, railway.json
```

---

## 🎉 **¡LISTO PARA USAR!**

Tu bot mentor está configurado con:

- ✅ **Seguimiento estricto** semanal
- ✅ **Evidencias reales** obligatorias
- ✅ **Exámenes** de validación
- ✅ **Notificaciones inteligentes** por Telegram
- ✅ **Deployment 24/7** en la nube
- ✅ **Sistema anti-engaño**

**🚀 ¡12 semanas hacia Job Ready Developer!** 💪

---

### **📞 Contacto de Emergencia**

Si algo no funciona:

1. Revisar logs en consola
2. Verificar archivo `.env`
3. Comprobar conexión a internet
4. Reiniciar bot: `Ctrl+C` → `python launch_bot.py`

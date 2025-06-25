#!/usr/bin/env python3
"""
Bot Mentor de Desarrollo Web - Versión Definitiva con Sistema de Evidencias
Bot personalizado para Sebastian - 12 semanas hacia Job Ready Developer
"""

import asyncio
import logging
from datetime import datetime, timedelta, date
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import random
import sqlite3
from config import BOT_TOKEN, MOTIVATIONAL_PHRASES, STUDY_GUIDE, TOTAL_WEEKS, POINTS_TARGET, EVIDENCE_REQUIRED, STRICT_VALIDATION
from database import init_db, update_progress, get_user_stats
from evidence_manager import evidence_validator, exam_manager

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class StudyMentorBot:
    def __init__(self):
        self.app = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
        
    def setup_handlers(self):
        """Configurar todos los handlers del bot"""
        # Comandos básicos
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        
        # Comandos principales
        self.app.add_handler(CommandHandler("semana", self.current_week))
        self.app.add_handler(CommandHandler("progreso", self.show_progress))
        self.app.add_handler(CommandHandler("motivacion", self.motivation))
        
        # Comandos de registro
        self.app.add_handler(CommandHandler("estudie", self.log_study_time))
        self.app.add_handler(CommandHandler("completar", self.complete_task))
        
        # Comandos de navegación
        self.app.add_handler(CommandHandler("recursos", self.show_resources))
        self.app.add_handler(CommandHandler("objetivo", self.show_objectives))
        self.app.add_handler(CommandHandler("siguiente", self.next_step))
        
        # NUEVOS COMANDOS - Sistema de evidencias y exámenes
        self.app.add_handler(CommandHandler("evidencia", self.submit_evidence))
        self.app.add_handler(CommandHandler("examen", self.start_exam))
        self.app.add_handler(CommandHandler("validacion", self.check_validation))
        self.app.add_handler(CommandHandler("estado", self.week_status))
        
        # Manejo de fotos para evidencias
        self.app.add_handler(MessageHandler(filters.PHOTO, self.handle_photo_evidence))
        
        # Handlers para botones del teclado
        self.app.add_handler(MessageHandler(filters.Regex("^📅 Semana Actual$"), self.current_week))
        self.app.add_handler(MessageHandler(filters.Regex("^📊 Mi Progreso$"), self.show_progress))
        self.app.add_handler(MessageHandler(filters.Regex("^🚀 Motivación$"), self.motivation))
        self.app.add_handler(MessageHandler(filters.Regex("^⏰ Estudié Hoy$"), self.log_study_time))
        self.app.add_handler(MessageHandler(filters.Regex("^✅ Completar Tarea$"), self.complete_task))
        self.app.add_handler(MessageHandler(filters.Regex("^🎯 Mi Objetivo$"), self.show_objectives))
        
        # Callback handlers para botones inline
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start - Inicializar bot"""
        user_id = update.effective_user.id
        username = update.effective_user.first_name
        
        # Inicializar usuario en la base de datos
        init_db(user_id, username)
        
        welcome_message = f"""
🎯 **¡Hola {username}! Soy tu Mentor de Desarrollo Web** 🚀

Estoy aquí para guiarte en tu journey de **12 semanas** hacia convertirte en un desarrollador web profesional.

📋 **¿Qué puedo hacer por ti?**
• 📅 Seguimiento semanal personalizado
• 📊 Estadísticas de tu progreso  
• 🎯 Objetivos y proyectos específicos
• 💪 Motivación cuando la necesites
• ⏰ Registro de tiempo de estudio

🏁 **Tu Meta:** 15 puntos en 12 semanas = **Job Ready Developer**

🎮 **Sistema de Puntos:**
• 1 punto = Proyecto completado
• 0.5 puntos = Concepto/tarea dominada

**📱 Comandos principales:**
• /semana - Ver contenido actual
• /progreso - Tus estadísticas  
• /estudie [horas] - Registrar tiempo
• /completar - Marcar tarea completada
• /motivacion - Boost de energía
• /help - Lista completa

¿Listo para empezar tu transformación? 💪

**🎯 Tu primera misión:** Ve a flexboxfroggy.com y completa los niveles 1-12
"""
        
        # Teclado personalizado
        keyboard = [
            [KeyboardButton("📅 Semana Actual"), KeyboardButton("📊 Mi Progreso")],
            [KeyboardButton("⏰ Estudié Hoy"), KeyboardButton("✅ Completar Tarea")], 
            [KeyboardButton("🚀 Motivación"), KeyboardButton("🎯 Mi Objetivo")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help - Lista de comandos"""
        message = """
🤖 **Bot Mentor - Comandos Disponibles**

**📋 Comandos Básicos:**
• `/start` - Reiniciar bot y ver bienvenida
• `/help` - Esta lista de comandos

**📚 Contenido y Navegación:**
• `/semana` - Ver contenido de la semana actual
• `/recursos` - Enlaces y materiales de estudio
• `/objetivo` - Ver objetivos actuales
• `/siguiente` - Ver qué viene después

**📊 Progreso y Seguimiento:**
• `/progreso` - Estadísticas detalladas
• `/estudie [horas]` - Registrar tiempo (ej: `/estudie 2.5`)
• `/completar` - Marcar tarea o proyecto completado

**💪 Motivación:**
• `/motivacion` - Recibir mensaje motivacional

**📱 NUEVOS COMANDOS:**
• `/evidencia` - Enviar evidencia de estudio
• `/examen` - Iniciar examen
• `/validacion` - Validar progreso
• `/estado` - Ver estado de la semana

**🎯 Tu Objetivo:** 15 puntos en 12 semanas
• 1 punto = Proyecto semanal completado
• 0.5 puntos = Concepto/tarea dominada

**📱 También puedes usar los botones del teclado para navegación rápida.**

¡Tu futuro como developer empieza ahora! 🚀
"""
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    def calculate_current_week(self, user_id: int) -> int:
        """Calcular semana actual basada en fecha de inicio"""
        stats = get_user_stats(user_id)
        if not stats:
            return 1
            
        start_date = datetime.strptime(str(stats['start_date']), "%Y-%m-%d").date()
        days_passed = (date.today() - start_date).days
        current_week = min((days_passed // 7) + 1, TOTAL_WEEKS)
        
        return current_week
        
    def get_week_content(self, week: int) -> dict:
        """Obtener contenido de la semana específica"""
        return STUDY_GUIDE.get(week, {
            "title": "Programa Completado",
            "phase": "Job Search",
            "goal": "¡Felicidades! Has terminado el programa",
            "videos": "Repaso y mejoras de portfolio",
            "tools": "LinkedIn, AngelList, Indeed",
            "project": {
                "name": "Búsqueda activa de empleo", 
                "requirements": "• Aplicar a 5 posiciones diarias\n• Networking en LinkedIn\n• Mejorar portfolio"
            },
            "estimated_time": "Full time job hunting",
            "tip": "¡Es hora de conseguir ese trabajo!",
            "daily_goal": "Aplica a 5 posiciones por día"
        })
        
    async def current_week(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mostrar contenido de la semana actual"""
        user_id = update.effective_user.id
        current_week = self.calculate_current_week(user_id)
        
        if current_week > TOTAL_WEEKS:
            message = """
🎉 **¡FELICIDADES! ¡PROGRAMA COMPLETADO!** 🎉

Has completado las 12 semanas del programa. 
¡Es hora de conseguir ese trabajo como desarrollador web!

🚀 **Próximos pasos:**
• Aplica a posiciones junior
• Continúa practicando con proyectos personales
• Mantén tu portfolio actualizado
• Haz networking en la comunidad dev

🏆 **¡Tu futuro como developer está aquí!** 💼
"""
            await update.message.reply_text(message, parse_mode='Markdown')
            return
            
        week_content = self.get_week_content(current_week)
        
        # Crear botones inline para explorar contenido
        keyboard = [
            [InlineKeyboardButton("🎥 Ver Videos", callback_data=f"videos_{current_week}")],
            [InlineKeyboardButton("🛠️ Herramientas", callback_data=f"tools_{current_week}")],
            [InlineKeyboardButton("📝 Proyecto Detallado", callback_data=f"project_{current_week}")],
            [InlineKeyboardButton("💡 Tip de la Semana", callback_data=f"tip_{current_week}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"""
📅 **SEMANA {current_week}/{TOTAL_WEEKS}** - {week_content['title']}

🔥 **Fase:** {week_content['phase']}

🎯 **Objetivo de la semana:**
{week_content['goal']}

📝 **Proyecto:**
**"{week_content['project']['name']}"**

⏰ **Tiempo estimado:** {week_content['estimated_time']}

🎯 **Tu objetivo diario:**
{week_content['daily_goal']}

💡 **Tip:** {week_content['tip']}

👇 **Usa los botones para ver contenido específico**
"""
        
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        
    async def show_progress(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mostrar progreso detallado del usuario"""
        user_id = update.effective_user.id
        stats = get_user_stats(user_id)
        
        if not stats:
            await update.message.reply_text("❌ No se encontraron datos. Usa /start para inicializar.")
            return
            
        current_week = self.calculate_current_week(user_id)
        progress_percentage = min((current_week / TOTAL_WEEKS) * 100, 100)
        
        points_earned = stats['projects_completed'] + (stats['concepts_mastered'] * 0.5)
        points_percentage = min((points_earned / POINTS_TARGET) * 100, 100)
        
        # Calcular nivel y siguiente hito
        level = self.calculate_level(points_earned)
        level_name = self.get_level_name(level)
        
        # Generar barra de progreso visual
        progress_bar = self.generate_progress_bar(points_percentage)
        
        message = f"""
📊 **TU PROGRESO ACTUAL** 📈

🏆 **Nivel {level}: {level_name}**
{progress_bar} {points_percentage:.1f}%

📅 **Programa:** Semana {current_week}/{TOTAL_WEEKS} ({progress_percentage:.1f}%)

🎯 **Puntos:** {points_earned:.1f}/{POINTS_TARGET} 
• 🏆 Proyectos completados: {stats['projects_completed']} 
• 🧠 Conceptos dominados: {stats['concepts_mastered']}

📚 **Estadísticas de Estudio:**
• ⏰ Horas totales: {stats['total_hours']:.1f}h
• 📅 Días estudiando: {stats['study_days']}
• 🔥 Streak actual: {stats['current_streak']} días

📈 **Análisis de Ritmo:**
{self.calculate_pace_feedback(current_week, points_earned)}

🎯 **Próximo hito:**
{self.get_next_milestone(points_earned)}

{self.get_motivational_badges(stats)}

¡Sigue así! Cada día cuenta 💪
"""
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    async def log_study_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Registrar tiempo de estudio"""
        user_id = update.effective_user.id
        
        if not context.args:
            # Mostrar opciones rápidas con botones
            keyboard = [
                [
                    InlineKeyboardButton("⏰ 30min", callback_data="study_0.5"),
                    InlineKeyboardButton("⏰ 1h", callback_data="study_1")
                ],
                [
                    InlineKeyboardButton("⏰ 1.5h", callback_data="study_1.5"),
                    InlineKeyboardButton("⏰ 2h", callback_data="study_2")
                ],
                [
                    InlineKeyboardButton("⏰ 3h", callback_data="study_3"),
                    InlineKeyboardButton("⏰ 4h+", callback_data="study_4")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "⏰ **¿Cuánto tiempo estudiaste hoy?**\n\n"
                "Selecciona una opción rápida o usa:\n"
                "`/estudie [horas]` (ej: `/estudie 2.5`)",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            return
            
        try:
            hours = float(context.args[0])
            if hours <= 0:
                await update.message.reply_text("⚠️ Las horas deben ser un número positivo")
                return
                
            await self.process_study_log(update, hours)
            
        except ValueError:
            await update.message.reply_text(
                "❌ **Formato incorrecto**\n\n"
                "Uso: `/estudie [horas]`\n\n"
                "**Ejemplos:**\n"
                "• `/estudie 2` - 2 horas\n"
                "• `/estudie 1.5` - 1 hora y 30 minutos\n"
                "• `/estudie 0.5` - 30 minutos",
                parse_mode='Markdown'
            )
            
    async def process_study_log(self, update, hours: float):
        """Procesar registro de tiempo de estudio"""
        user_id = update.effective_user.id
        
        # Registrar tiempo en la base de datos
        update_progress(user_id, 'study_hours', hours)
        stats = get_user_stats(user_id)
        
        # Mensaje personalizado según las horas
        if hours >= 4:
            reaction = "🔥 ¡BEAST MODE ACTIVADO!"
            emoji = "🔥"
        elif hours >= 3:
            reaction = "💪 ¡EXCELENTE dedicación!"
            emoji = "💪"
        elif hours >= 2:
            reaction = "⭐ ¡Muy buen trabajo!"
            emoji = "⭐"
        elif hours >= 1:
            reaction = "✅ ¡Perfecto! La constancia es clave"
            emoji = "✅"
        else:
            reaction = "👍 ¡Cada minuto cuenta!"
            emoji = "👍"
            
        # Verificar logros/milestones
        milestone_message = self.check_study_milestones(stats)
        
        message = f"""
{reaction}

⏰ **Tiempo registrado:** {hours}h {emoji}
📚 **Total acumulado:** {stats['total_hours']:.1f}h
🔥 **Streak actual:** {stats['current_streak']} días
📅 **Días estudiando:** {stats['study_days']}

💡 **Recuerda la regla 70/30:**
• 70% programando proyectos
• 30% viendo tutoriales

{milestone_message}

¡Sigue con ese ritmo! 🚀
"""
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    async def complete_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Marcar tarea como completada"""
        user_id = update.effective_user.id
        current_week = self.calculate_current_week(user_id)
        week_content = self.get_week_content(current_week)
        
        # Opciones de que puede completar
        keyboard = [
            [InlineKeyboardButton("🏆 Proyecto de la Semana", callback_data=f"complete_project_{current_week}")],
            [InlineKeyboardButton("🧠 Concepto/Skill Nueva", callback_data="complete_concept")],
            [InlineKeyboardButton("🎯 Objetivo Diario", callback_data="complete_daily")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"""
✅ **¿Qué completaste hoy?**

📅 **Semana {current_week}:** {week_content['title']}

📝 **Proyecto actual:** 
{week_content['project']['name']}

🎯 **Objetivo diario:** 
{week_content['daily_goal']}

Selecciona lo que lograste:
"""
        
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        
    async def motivation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enviar mensaje motivacional personalizado"""
        user_id = update.effective_user.id
        stats = get_user_stats(user_id)
        current_week = self.calculate_current_week(user_id)
        
        if not stats:
            await update.message.reply_text("❌ Error: Usuario no inicializado. Envía /start primero.")
            return
        
        # Mensaje base aleatorio
        base_message = random.choice(MOTIVATIONAL_PHRASES)
        
        # Contexto personal
        personal_touches = []
        
        current_streak = stats.get('current_streak', 0)
        projects_completed = stats.get('projects_completed', 0)
        total_hours = stats.get('total_hours', 0)
        
        if current_streak >= 7:
            personal_touches.append(f"🔥 ¡INCREÍBLE! Llevas {current_streak} días seguidos!")
        elif current_streak > 0:
            personal_touches.append(f"⭐ ¡{current_streak} días de streak!")
            
        if projects_completed >= 3:
            personal_touches.append(f"🏆 Ya completaste {projects_completed} proyectos!")
        elif projects_completed > 0:
            personal_touches.append(f"📝 {projects_completed} proyecto(s) completado(s)!")
            
        if total_hours >= 50:
            personal_touches.append(f"⏰ ¡{stats['total_hours']:.0f} horas de dedicación!")
            
        if not personal_touches:
            personal_touches.append("🚀 ¡Tu journey apenas comienza!")
            
        # Motivación específica de la semana
        week_motivation = self.get_week_specific_motivation(current_week)
        
        # Consejo personalizado
        progress_advice = self.get_progress_specific_advice(stats, current_week)
        
        full_message = f"""
🚀 **¡BOOST DE MOTIVACIÓN!**

{base_message}

{random.choice(personal_touches)}

💭 **Para la semana {current_week}:**
{week_motivation}

🎯 **Consejo personalizado:**
{progress_advice}

🏆 **Mantra del día:**
"No existe código perfecto, solo código que funciona y se puede mejorar"

**¡TÚ PUEDES HACERLO!** 💪✨
"""
        
        await update.message.reply_text(full_message, parse_mode='Markdown')
        
    async def show_objectives(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mostrar objetivos actuales"""
        user_id = update.effective_user.id
        current_week = self.calculate_current_week(user_id)
        week_content = self.get_week_content(current_week)
        stats = get_user_stats(user_id)
        
        if not stats:
            await update.message.reply_text("❌ Error: Usuario no inicializado. Envía /start primero.")
            return
        
        points_earned = stats.get('projects_completed', 0) + (stats.get('concepts_mastered', 0) * 0.5)
        target_this_week = current_week * 1.25
        
        message = f"""
🎯 **TUS OBJETIVOS ACTUALES**

📅 **Semana {current_week}/{TOTAL_WEEKS}:** {week_content['title']}

🎯 **Objetivo Principal:**
{week_content['goal']}

📝 **Proyecto de la Semana:**
{week_content['project']['name']}

🎯 **Objetivo Diario:**
{week_content['daily_goal']}

📊 **Progreso de Puntos:**
• Puntos actuales: {points_earned:.1f}/{POINTS_TARGET}
• Meta semana {current_week}: {target_this_week:.1f} puntos
• {self.get_points_status(points_earned, target_this_week)}

🎯 **Para completar esta semana:**
{self.get_week_completion_advice(current_week, stats)}

💡 **Tip clave:**
{week_content['tip']}

¡Enfócate en UN objetivo a la vez! 🚀
"""
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    async def show_resources(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mostrar recursos de la semana actual"""
        user_id = update.effective_user.id
        current_week = self.calculate_current_week(user_id)
        week_content = self.get_week_content(current_week)
        
        keyboard = [
            [InlineKeyboardButton("🎥 Videos", callback_data=f"videos_{current_week}")],
            [InlineKeyboardButton("🛠️ Herramientas", callback_data=f"tools_{current_week}")],
            [InlineKeyboardButton("📚 Documentación", callback_data="docs_general")],
            [InlineKeyboardButton("🌐 Sitios de Práctica", callback_data="practice_sites")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"""
📚 **RECURSOS PARA SEMANA {current_week}**

**{week_content['title']}**

🎯 **Objetivo:** {week_content['goal']}

Selecciona el tipo de recurso que necesitas:
"""
        
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        
    async def next_step(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mostrar próximos pasos"""
        user_id = update.effective_user.id
        current_week = self.calculate_current_week(user_id)
        stats = get_user_stats(user_id)
        
        if current_week >= TOTAL_WEEKS:
            next_steps = """
🎉 **¡PROGRAMA COMPLETADO!**

🚀 **Próximos pasos profesionales:**
• 💼 Aplica a trabajos junior/trainee
• 🔧 Continúa con proyectos personales
• 🌐 Contribuye a open source
• 📱 Amplía tu network profesional
• ⚡ Especialízate en un framework

¡Es hora de conseguir ese trabajo! 💼
"""
        else:
            next_week_content = self.get_week_content(current_week + 1)
            points_earned = stats['projects_completed'] + (stats['concepts_mastered'] * 0.5)
            
            next_steps = f"""
🔮 **¿QUÉ SIGUE DESPUÉS?**

📅 **Próxima semana ({current_week + 1}/{TOTAL_WEEKS}):**
{next_week_content['title']}

🎯 **Nuevo objetivo:**
{next_week_content['goal']}

📝 **Próximo proyecto:**
{next_week_content['project']['name']}

📊 **Tu progreso actual:**
• Puntos: {points_earned:.1f}/{POINTS_TARGET}
• Meta próxima semana: {(current_week + 1) * 1.25:.1f}

💡 **Consejo:**
{next_week_content['tip']}

**⚠️ ¡Primero termina la semana actual!** 💪
"""
        
        await update.message.reply_text(next_steps, parse_mode='Markdown')
        
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar todos los callbacks de botones inline"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        data = query.data
        
        # Contenido semanal
        if data.startswith("videos_"):
            week = int(data.split("_")[1])
            await self.show_week_videos(query, week)
            
        elif data.startswith("tools_"):
            week = int(data.split("_")[1])
            await self.show_week_tools(query, week)
            
        elif data.startswith("project_"):
            week = int(data.split("_")[1])
            await self.show_project_details(query, week)
            
        elif data.startswith("tip_"):
            week = int(data.split("_")[1])
            await self.show_week_tip(query, week)
            
        # Registro de tiempo
        elif data.startswith("study_"):
            hours = float(data.split("_")[1])
            await self.process_study_log_callback(query, hours)
            
        # Completar tareas
        elif data.startswith("complete_project_"):
            week = int(data.split("_")[2])
            await self.complete_project_callback(query, week)
            
        elif data == "complete_concept":
            await self.complete_concept_callback(query)
            
        elif data == "complete_daily":
            await self.complete_daily_callback(query)
            
        # Recursos generales
        elif data == "docs_general":
            await self.show_documentation(query)
            
        elif data == "practice_sites":
            await self.show_practice_sites(query)
            
    # Métodos para callbacks específicos
    
    async def show_week_videos(self, query, week: int):
        """Mostrar videos de la semana"""
        week_content = self.get_week_content(week)
        
        message = f"""
📺 **VIDEOS RECOMENDADOS - SEMANA {week}**

**{week_content['title']}**

{week_content['videos']}

💡 **Regla de oro:**
Pausa cada 5 minutos e intenta replicar el código sin mirar!

🎯 **Regla 70/30:**
• 70% programando proyectos
• 30% viendo tutoriales

⚡ **No copies código directamente. Entiende primero.**
"""
        
        await query.edit_message_text(message, parse_mode='Markdown')
        
    async def show_week_tools(self, query, week: int):
        """Mostrar herramientas de la semana"""
        week_content = self.get_week_content(week)
        
        message = f"""
🛠️ **HERRAMIENTAS PARA PRACTICAR - SEMANA {week}**

**{week_content['title']}**

{week_content['tools']}

🎮 **¡Importante!**
Estas herramientas son para PRACTICAR, no solo leer.

🎯 **Sugerencia:**
Dedica mínimo 1 hora diaria a estas plataformas.

💪 **¡La programación se aprende programando!**
"""
        
        await query.edit_message_text(message, parse_mode='Markdown')
        
    async def show_project_details(self, query, week: int):
        """Mostrar detalles del proyecto semanal"""
        week_content = self.get_week_content(week)
        
        message = f"""
📝 **PROYECTO SEMANA {week} - DETALLES**

**"{week_content['project']['name']}"**

📋 **Requisitos específicos:**
{week_content['project']['requirements']}

⏰ **Tiempo estimado:** {week_content['estimated_time']}

🎯 **Objetivo principal:**
{week_content['goal']}

💡 **Tip clave:**
{week_content['tip']}

🚀 **Recordatorio importante:**
¡Haz deploy cuando termines! (Netlify, Vercel, GitHub Pages)

📸 **No olvides tomar screenshots para tu portfolio**
"""
        
        await query.edit_message_text(message, parse_mode='Markdown')
        
    async def show_week_tip(self, query, week: int):
        """Mostrar tip de la semana"""
        week_content = self.get_week_content(week)
        
        # Tips adicionales específicos por semana
        extra_tips = {
            1: "• Flexbox = 1 dimensión (fila O columna)\n• Grid = 2 dimensiones (filas Y columnas)\n• Practica 30 min diarios mínimo",
            2: "• Mobile-first = diseña para 320px primero\n• Después agrega breakpoints\n• Usa rem/em en lugar de px",
            3: "• Variables CSS van en :root\n• Úsalas para colores y espaciado\n• Mantiene consistencia",
            4: "• Grid para layout principal\n• Flexbox para alineación interna\n• Combina ambas técnicas",
            5: "• const para valores fijos\n• let para variables\n• Evita var por completo",
            6: "• querySelector > getElementById\n• addEventListener > onclick\n• Valida que elementos existan",
            7: "• fetch() devuelve promesas\n• Siempre maneja errores\n• async/await > .then()",
            8: "• Planifica antes de codear\n• Divide en tareas pequeñas\n• Un feature a la vez"
        }
        
        extra_tip = extra_tips.get(week, "• Constancia diaria\n• Más código, menos videos\n• Cada línea cuenta")
        
        message = f"""
💡 **TIP DE LA SEMANA {week}**

**{week_content['title']}**

🎯 **Tip principal:**
{week_content['tip']}

🔥 **Tips adicionales:**
{extra_tip}

⭐ **Recuerda siempre:**
La programación se aprende PROGRAMANDO, no viendo videos!

💪 **¡Pon en práctica cada concepto inmediatamente!**
"""
        
        await query.edit_message_text(message, parse_mode='Markdown')
        
    async def process_study_log_callback(self, query, hours: float):
        """Procesar registro de tiempo desde callback"""
        user_id = query.from_user.id
        
        # Registrar tiempo
        update_progress(user_id, 'study_hours', hours)
        stats = get_user_stats(user_id)
        
        # Mensaje de confirmación
        if hours >= 3:
            reaction = "🔥 ¡BEAST MODE!"
        elif hours >= 2:
            reaction = "💪 ¡Excelente!"
        elif hours >= 1:
            reaction = "✅ ¡Perfecto!"
        else:
            reaction = "👍 ¡Bien hecho!"
            
        message = f"""
{reaction}

⏰ **Tiempo registrado:** {hours}h
📚 **Total acumulado:** {stats['total_hours']:.1f}h
🔥 **Streak:** {stats['current_streak']} días

{self.check_study_milestones(stats)}

¡Sigue así! 🚀
"""
        
        await query.edit_message_text(message, parse_mode='Markdown')
        
    async def complete_project_callback(self, query, week: int):
        """Manejar completar proyecto semanal"""
        user_id = query.from_user.id
        
        # Registrar proyecto completado
        update_progress(user_id, 'project_completed', week)
        stats = get_user_stats(user_id)
        
        congratulations = [
            "🎉 ¡EXCELENTE! ¡Proyecto completado!",
            "🚀 ¡INCREÍBLE! +1 punto ganado!",
            "⭐ ¡GENIAL! Cada proyecto cuenta!",
            "🔥 ¡IMPARABLE! ¡Sigue así!",
            "💪 ¡FANTÁSTICO! Buen trabajo!"
        ]
        
        points_earned = stats['projects_completed'] + (stats['concepts_mastered'] * 0.5)
        
        message = f"""
{random.choice(congratulations)}

🏆 **Proyecto Semana {week} Completado ✅**

📊 **Progreso actualizado:**
• Puntos totales: {points_earned:.1f}/{POINTS_TARGET}
• Proyectos: {stats['projects_completed']}
• Progreso: {(points_earned/POINTS_TARGET)*100:.1f}%

🎯 **¿Qué sigue?**
{self.get_next_step_after_project(week)}

🎉 **¡Tómate un descanso, te lo mereces!** 😊

📸 **No olvides hacer screenshots para tu portfolio**
"""
        
        await query.edit_message_text(message, parse_mode='Markdown')
        
    async def complete_concept_callback(self, query):
        """Manejar completar concepto/skill"""
        user_id = query.from_user.id
        
        # Registrar concepto dominado
        update_progress(user_id, 'concept_mastered', 1)
        stats = get_user_stats(user_id)
        
        points_earned = stats['projects_completed'] + (stats['concepts_mastered'] * 0.5)
        
        message = f"""
🧠 **¡Concepto Dominado!** +0.5 puntos

✨ **Excelente progreso incremental!**

📊 **Progreso actualizado:**
• Puntos: {points_earned:.1f}/{POINTS_TARGET}
• Conceptos: {stats['concepts_mastered']}

💡 **Recuerda:** 
¡Los pequeños logros suman para el gran objetivo!

🚀 **¡Sigue aprendiendo paso a paso!**
"""
        
        await query.edit_message_text(message, parse_mode='Markdown')
        
    async def complete_daily_callback(self, query):
        """Manejar completar objetivo diario"""
        user_id = query.from_user.id
        current_week = self.calculate_current_week(user_id)
        week_content = self.get_week_content(current_week)
        
        message = f"""
🎯 **¡Objetivo Diario Completado!**

✅ **Lograste hoy:**
{week_content['daily_goal']}

💪 **¡Excelente constancia diaria!**

📅 **Mañana continúa con:**
{self.get_tomorrow_suggestion(current_week)}

⭐ **Cada día cuenta para tu objetivo. ¡Sigue así!** 🌟
"""
        
        await query.edit_message_text(message, parse_mode='Markdown')
        
    async def show_documentation(self, query):
        """Mostrar documentación general"""
        message = """
📚 **DOCUMENTACIÓN Y REFERENCIAS**

🌐 **Recursos Oficiales:**
• MDN Web Docs - https://developer.mozilla.org/
• CSS Tricks - https://css-tricks.com/
• JavaScript.info - https://javascript.info/
• Web.dev - https://web.dev/

🎨 **CSS y Diseño:**
• CSS Grid Garden - https://cssgridgarden.com/
• Flexbox Froggy - https://flexboxfroggy.com/
• Can I Use - https://caniuse.com/

🔧 **Herramientas:**
• VS Code - Editor recomendado
• Chrome DevTools - Debugging
• Git & GitHub - Control de versiones

💡 **Tip:** Usa MDN como tu referencia principal. Es la documentación más confiable.
"""
        
        await query.edit_message_text(message, parse_mode='Markdown')
        
    async def show_practice_sites(self, query):
        """Mostrar sitios de práctica"""
        message = """
🌐 **SITIOS PARA PRACTICAR CÓDIGO**

🎮 **Interactivos CSS:**
• CSS Grid Garden - Grid layouts
• Flexbox Froggy - Flexbox
• CSS Battle - Desafíos creativos

🧩 **JavaScript:**
• Codewars - Algoritmos
• LeetCode - Programación
• HackerRank - Challenges

🎨 **Proyectos Reales:**
• Frontend Mentor - Diseños reales
• DevChallenges - Proyectos full stack
• 100 Days CSS - Desafíos diarios

🚀 **Para Practicar Deploy:**
• Netlify - Static sites
• Vercel - Next.js y más
• GitHub Pages - Repositorios

💡 **Tip:** Combina teoría con práctica diaria. ¡30 min/día marcan la diferencia!
"""
        
        await query.edit_message_text(message, parse_mode='Markdown')
        
    # Métodos auxiliares
    
    def generate_progress_bar(self, percentage: float) -> str:
        """Generar barra de progreso visual"""
        filled = int(percentage // 10)
        empty = 10 - filled
        return "▓" * filled + "░" * empty
        
    def calculate_level(self, points: float) -> int:
        """Calcular nivel basado en puntos"""
        if points >= 12:
            return 5  # Job Ready
        elif points >= 9:
            return 4  # Advanced
        elif points >= 6:
            return 3  # Intermediate
        elif points >= 3:
            return 2  # Beginner+
        else:
            return 1  # Beginner
            
    def get_level_name(self, level: int) -> str:
        """Obtener nombre del nivel"""
        names = {
            1: "Beginner Coder",
            2: "Aspiring Developer", 
            3: "Intermediate Builder",
            4: "Advanced Creator",
            5: "Job Ready Developer"
        }
        return names.get(level, "Coding Master")
        
    def calculate_pace_feedback(self, week: int, points: float) -> str:
        """Calcular feedback del ritmo"""
        expected_points = week * 1.25
        
        if points >= expected_points + 1:
            return "🚀 ¡Ritmo EXCELENTE! Vas adelantado"
        elif points >= expected_points:
            return "✅ ¡Ritmo PERFECTO! En el objetivo"
        elif points >= expected_points - 1:
            return "⚠️ Ritmo bueno, se puede mejorar"
        else:
            return "🔥 ¡Acelera el ritmo! ¡Tú puedes!"
            
    def get_next_milestone(self, points: float) -> str:
        """Obtener próximo hito"""
        milestones = [3, 6, 9, 12, 15]
        
        for milestone in milestones:
            if points < milestone:
                points_needed = milestone - points
                return f"🎯 {points_needed:.1f} puntos para próximo hito ({milestone})"
        
        return "🎉 ¡Todos los hitos completados!"
        
    def get_motivational_badges(self, stats: dict) -> str:
        """Obtener badges motivacionales"""
        badges = []
        
        if stats['current_streak'] >= 10:
            badges.append("🔥 STREAK MASTER")
        elif stats['current_streak'] >= 5:
            badges.append("⭐ CONSISTENT")
            
        if stats['total_hours'] >= 100:
            badges.append("⏰ CENTURY")
        elif stats['total_hours'] >= 50:
            badges.append("💪 DEDICATED")
            
        if stats['projects_completed'] >= 5:
            badges.append("🏆 BUILDER")
            
        if badges:
            return f"\n🏅 **Badges:** {' | '.join(badges)}"
        else:
            return "\n🌟 ¡Sigue así para desbloquear badges!"
            
    def check_study_milestones(self, stats: dict) -> str:
        """Verificar hitos de estudio"""
        milestones = []
        
        total_hours = int(stats['total_hours'])
        if total_hours in [10, 25, 50, 100]:
            milestones.append(f"🏆 ¡{total_hours}h milestone!")
            
        streak = stats['current_streak']
        if streak in [5, 10, 15, 21, 30]:
            milestones.append(f"🔥 ¡{streak} días streak!")
            
        return "\n".join(milestones) if milestones else ""
        
    def get_week_specific_motivation(self, week: int) -> str:
        """Motivación específica por semana"""
        motivations = {
            1: "CSS puede ser frustrante, ¡pero es tu herramienta más poderosa!",
            2: "Responsive design separa pros de principiantes",
            3: "Variables CSS cambiarán tu forma de programar", 
            4: "Este proyecto es tu prueba de fuego en CSS",
            5: "Corregir conceptos erróneos te hará mejor",
            6: "El DOM es tu playground. ¡Domínalo!",
            7: "APIs abren un mundo infinito de posibilidades",
            8: "Proyectos complejos se construyen paso a paso",
            9: "E-commerce demuestra tu nivel profesional",
            10: "Los detalles marcan la diferencia",
            11: "Tu portfolio es tu carta de presentación",
            12: "¡Estás a semanas de tu primer trabajo dev!"
        }
        return motivations.get(week, "¡Cada día te acerca más a tu objetivo!")
        
    def get_progress_specific_advice(self, stats: dict, week: int) -> str:
        """Consejo específico según progreso"""
        points = stats['projects_completed'] + (stats['concepts_mastered'] * 0.5)
        expected = week * 1.25
        
        if stats['current_streak'] == 0:
            return "Empieza un nuevo streak hoy. ¡30 minutos cuentan!"
        elif points < expected - 2:
            return "Enfócate en completar el proyecto semanal. ¡Prioridad!"
        elif stats['total_hours'] < week * 10:
            return "Aumenta tu tiempo diario. Calidad + cantidad = éxito"
        else:
            return "¡Vas por buen camino! Mantén constancia y disciplina"
            
    def get_week_completion_advice(self, current_week: int, stats: dict) -> str:
        """Consejo para completar la semana"""
        week_content = self.get_week_content(current_week)
        project_name = week_content['project']['name']
        
        if stats['projects_completed'] < current_week:
            return f"Termina el proyecto: {project_name}"
        else:
            return "¡Proyecto completado! Refina detalles o avanza"
            
    def get_points_status(self, current: float, target: float) -> str:
        """Estado de puntos vs objetivo"""
        if current >= target:
            return "✅ ¡Objetivo alcanzado!"
        else:
            diff = target - current
            return f"⚠️ Faltan {diff:.1f} puntos"
            
    def get_tomorrow_suggestion(self, week: int) -> str:
        """Sugerencia para mañana"""
        suggestions = [
            "Continúa con el proyecto semanal",
            "Practica lo aprendido ayer", 
            "Revisa y refactoriza tu código",
            "Agrega una nueva funcionalidad",
            "Haz deploy de tu progreso"
        ]
        return random.choice(suggestions)
        
    def get_next_step_after_project(self, week: int) -> str:
        """Próximo paso después de completar proyecto"""
        if week < TOTAL_WEEKS:
            next_week_content = self.get_week_content(week + 1)
            return f"Prepárate para Semana {week + 1}: {next_week_content['title']}"
        else:
            return "¡Es hora de aplicar a trabajos junior!"
    
    # NUEVOS MÉTODOS - Sistema de Evidencias y Validación
    
    async def submit_evidence(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /evidencia - Enviar evidencia de proyecto"""
        user_id = update.effective_user.id
        current_week = self.calculate_current_week(user_id)
        
        # Mostrar opciones de evidencia
        keyboard = [
            [InlineKeyboardButton("📸 Subir Captura", callback_data=f"evidence_screenshot_{current_week}")],
            [InlineKeyboardButton("🌐 URL del Proyecto", callback_data=f"evidence_url_{current_week}")],
            [InlineKeyboardButton("📁 Repositorio GitHub", callback_data=f"evidence_github_{current_week}")],
            [InlineKeyboardButton("💬 Explicación Técnica", callback_data=f"evidence_explanation_{current_week}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        week_content = self.get_week_content(current_week)
        
        message = f"""
📸 **ENVIAR EVIDENCIA - SEMANA {current_week}**

📝 **Proyecto:** {week_content['project']['name']}

🎯 **Tipos de evidencia requerida:**
• **Captura:** Proyecto funcionando en navegador
• **URL:** Link del proyecto desplegado 
• **GitHub:** Repositorio con código fuente
• **Explicación:** 3 conceptos técnicos usados

⚠️ **IMPORTANTE:** Sin evidencias válidas no puedes avanzar a la siguiente semana.

Selecciona el tipo de evidencia a enviar:
"""
        
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_photo_evidence(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar capturas enviadas como evidencia"""
        user_id = update.effective_user.id
        current_week = self.calculate_current_week(user_id)
        
        # Obtener información de la foto
        photo = update.message.photo[-1]  # La más grande
        file = await context.bot.get_file(photo.file_id)
        
        # Validar evidencia
        validation_result = evidence_validator.submit_evidence(
            user_id, current_week, "screenshot_project", f"photo_id:{photo.file_id}"
        )
        
        if validation_result['status'] == 'approved':
            response = f"✅ **Captura validada correctamente**\n\n{validation_result['message']}"
        else:
            response = f"⚠️ **Captura recibida**\n\n{validation_result['message']}"
        
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def start_exam(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /examen - Iniciar examen semanal"""
        user_id = update.effective_user.id
        current_week = self.calculate_current_week(user_id)
        
        # Verificar si puede tomar el examen
        can_advance, reason = evidence_validator.can_advance_to_week(user_id, current_week + 1)
        
        if not can_advance and STRICT_VALIDATION:
            await update.message.reply_text(
                f"❌ **No puedes tomar el examen**\n\n{reason}\n\nCompleta las evidencias primero con /evidencia",
                parse_mode='Markdown'
            )
            return
        
        # Iniciar examen
        exam_config, message = exam_manager.start_exam(user_id, current_week)
        
        if not exam_config:
            await update.message.reply_text(f"❌ {message}", parse_mode='Markdown')
            return
        
        # Mostrar primera pregunta
        questions = exam_config['questions']
        first_question = questions[0]
        
        if first_question['type'] == 'multiple_choice':
            keyboard = []
            for option in first_question['options']:
                callback_data = f"exam_answer_{current_week}_0_{option[0]}"
                keyboard.append([InlineKeyboardButton(option, callback_data=callback_data)])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            exam_message = f"""
📝 **EXAMEN SEMANA {current_week}** - {exam_config['title']}

**Pregunta 1/{len(questions)}:**

{first_question['question']}

Selecciona tu respuesta:
"""
            
            await update.message.reply_text(exam_message, reply_markup=reply_markup, parse_mode='Markdown')
        
        else:
            # Pregunta de evidencia o texto libre
            exam_message = f"""
📝 **EXAMEN SEMANA {current_week}** - {exam_config['title']}

**Pregunta 1/{len(questions)}:**

{first_question['question']}

{first_question.get('instructions', 'Envía tu respuesta como mensaje de texto.')}
"""
            
            await update.message.reply_text(exam_message, parse_mode='Markdown')
    
    async def check_validation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /validacion - Verificar estado de validación"""
        user_id = update.effective_user.id
        current_week = self.calculate_current_week(user_id)
        
        # Verificar estado de evidencias
        evidence_status = evidence_validator.get_week_evidence_status(user_id, current_week)
        
        # Verificar último examen
        exam_result = exam_manager.get_latest_exam_result(user_id, current_week)
        
        message = f"""
🔍 **ESTADO DE VALIDACIÓN - SEMANA {current_week}**

📸 **EVIDENCIAS:**
"""
        
        for evidence_type, status in evidence_status.items():
            if status['status'] == 'approved':
                message += f"✅ {evidence_type}: Aprobada\n"
            elif status['status'] == 'pending_review':
                message += f"⏳ {evidence_type}: Pendiente revisión\n"
            elif status['status'] == 'invalid':
                message += f"❌ {evidence_type}: Rechazada\n"
            else:
                message += f"⚠️ {evidence_type}: Faltante\n"
        
        message += f"\n📝 **EXAMEN:**\n"
        
        if exam_result:
            if exam_result['passed']:
                message += f"✅ Aprobado ({int(exam_result['score'] * 100)}%)\n"
            else:
                message += f"❌ Reprobado ({int(exam_result['score'] * 100)}%) - Intento #{exam_result['attempt_number']}\n"
        else:
            message += "⚠️ No tomado\n"
        
        # Verificar si puede avanzar
        can_advance, reason = evidence_validator.can_advance_to_week(user_id, current_week + 1)
        
        message += f"\n🚀 **ESTADO GENERAL:**\n"
        if can_advance:
            message += "✅ Puedes avanzar a la siguiente semana"
        else:
            message += f"❌ {reason}"
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def week_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /estado - Estado completo de la semana"""
        user_id = update.effective_user.id
        current_week = self.calculate_current_week(user_id)
        
        week_content = self.get_week_content(current_week)
        evidence_status = evidence_validator.get_week_evidence_status(user_id, current_week)
        exam_result = exam_manager.get_latest_exam_result(user_id, current_week)
        
        # Calcular progreso
        total_requirements = len(evidence_status) + 1  # evidencias + examen
        completed_requirements = 0
        
        for status in evidence_status.values():
            if status['status'] == 'approved':
                completed_requirements += 1
        
        if exam_result and exam_result['passed']:
            completed_requirements += 1
        
        progress_percentage = (completed_requirements / total_requirements) * 100
        
        message = f"""
📊 **ESTADO COMPLETO - SEMANA {current_week}/12**

**{week_content['title']}**

📈 **PROGRESO:** {progress_percentage:.0f}% completado
▓▓▓▓▓▓▓▓▓▓ {completed_requirements}/{total_requirements} requisitos

🎯 **PROYECTO:** {week_content['project']['name']}

📸 **EVIDENCIAS:** {len([s for s in evidence_status.values() if s['status'] == 'approved'])}/{len(evidence_status)} aprobadas

📝 **EXAMEN:** {"✅ Aprobado" if exam_result and exam_result['passed'] else "❌ Pendiente"}

⏰ **TIEMPO ESTIMADO:** {week_content['estimated_time']}

💡 **TIP:** {week_content['tip']}

🎯 **OBJETIVO DIARIO:** {week_content['daily_goal']}
"""
        
        # Botones de acción
        keyboard = []
        if completed_requirements < total_requirements:
            keyboard.append([InlineKeyboardButton("📸 Enviar Evidencia", callback_data=f"evidence_menu_{current_week}")])
            if exam_result is None or not exam_result['passed']:
                keyboard.append([InlineKeyboardButton("📝 Tomar Examen", callback_data=f"start_exam_{current_week}")])
        
        keyboard.append([InlineKeyboardButton("🔍 Ver Validación", callback_data=f"check_validation_{current_week}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
        
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

def main():
    """Función principal"""
    # Inicializar base de datos
    init_db()
    
    # Crear y configurar bot
    bot = StudyMentorBot()
    
    logger.info("🤖 Bot Mentor de Desarrollo Web iniciado")
    logger.info("🔗 Busca tu bot en Telegram y envía /start")
    logger.info("📱 Todos los comandos y botones están funcionando")
    logger.info("Presiona Ctrl+C para detener")
    
    # Iniciar bot
    bot.app.run_polling()

if __name__ == '__main__':
    main()

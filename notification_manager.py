#!/usr/bin/env python3
"""
Sistema de Notificaciones Diarias del Bot Mentor
Maneja recordatorios, motivación y validación de progreso semanal
"""

import asyncio
import logging
import random
from datetime import datetime, timedelta, time
from typing import Dict, Any
from telegram import Bot
from telegram.error import TelegramError
import schedule
import threading
import time as time_module

from config import (
    BOT_TOKEN, DAILY_STUDY_REMINDER, MOTIVATIONAL_REMINDER, 
    AI_MOTIVATIONAL_PHRASES, DAILY_NOTIFICATIONS, WEEK_DEADLINE_DAYS,
    WEEK_COMPLETION_REQUIRED, AUTO_RESET_INCOMPLETE_WEEKS
)
from database import get_all_users, get_user_stats, update_progress
from evidence_manager import evidence_validator, exam_manager

logger = logging.getLogger(__name__)

class NotificationManager:
    def __init__(self, bot_token: str):
        """Inicializar el sistema de notificaciones"""
        self.bot = Bot(token=bot_token)
        self.running = False
        self.scheduler_thread = None
        
    def start_scheduler(self):
        """Iniciar el scheduler de notificaciones"""
        if not DAILY_NOTIFICATIONS:
            logger.info("Notificaciones diarias deshabilitadas")
            return
            
        self.running = True
        
        # Programar notificaciones diarias
        schedule.every().day.at(DAILY_STUDY_REMINDER).do(self._send_daily_study_reminder)
        schedule.every().day.at(MOTIVATIONAL_REMINDER).do(self._send_motivational_message)
        schedule.every().day.at("23:59").do(self._check_weekly_progress)
        
        # Ejecutar scheduler en thread separado
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("Sistema de notificaciones iniciado")
        logger.info(f"Recordatorio diario: {DAILY_STUDY_REMINDER}")
        logger.info(f"Motivación diaria: {MOTIVATIONAL_REMINDER}")
        
    def stop_scheduler(self):
        """Detener el scheduler"""
        self.running = False
        schedule.clear()
        logger.info("Sistema de notificaciones detenido")
        
    def _run_scheduler(self):
        """Ejecutar scheduler en loop"""
        while self.running:
            schedule.run_pending()
            time_module.sleep(60)  # Verificar cada minuto
            
    def _send_daily_study_reminder(self):
        """Enviar recordatorio diario de estudio"""
        asyncio.run(self._async_send_daily_reminder())
        
    def _send_motivational_message(self):
        """Enviar mensaje motivacional diario"""
        asyncio.run(self._async_send_motivational_message())
        
    def _check_weekly_progress(self):
        """Verificar progreso semanal y resetear si es necesario"""
        asyncio.run(self._async_check_weekly_progress())
        
    async def _async_send_daily_reminder(self):
        """Enviar recordatorio diario a todos los usuarios"""
        try:
            users = get_all_users()
            
            for user_id, username in users:
                try:
                    stats = get_user_stats(user_id)
                    if not stats:
                        continue
                        
                    # Calcular semana actual
                    current_week = self._calculate_current_week(stats)
                    
                    # Generar mensaje personalizado
                    message = self._generate_daily_reminder_message(stats, current_week)
                    
                    await self.bot.send_message(
                        chat_id=user_id,
                        text=message,
                        parse_mode='Markdown'
                    )
                    
                    logger.info(f"Recordatorio diario enviado a {username} (ID: {user_id})")
                    
                except TelegramError as e:
                    logger.error(f"Error enviando recordatorio a {user_id}: {e}")
                    
        except Exception as e:
            logger.error(f"Error en recordatorio diario: {e}")
            
    async def _async_send_motivational_message(self):
        """Enviar mensaje motivacional diario"""
        try:
            users = get_all_users()
            
            for user_id, username in users:
                try:
                    stats = get_user_stats(user_id)
                    if not stats:
                        continue
                        
                    # Seleccionar frase motivacional única del día
                    daily_phrase = self._get_daily_motivational_phrase()
                    
                    # Generar mensaje motivacional personalizado
                    message = self._generate_motivational_message(stats, daily_phrase)
                    
                    await self.bot.send_message(
                        chat_id=user_id,
                        text=message,
                        parse_mode='Markdown'
                    )
                    
                    logger.info(f"Motivación diaria enviada a {username} (ID: {user_id})")
                    
                except TelegramError as e:
                    logger.error(f"Error enviando motivación a {user_id}: {e}")
                    
        except Exception as e:
            logger.error(f"Error en motivación diaria: {e}")
            
    async def _async_check_weekly_progress(self):
        """Verificar progreso semanal y resetear si es necesario"""
        try:
            users = get_all_users()
            
            for user_id, username in users:
                try:
                    stats = get_user_stats(user_id)
                    if not stats:
                        continue
                        
                    current_week = self._calculate_current_week(stats)
                    
                    # Verificar si debe resetear la semana
                    if await self._should_reset_week(user_id, current_week):
                        await self._reset_user_to_previous_week(user_id, current_week)
                        logger.info(f"Usuario {username} reseteado a semana anterior")
                        
                except Exception as e:
                    logger.error(f"Error verificando progreso de {user_id}: {e}")
                    
        except Exception as e:
            logger.error(f"Error en verificación semanal: {e}")
            
    def _calculate_current_week(self, stats: Dict[str, Any]) -> int:
        """Calcular semana actual basada en fecha de inicio"""
        if not stats.get('start_date'):
            return 1
            
        start_date = datetime.strptime(str(stats['start_date']), "%Y-%m-%d").date()
        days_passed = (datetime.now().date() - start_date).days
        current_week = min((days_passed // 7) + 1, 12)
        
        return current_week
        
    def _get_daily_motivational_phrase(self) -> str:
        """Obtener frase motivacional única del día"""
        # Usar fecha como seed para consistencia diaria
        today = datetime.now().date()
        random.seed(today.toordinal())
        
        phrase = random.choice(AI_MOTIVATIONAL_PHRASES)
        
        # Resetear seed
        random.seed()
        
        return phrase
        
    def _generate_daily_reminder_message(self, stats: Dict[str, Any], current_week: int) -> str:
        """Generar mensaje de recordatorio personalizado"""
        username = stats.get('username', 'Developer')
        streak = stats.get('current_streak', 0)
        total_hours = stats.get('total_hours', 0)
        
        # Mensaje base
        message = f"☀️ **¡Buenos días, {username}!**\n\n"
        
        # Estadísticas motivacionales
        if streak >= 5:
            message += f"🔥 **¡Increíble streak de {streak} días!** Eres imparable\n\n"
        elif streak > 0:
            message += f"⭐ **Streak de {streak} días** - ¡Mantén el impulso!\n\n"
        else:
            message += f"🌟 **¡Nuevo día, nueva oportunidad!** Empieza tu streak hoy\n\n"
            
        # Información de la semana
        message += f"📅 **Semana {current_week}/12** - ¡Sigues avanzando!\n"
        message += f"⏰ **Horas acumuladas:** {total_hours:.1f}h\n\n"
        
        # Recordatorio de estudio
        message += f"📚 **Recordatorio de hoy:**\n"
        message += f"• Dedica al menos 1 hora a programar\n"
        message += f"• Regla 70/30: más código, menos videos\n"
        message += f"• Registra tu progreso con /estudie\n\n"
        
        # Call to action
        message += f"🎯 **¡Empieza ahora!** Envía /semana para ver qué trabajar hoy\n\n"
        message += f"💪 **¡Tu futuro developer te está esperando!**"
        
        return message
        
    def _generate_motivational_message(self, stats: Dict[str, Any], daily_phrase: str) -> str:
        """Generar mensaje motivacional personalizado"""
        username = stats.get('username', 'Developer')
        current_week = self._calculate_current_week(stats)
        
        message = f"🌙 **¡Buenas noches, {username}!**\n\n"
        message += f"💭 **Inspiración del día:**\n{daily_phrase}\n\n"
        
        # Reflexión del día
        message += f"🤔 **Reflexión:**\n"
        message += f"• ¿Qué aprendiste hoy?\n"
        message += f"• ¿Qué reto superaste?\n"
        message += f"• ¿Cómo te acercaste a tu objetivo?\n\n"
        
        # Motivación para mañana
        message += f"🌅 **Mañana será un gran día para:**\n"
        message += f"• Escribir código que funcione\n"
        message += f"• Resolver un problema complejo\n"
        message += f"• Aprender algo nuevo\n\n"
        
        message += f"✨ **¡Descansa bien, mañana seguimos construyendo tu futuro!**"
        
        return message
        
    async def _should_reset_week(self, user_id: int, current_week: int) -> bool:
        """Verificar si debe resetear la semana por falta de progreso"""
        if not WEEK_COMPLETION_REQUIRED or not AUTO_RESET_INCOMPLETE_WEEKS:
            return False
            
        # Verificar si ha pasado el deadline
        stats = get_user_stats(user_id)
        if not stats:
            return False
            
        start_date = datetime.strptime(str(stats['start_date']), "%Y-%m-%d").date()
        days_passed = (datetime.now().date() - start_date).days
        
        # Si han pasado más de 7 días desde el inicio de la semana
        week_start_day = (current_week - 1) * 7
        if days_passed <= week_start_day + WEEK_DEADLINE_DAYS:
            return False
            
        # Verificar si completó los requisitos de la semana
        return not await self._week_completed(user_id, current_week)
        
    async def _week_completed(self, user_id: int, week: int) -> bool:
        """Verificar si completó todos los requisitos de la semana"""
        # Verificar evidencias
        evidence_status = evidence_validator.get_week_evidence_status(user_id, week)
        for evidence_type, status in evidence_status.items():
            if status['status'] != 'approved':
                return False
                
        # Verificar examen
        exam_result = exam_manager.get_latest_exam_result(user_id, week)
        if not exam_result or not exam_result['passed']:
            return False
            
        return True
        
    async def _reset_user_to_previous_week(self, user_id: int, current_week: int):
        """Resetear usuario a la semana anterior"""
        try:
            previous_week = max(1, current_week - 1)
            
            # Actualizar semana en base de datos
            update_progress(user_id, 'reset_week', previous_week)
            
            # Enviar notificación de reset
            message = f"""
⚠️ **SEMANA RESTABLECIDA**

📅 **De semana {current_week} → semana {previous_week}**

🎯 **Motivo:** No completaste todos los requisitos de la semana {current_week}

📋 **Para avanzar necesitas:**
• ✅ Completar proyecto semanal
• ✅ Aprobar examen (70% mínimo)
• ✅ Enviar todas las evidencias

💪 **¡No te desanimes!** Cada reset es una oportunidad para:
• Reforzar conceptos
• Mejorar tu proyecto
• Dominar completamente la semana

🚀 **Usa /semana para ver qué completar**

¡Tú puedes hacerlo! 💪
"""
            
            await self.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info(f"Usuario {user_id} reseteado de semana {current_week} a {previous_week}")
            
        except Exception as e:
            logger.error(f"Error reseteando usuario {user_id}: {e}")

# Instancia global
notification_manager = NotificationManager(BOT_TOKEN)

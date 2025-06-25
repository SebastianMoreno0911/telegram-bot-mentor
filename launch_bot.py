#!/usr/bin/env python3
"""
🚀 BOT MENTOR - LANZADOR TEMPORAL (SOLO POLLING)
Versión temporal que solo usa polling para evitar problemas de webhook
"""

import os
import sys
import logging
from pathlib import Path

# Configurar la ruta base del proyecto automáticamente
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Configurar zona horaria
os.environ.setdefault('TZ', 'America/Bogota')

def setup_logging():
    """Configurar sistema de logging mejorado"""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Crear directorio de logs si no existe
    log_dir = PROJECT_ROOT / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # Configurar logging con rotación
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'bot.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Reducir logs de librerías externas
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.WARNING)

def check_environment():
    """Verificar configuración del entorno"""
    from dotenv import load_dotenv
    
    # Cargar variables de entorno
    env_path = PROJECT_ROOT / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Configuración cargada desde: {env_path}")
    else:
        print(f"⚠️  Archivo .env no encontrado en: {env_path}")
        print("📝 Usando variables de entorno del sistema (Render/Railway)")
    
    # Verificar variables obligatorias (intentar ambos nombres)
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN') or os.getenv('BOT_TOKEN')
    
    if not bot_token:
        print("❌ Variable faltante: TELEGRAM_BOT_TOKEN")
        print("💡 Configura las variables de entorno en Render:")
        print("   - TELEGRAM_BOT_TOKEN: Tu token de BotFather")
        print("   - ENVIRONMENT: production")
        return False
    
    print("✅ Configuración de entorno correcta")
    return True

def check_database():
    """Inicializar base de datos"""
    try:
        from database import init_db
        
        # Usar ruta absoluta para la base de datos
        db_path = PROJECT_ROOT / 'study_mentor.db'
        init_db()
        print(f"✅ Base de datos inicializada: {db_path}")
        return True
    except Exception as e:
        print(f"❌ Error configurando base de datos: {e}")
        return False

def check_dependencies():
    """Verificar dependencias instaladas"""
    try:
        import telegram
        from dotenv import load_dotenv
        print("✅ Dependencias básicas instaladas")
        
        # Verificar dependencias opcionales
        try:
            import twilio
            print("✅ Twilio (WhatsApp) disponible")
        except ImportError:
            print("⚠️  Twilio no instalado - WhatsApp deshabilitado")
            
        return True
    except ImportError as e:
        print(f"❌ Dependencias faltantes: {e}")
        print("📦 Ejecuta: pip install -r requirements.txt")
        return False

def main():
    """Función principal - SOLO POLLING"""
    print("=" * 60)
    print("🤖 BOT MENTOR DE DESARROLLO WEB - SEBASTIÁN")
    print("🔄 MODO TEMPORAL: SOLO POLLING")
    print("=" * 60)
    print(f"📁 Directorio del proyecto: {PROJECT_ROOT}")
    print(f"🐍 Python: {sys.version}")
    print(f"💻 Sistema: {sys.platform}")
    print("=" * 60)
    
    # Configurar logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Verificaciones previas
    if not check_dependencies():
        logger.error("Dependencias faltantes")
        return
    
    if not check_environment():
        logger.error("Variables de entorno faltantes")
        return
    
    if not check_database():
        logger.error("Error de base de datos")
        return
    
    # Detectar entorno de ejecución
    is_cloud = os.getenv('PORT') or os.getenv('RENDER') or os.getenv('RENDER_EXTERNAL_HOSTNAME')
    
    if is_cloud:
        print("☁️  Ejecutando en entorno de nube")
        print("🔄 USANDO POLLING (temporal para solucionar webhook)")
    else:
        print("💻 Ejecutando en entorno local")
    
    try:
        # Importar y iniciar el bot
        from bot_final import StudyMentorBot
        
        logger.info("Iniciando Bot Mentor...")
        print("🚀 Bot iniciando...")
        
        bot = StudyMentorBot()
        
        # SIEMPRE usar polling (temporal)
        if is_cloud:
            port = int(os.getenv('PORT', 8000))
            print(f"☁️  Puerto detectado: {port} (no usado en polling)")
            logger.info(f"Bot iniciado en modo cloud - Polling temporal")
        else:
            logger.info("Bot iniciado en modo local")
        
        print("🔄 Usando polling mode")
        print("💡 Bot funcionando - Presiona Ctrl+C para detener")
        bot.app.run_polling(drop_pending_updates=True)
    
    except KeyboardInterrupt:
        print("\n🔴 Bot detenido por el usuario")
        logger.info("Bot detenido por el usuario")
    
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        logger.error(f"Error crítico: {e}", exc_info=True)

if __name__ == '__main__':
    main()

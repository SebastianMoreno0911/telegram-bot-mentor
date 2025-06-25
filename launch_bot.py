#!/usr/bin/env python3
"""
🚀 BOT MENTOR - LANZADOR UNIVERSAL
Funciona desde cualquier ubicación y preparado para la nube
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
        print("📝 Copia .env.example a .env y configúralo")
        return False
    
    # Verificar variables obligatorias
    required_vars = ['BOT_TOKEN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Variables faltantes en .env: {', '.join(missing_vars)}")
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
    """Función principal mejorada"""
    print("=" * 60)
    print("🤖 BOT MENTOR DE DESARROLLO WEB - SEBASTIÁN")
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
        input("❌ Presiona Enter para salir...")
        return
    
    if not check_environment():
        input("❌ Presiona Enter para salir...")
        return
    
    if not check_database():
        input("❌ Presiona Enter para salir...")
        return
    
    # Detectar entorno de ejecución
    is_cloud = os.getenv('PORT') or os.getenv('DYNO') or os.getenv('RAILWAY_ENVIRONMENT')
    
    if is_cloud:
        print("☁️  Ejecutando en entorno de nube")
    else:
        print("💻 Ejecutando en entorno local")
    
    try:
        # Importar y iniciar el bot
        from bot_final import StudyMentorBot
        
        logger.info("Iniciando Bot Mentor...")
        print("🚀 Bot iniciando...")
        
        bot = StudyMentorBot()
        
        if is_cloud:
            # Configuración para deployment en la nube
            port = int(os.getenv('PORT', 8000))
            print(f"☁️  Iniciando en puerto {port}")
            logger.info(f"Bot iniciado en modo cloud - Puerto: {port}")
            
            # Para Railway, Heroku, etc.
            bot.app.run_webhook(
                listen="0.0.0.0",
                port=port,
                webhook_url=os.getenv('WEBHOOK_URL', '')
            )
        else:
            # Configuración para ejecución local
            print("💻 Iniciando en modo local (polling)")
            print("🔄 Bot funcionando - Presiona Ctrl+C para detener")
            logger.info("Bot iniciado en modo local")
            
            bot.app.run_polling(drop_pending_updates=True)
    
    except KeyboardInterrupt:
        print("\n🔴 Bot detenido por el usuario")
        logger.info("Bot detenido por el usuario")
    
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        logger.error(f"Error crítico: {e}", exc_info=True)
        
        if not is_cloud:
            input("❌ Presiona Enter para salir...")

if __name__ == '__main__':
    main()

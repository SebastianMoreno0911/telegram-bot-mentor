import sqlite3
from datetime import datetime, date
import json

DB_FILE = 'study_mentor.db'

def init_db(user_id=None, username=None):
    """Inicializar base de datos y usuario"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        start_date DATE,
        current_week INTEGER DEFAULT 1,
        total_points REAL DEFAULT 0,
        projects_completed INTEGER DEFAULT 0,
        concepts_mastered INTEGER DEFAULT 0,
        total_hours REAL DEFAULT 0,
        study_days INTEGER DEFAULT 0,
        current_streak INTEGER DEFAULT 0,
        last_study_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Crear tabla de progreso diario
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date DATE,
        hours_studied REAL DEFAULT 0,
        tasks_completed TEXT,
        notes TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    # Crear tabla de evaluaciones semanales
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weekly_evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        week_number INTEGER,
        project_completed BOOLEAN DEFAULT 0,
        difficulty_level INTEGER,
        concepts_learned TEXT,
        next_week_focus TEXT,
        evaluation_date DATE,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    # Si se proporciona user_id, crear/actualizar usuario
    if user_id:
        cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, start_date) 
        VALUES (?, ?, ?)
        ''', (user_id, username, date.today()))
    
    conn.commit()
    conn.close()

def update_progress(user_id: int, progress_type: str, value):
    """Actualizar progreso del usuario"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    today = date.today()
    
    if progress_type == 'study_hours':
        # Verificar si ya estudió hoy
        cursor.execute('''
        SELECT last_study_date FROM users WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        last_date = result[0] if result else None
        is_new_day = str(last_date) != str(today)
        
        # Actualizar horas de estudio
        cursor.execute('''
        UPDATE users 
        SET total_hours = total_hours + ?, 
            last_study_date = ?,
            study_days = study_days + ?,
            current_streak = CASE 
                WHEN ? THEN current_streak + 1 
                ELSE current_streak 
            END
        WHERE user_id = ?
        ''', (value, today, 1 if is_new_day else 0, is_new_day, user_id))
        
        # Registrar en progreso diario
        cursor.execute('''
        INSERT OR REPLACE INTO daily_progress (user_id, date, hours_studied)
        VALUES (?, ?, COALESCE((SELECT hours_studied FROM daily_progress WHERE user_id = ? AND date = ?), 0) + ?)
        ''', (user_id, today, user_id, today, value))
        
    elif progress_type == 'project_completed':
        cursor.execute('''
        UPDATE users 
        SET projects_completed = projects_completed + 1,
            total_points = total_points + 1,
            current_week = ?
        WHERE user_id = ?
        ''', (value, user_id))
        
    elif progress_type == 'concept_mastered':
        cursor.execute('''
        UPDATE users 
        SET concepts_mastered = concepts_mastered + 1,
            total_points = total_points + 0.5
        WHERE user_id = ?
        ''', (user_id,))
        
    elif progress_type == 'reset_week':
        cursor.execute('''
        UPDATE users 
        SET current_week = ?
        WHERE user_id = ?
        ''', (value, user_id))
    
    conn.commit()
    conn.close()

def get_user_stats(user_id: int) -> dict:
    """Obtener estadísticas del usuario"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM users WHERE user_id = ?
    ''', (user_id,))
    
    user_data = cursor.fetchone()
    
    if user_data:
        # Verificar streak actual
        last_date = datetime.strptime(str(user_data[10]), "%Y-%m-%d").date() if user_data[10] else None
        current_streak = user_data[9]
        
        # Si no estudió ayer, resetear streak
        if last_date and (date.today() - last_date).days > 1:
            current_streak = 0
            cursor.execute('''
            UPDATE users SET current_streak = 0 WHERE user_id = ?
            ''', (user_id,))
            conn.commit()
        
        conn.close()
        
        return {
            'user_id': user_data[0],
            'username': user_data[1],
            'start_date': user_data[2],
            'current_week': user_data[3],
            'total_points': user_data[4],
            'projects_completed': user_data[5],
            'concepts_mastered': user_data[6],
            'total_hours': user_data[7],
            'study_days': user_data[8],
            'current_streak': current_streak,
            'last_study_date': last_date
        }
    
    conn.close()
    return {}

def save_weekly_evaluation(user_id: int, week: int, evaluation_data: dict):
    """Guardar evaluación semanal"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR REPLACE INTO weekly_evaluations 
    (user_id, week_number, project_completed, difficulty_level, concepts_learned, next_week_focus, evaluation_date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, 
        week, 
        evaluation_data.get('project_completed', False),
        evaluation_data.get('difficulty_level', 3),
        evaluation_data.get('concepts_learned', ''),
        evaluation_data.get('next_week_focus', ''),
        date.today()
    ))
    
    conn.commit()
    conn.close()

def get_weekly_evaluation(user_id: int, week: int) -> dict:
    """Obtener evaluación de una semana específica"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM weekly_evaluations WHERE user_id = ? AND week_number = ?
    ''', (user_id, week))
    
    evaluation = cursor.fetchone()
    conn.close()
    
    if evaluation:
        return {
            'week_number': evaluation[2],
            'project_completed': evaluation[3],
            'difficulty_level': evaluation[4],
            'concepts_learned': evaluation[5],
            'next_week_focus': evaluation[6],
            'evaluation_date': evaluation[7]
        }
    
    return {}

def get_study_history(user_id: int, days: int = 7) -> list:
    """Obtener historial de estudio de los últimos N días"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT user_id, date, hours_studied FROM daily_progress 
    WHERE user_id = ? 
    ORDER BY date DESC 
    LIMIT ?
    ''', (user_id, days))
    
    history = cursor.fetchall()
    conn.close()
    
    return history

def get_all_users() -> list:
    """Obtener todos los usuarios activos para recordatorios"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT user_id, username FROM users 
    WHERE total_hours > 0 OR projects_completed > 0
    ORDER BY last_study_date DESC
    ''')
    
    users = cursor.fetchall()
    conn.close()
    
    return users

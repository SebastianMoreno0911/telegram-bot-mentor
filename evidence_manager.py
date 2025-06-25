import sqlite3
import json
import requests
import re
from datetime import datetime, date
from config import WEEKLY_EXAMS, EVIDENCE_VALIDATION, EXAM_THRESHOLD, EVIDENCE_REQUIRED
from database import get_user_stats, update_progress
import logging

logger = logging.getLogger(__name__)

class EvidenceValidator:
    def __init__(self):
        """Inicializar validador de evidencias"""
        self.setup_evidence_db()
    
    def setup_evidence_db(self):
        """Crear tabla para evidencias"""
        conn = sqlite3.connect('study_mentor.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evidences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                week INTEGER,
                evidence_type TEXT,
                content TEXT,
                status TEXT DEFAULT 'pending',
                submitted_date DATE DEFAULT CURRENT_DATE,
                reviewed_date DATE,
                score REAL,
                feedback TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exam_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                week INTEGER,
                exam_type TEXT DEFAULT 'weekly',
                score REAL,
                passed BOOLEAN,
                attempt_number INTEGER DEFAULT 1,
                exam_date DATE DEFAULT CURRENT_DATE,
                answers TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def submit_evidence(self, user_id: int, week: int, evidence_type: str, content: str):
        """Enviar evidencia para validación"""
        conn = sqlite3.connect('study_mentor.db')
        cursor = conn.cursor()
        
        # Verificar si ya existe evidencia para esta semana/tipo
        cursor.execute('''
            SELECT id FROM evidences 
            WHERE user_id = ? AND week = ? AND evidence_type = ?
        ''', (user_id, week, evidence_type))
        
        existing = cursor.fetchone()
        
        if existing:
            # Actualizar evidencia existente
            cursor.execute('''
                UPDATE evidences 
                SET content = ?, status = 'pending', submitted_date = CURRENT_DATE
                WHERE id = ?
            ''', (content, existing[0]))
        else:
            # Crear nueva evidencia
            cursor.execute('''
                INSERT INTO evidences (user_id, week, evidence_type, content, status)
                VALUES (?, ?, ?, ?, 'pending')
            ''', (user_id, week, evidence_type, content))
        
        conn.commit()
        conn.close()
        
        return self.validate_evidence(user_id, week, evidence_type, content)
    
    def validate_evidence(self, user_id: int, week: int, evidence_type: str, content: str):
        """Validar evidencia automáticamente"""
        validation_config = EVIDENCE_VALIDATION.get(evidence_type, {})
        
        if evidence_type == "deployed_url":
            return self.validate_deployed_url(content)
        elif evidence_type == "github_repository":
            return self.validate_github_repo(content)
        elif evidence_type == "screenshot_project":
            return self.validate_screenshot(content)
        else:
            # Validación manual requerida
            return {
                "status": "pending_review",
                "message": "Evidencia enviada. Requiere revisión manual.",
                "auto_validated": False
            }
    
    def validate_deployed_url(self, url: str):
        """Validar que la URL esté desplegada y funcionando"""
        try:
            # Verificar formato de URL
            if not re.match(r'https?://', url):
                return {
                    "status": "invalid",
                    "message": "URL debe comenzar con http:// o https://",
                    "auto_validated": True
                }
            
            # Hacer request para verificar que funciona
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Verificar que no sea página por defecto
                content = response.text.lower()
                default_indicators = [
                    "welcome to nginx",
                    "default web page",
                    "it works!",
                    "apache default page"
                ]
                
                if any(indicator in content for indicator in default_indicators):
                    return {
                        "status": "invalid",
                        "message": "La URL muestra una página por defecto, no tu proyecto",
                        "auto_validated": True
                    }
                
                return {
                    "status": "approved",
                    "message": "✅ URL validada correctamente",
                    "auto_validated": True
                }
            else:
                return {
                    "status": "invalid",
                    "message": f"URL no accesible (Error {response.status_code})",
                    "auto_validated": True
                }
                
        except requests.RequestException as e:
            return {
                "status": "invalid",
                "message": f"Error al acceder a la URL: {str(e)}",
                "auto_validated": True
            }
    
    def validate_github_repo(self, url: str):
        """Validar repositorio de GitHub"""
        try:
            # Verificar formato de GitHub
            github_pattern = r'https://github\.com/[^/]+/[^/]+'
            if not re.match(github_pattern, url):
                return {
                    "status": "invalid", 
                    "message": "Debe ser una URL válida de GitHub (https://github.com/usuario/repo)",
                    "auto_validated": True
                }
            
            # Verificar que el repo existe (usando API de GitHub)
            api_url = url.replace('github.com', 'api.github.com/repos')
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                repo_data = response.json()
                
                # Verificar que no esté vacío
                if repo_data.get('size', 0) == 0:
                    return {
                        "status": "invalid",
                        "message": "El repositorio está vacío",
                        "auto_validated": True
                    }
                
                return {
                    "status": "approved",
                    "message": "✅ Repositorio GitHub validado",
                    "auto_validated": True
                }
            else:
                return {
                    "status": "invalid",
                    "message": "Repositorio no encontrado o es privado",
                    "auto_validated": True
                }
                
        except Exception as e:
            return {
                "status": "pending_review",
                "message": f"Error validando repo: {str(e)}. Requiere revisión manual.",
                "auto_validated": False
            }
    
    def validate_screenshot(self, file_info: str):
        """Validar captura de pantalla"""
        # Por ahora, aceptar todas las capturas para revisión manual
        return {
            "status": "pending_review",
            "message": "Captura recibida. Se validará manualmente.",
            "auto_validated": False
        }
    
    def get_week_evidence_status(self, user_id: int, week: int):
        """Obtener estado de evidencias de una semana"""
        conn = sqlite3.connect('study_mentor.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT evidence_type, status, score, feedback
            FROM evidences 
            WHERE user_id = ? AND week = ?
        ''', (user_id, week))
        
        evidences = cursor.fetchall()
        conn.close()
        
        # Obtener evidencias requeridas para la semana
        exam_config = WEEKLY_EXAMS.get(week, {})
        required_evidences = []
        
        for question in exam_config.get('questions', []):
            if question.get('type') == 'evidence':
                required_evidences.extend(question.get('required_evidence', []))
        
        # Calcular estado
        evidence_status = {}
        for evidence_type in set(required_evidences):
            found = False
            for ev in evidences:
                if ev[0] == evidence_type:
                    evidence_status[evidence_type] = {
                        'status': ev[1],
                        'score': ev[2],
                        'feedback': ev[3]
                    }
                    found = True
                    break
            
            if not found:
                evidence_status[evidence_type] = {
                    'status': 'missing',
                    'score': None,
                    'feedback': None
                }
        
        return evidence_status
    
    def can_advance_to_week(self, user_id: int, target_week: int):
        """Verificar si puede avanzar a la semana objetivo"""
        if not EVIDENCE_REQUIRED:
            return True, "Validación de evidencias deshabilitada"
        
        previous_week = target_week - 1
        if previous_week < 1:
            return True, "Primera semana"
        
        # Verificar evidencias de la semana anterior
        evidence_status = self.get_week_evidence_status(user_id, previous_week)
        
        missing_evidences = []
        for evidence_type, status in evidence_status.items():
            if status['status'] in ['missing', 'invalid']:
                missing_evidences.append(evidence_type)
        
        if missing_evidences:
            return False, f"Faltan evidencias de semana {previous_week}: {', '.join(missing_evidences)}"
        
        # Verificar examen de la semana anterior
        exam_result = self.get_latest_exam_result(user_id, previous_week)
        if not exam_result or not exam_result['passed']:
            return False, f"Debes aprobar el examen de la semana {previous_week}"
        
        return True, "Puede avanzar"

class ExamManager:
    def __init__(self):
        """Inicializar manejador de exámenes"""
        self.evidence_validator = EvidenceValidator()
    
    def start_exam(self, user_id: int, week: int, exam_type: str = 'weekly'):
        """Iniciar examen para una semana"""
        exam_config = WEEKLY_EXAMS.get(week)
        if not exam_config:
            return None, "No hay examen configurado para esta semana"
        
        # Verificar intentos previos
        attempt_number = self.get_attempt_number(user_id, week, exam_type)
        
        if attempt_number > 3:
            return None, "Máximo de intentos alcanzado (3). Contacta al mentor."
        
        return exam_config, f"Examen iniciado. Intento #{attempt_number}"
    
    def submit_exam_answer(self, user_id: int, week: int, question_index: int, answer: str):
        """Enviar respuesta individual del examen"""
        exam_config = WEEKLY_EXAMS.get(week)
        if not exam_config:
            return False, "Examen no encontrado"
        
        questions = exam_config.get('questions', [])
        if question_index >= len(questions):
            return False, "Pregunta no encontrada"
        
        question = questions[question_index]
        
        # Validar según tipo de pregunta
        if question['type'] == 'multiple_choice':
            correct = answer.upper() == question['correct'].upper()
            feedback = question.get('explanation', '') if not correct else "¡Correcto!"
            return correct, feedback
        
        elif question['type'] == 'evidence':
            # Procesar evidencias
            required_evidences = question.get('required_evidence', [])
            # Por ahora, marcar como pendiente de revisión
            return True, "Evidencias enviadas para revisión"
        
        else:
            # Respuesta de código o texto libre
            return True, "Respuesta registrada para revisión manual"
    
    def complete_exam(self, user_id: int, week: int, answers: dict):
        """Completar examen y calcular puntuación"""
        exam_config = WEEKLY_EXAMS.get(week)
        if not exam_config:
            return None
        
        questions = exam_config.get('questions', [])
        total_questions = len(questions)
        correct_answers = 0
        
        # Calcular puntuación automática (solo multiple choice)
        for i, question in enumerate(questions):
            if question['type'] == 'multiple_choice':
                user_answer = answers.get(str(i), '').upper()
                if user_answer == question['correct'].upper():
                    correct_answers += 1
        
        # Puntuación parcial (solo preguntas automáticas)
        auto_questions = [q for q in questions if q['type'] == 'multiple_choice']
        if auto_questions:
            auto_score = correct_answers / len(auto_questions)
        else:
            auto_score = 0.5  # Score neutral si no hay preguntas automáticas
        
        passed = auto_score >= EXAM_THRESHOLD
        
        # Guardar resultado
        self.save_exam_result(user_id, week, auto_score, passed, answers)
        
        return {
            'score': auto_score,
            'passed': passed,
            'correct_answers': correct_answers,
            'total_auto_questions': len(auto_questions),
            'pending_review': total_questions - len(auto_questions)
        }
    
    def save_exam_result(self, user_id: int, week: int, score: float, passed: bool, answers: dict):
        """Guardar resultado del examen"""
        conn = sqlite3.connect('study_mentor.db')
        cursor = conn.cursor()
        
        attempt_number = self.get_attempt_number(user_id, week)
        
        cursor.execute('''
            INSERT INTO exam_results (user_id, week, score, passed, attempt_number, answers)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, week, score, passed, attempt_number, json.dumps(answers)))
        
        conn.commit()
        conn.close()
    
    def get_attempt_number(self, user_id: int, week: int, exam_type: str = 'weekly'):
        """Obtener número de intento actual"""
        conn = sqlite3.connect('study_mentor.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT MAX(attempt_number) FROM exam_results 
            WHERE user_id = ? AND week = ? AND exam_type = ?
        ''', (user_id, week, exam_type))
        
        result = cursor.fetchone()
        conn.close()
        
        return (result[0] or 0) + 1
    
    def get_latest_exam_result(self, user_id: int, week: int):
        """Obtener último resultado del examen"""
        conn = sqlite3.connect('study_mentor.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT score, passed, attempt_number, exam_date, answers
            FROM exam_results 
            WHERE user_id = ? AND week = ?
            ORDER BY attempt_number DESC
            LIMIT 1
        ''', (user_id, week))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'score': result[0],
                'passed': result[1],
                'attempt_number': result[2],
                'exam_date': result[3],
                'answers': json.loads(result[4]) if result[4] else {}
            }
        return None

# Instancias globales
evidence_validator = EvidenceValidator()
exam_manager = ExamManager()

import os
from dotenv import load_dotenv

load_dotenv()

# Configuración del bot - Soporta ambos nombres de variables
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') or os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')  # Tu chat ID específico

# Sistema de Validación y Evidencias
EVIDENCE_REQUIRED = True  # Exigir evidencias para completar tareas
STRICT_VALIDATION = True  # No avanzar sin completar semana actual
EXAM_THRESHOLD = 0.7  # 70% mínimo para aprobar exámenes
WEEK_COMPLETION_REQUIRED = True  # Debe completar TODO para avanzar
AUTO_RESET_INCOMPLETE_WEEKS = True  # Restablecer si no completa semana

EVIDENCE_TYPES = [
    "screenshot_project",  # Captura del proyecto funcionando
    "deployed_url",        # URL del proyecto desplegado
    "github_repository",   # Repositorio en GitHub
    "code_explanation"     # Explicación técnica del código
]

# Configuración de la guía de estudio
TOTAL_WEEKS = 12
POINTS_TARGET = 15
DAILY_STUDY_REMINDER = "09:00"  # 9 AM
WEEKLY_CHECK_REMINDER = "18:00"  # 6 PM viernes
MOTIVATIONAL_REMINDER = "20:00"  # 8 PM
DAILY_NOTIFICATIONS = True  # Activar notificaciones diarias
WEEK_DEADLINE_DAYS = 7  # Días para completar una semana

# Frases motivacionales
MOTIVATIONAL_PHRASES = [
    "🚀 Cada línea de código te acerca a tu objetivo!",
    "💪 El tutorial hell se vence programando, no viendo videos!",
    "🎯 Recuerda: 70% práctica, 30% teoría!",
    "⭐ Tu futuro como developer empieza HOY!",
    "🔥 No existe código perfecto, solo código que funciona!",
    "🏆 Cada pequeño logro suma para tu gran objetivo!"
]

# Frases motivacionales generadas con IA - Se renuevan automáticamente
AI_MOTIVATIONAL_PHRASES = [
    "🌟 Recuerda: cada bug que resuelves te convierte en mejor programador",
    "🎯 La consistencia diaria vale más que sesiones maratónicas esporádicas",
    "💡 Hoy es un día perfecto para transformar una idea en código funcional",
    "🔥 Tu único competidor eres tú mismo de ayer - mejora aunque sea 1%",
    "🚀 Los desarrolladores exitosos no nacen, se hacen línea por línea",
    "💪 Cada función que escribes hoy es una habilidad que tendrás para siempre",
    "⭐ El código que escribas hoy puede cambiar el mundo mañana",
    "🎮 Programar es como un videojuego: cada error es experiencia ganada",
    "🌈 La programación es arte que resuelve problemas reales",
    "🔧 Un desarrollador es un solucionador de problemas con superpoderes",
    "📚 Aprender a programar es como aprender un idioma que habla el futuro",
    "🎨 Cada proyecto es tu lienzo, cada línea de código tu pincelada",
    "🏆 No se trata de ser perfecto, se trata de ser constante",
    "🔥 La programación no es sobre memorizar sintaxis, es sobre resolver problemas",
    "🌍 Cada desarrollador empezó exactamente donde estás tú ahora",
    "⚡ El mejor momento para empezar era ayer, el segundo mejor es ahora",
    "💻 Tu computadora es tu laboratorio, experimenta sin miedo",
    "🎯 Small steps daily lead to big changes yearly",
    "🌟 Cada error es una lección disfrazada, abraza el debugging",
    "🚀 Tu próximo commit puede ser el que cambie tu carrera",
    "🔥 La programación es 10% escribir código, 90% pensar en soluciones",
    "💡 Hoy vas a aprender algo que tu yo del pasado no sabía",
    "🎮 Level up your skills: un proyecto a la vez",
    "⭐ El código limpio es amor propio convertido en sintaxis",
    "🌈 Diversity in approaches leads to creative solutions",
    "🔧 Break it, fix it, learn from it - ese es el ciclo del growth",
    "📈 Tu progreso no se mide en líneas de código, sino en problemas resueltos",
    "🎨 Elegant code is a poem that computers can understand",
    "🏆 Persistence beats talent when talent doesn't persist",
    "🔥 Today's struggle is tomorrow's strength"
]

# Datos de la guía de estudio estructurados
STUDY_GUIDE = {
    1: {
        "title": "CSS Layouts Fundamentals",
        "phase": "CSS Dominance",
        "goal": "Entender la diferencia entre Flexbox y Grid",
        "videos": "• Kevin Powell - CSS Grid & Flexbox\n• Canal: @KevinPowell",
        "tools": "• CSS Grid Garden\n• Flexbox Froggy\n• CSS Battle (primeros 10)",
        "project": {
            "name": "Recrear la landing page de Apple iPhone",
            "requirements": "• Solo HTML y CSS\n• Sin JavaScript\n• Enfoque en layout"
        },
        "estimated_time": "15-20 horas",
        "tip": "Pausa el video cada 5 minutos e intenta hacerlo solo",
        "daily_goal": "Completa Flexbox Froggy niveles 1-12"
    },
    2: {
        "title": "Responsive Design",
        "phase": "CSS Dominance",
        "goal": "Dominar media queries y mobile-first",
        "videos": "• freeCodeCamp - Responsive Web Design\n• YouTube: srvUrASNdlk",
        "tools": "• Chrome DevTools - Modo responsive\n• Practica con diferentes breakpoints",
        "project": {
            "name": "Portfolio Personal Responsive",
            "requirements": "• 3 secciones: Hero, Proyectos, Contacto\n• Mobile-first approach\n• Sin framework CSS"
        },
        "estimated_time": "12-15 horas",
        "tip": "Siempre diseña primero para móvil, luego desktop",
        "daily_goal": "Configura breakpoints: 320px, 768px, 1024px"
    },
    3: {
        "title": "CSS Avanzado",
        "phase": "CSS Dominance", 
        "goal": "Código CSS reutilizable y animado",
        "videos": "• Kevin Powell - CSS Variables\n• Dev Ed - CSS Animations",
        "tools": "• CSS Variables practice\n• Animation playground",
        "project": {
            "name": "Dashboard Admin Panel",
            "requirements": "• Sidebar navigation\n• Cards con hover effects\n• Variables CSS para temas\n• Micro-animaciones"
        },
        "estimated_time": "18-20 horas",
        "tip": "Las variables CSS hacen tu código más mantenible",
        "daily_goal": "Implementa al menos 3 variables CSS en tu proyecto"
    },
    4: {
        "title": "CSS Consolidation",
        "phase": "CSS Dominance",
        "goal": "Demostrar dominio completo de CSS",
        "videos": "• Repaso de conceptos anteriores\n• Netflix CSS Grid Layout",
        "tools": "• Consolidación de conocimientos\n• Grid + Flexbox combinados",
        "project": {
            "name": "Clone de Netflix Homepage",
            "requirements": "• Layout complejo con Grid/Flexbox\n• Carousel de imágenes (solo CSS)\n• Responsive design\n• Variables CSS para colores"
        },
        "estimated_time": "20-25 horas",
        "tip": "Este proyecto demuestra todo lo que has aprendido",
        "daily_goal": "Combina Grid para layout general, Flexbox para componentes"
    },
    5: {
        "title": "Corrección de Conceptos JS",
        "phase": "JavaScript Intermedio",
        "goal": "Corregir conceptos incorrectos y modernizar código",
        "videos": "• Traversy Media - JavaScript ES6+\n• The Net Ninja - Modern JavaScript",
        "tools": "• MDN JavaScript docs\n• JavaScript.info",
        "project": {
            "name": "Calculadora Científica",
            "requirements": "• Arrow functions para operaciones\n• Let/const apropiadamente\n• Event listeners modernos"
        },
        "estimated_time": "12-15 horas",
        "tip": "Arrow functions ≠ if statements. Son funciones más concisas",
        "daily_goal": "Practica diferencias entre const, let y var"
    },
    6: {
        "title": "DOM Manipulation Mastery", 
        "phase": "JavaScript Intermedio",
        "goal": "Manipular DOM como un profesional",
        "videos": "• Traversy Media - JavaScript DOM Crash Course\n• ~4 horas de contenido",
        "tools": "• Chrome DevTools - Console\n• DOM practice playground",
        "project": {
            "name": "Todo App con LocalStorage",
            "requirements": "• Agregar/eliminar tareas\n• Filtros (todas/completadas/pendientes)\n• Persistencia con localStorage\n• Drag & drop para reordenar"
        },
        "estimated_time": "15-18 horas",
        "tip": "querySelector es tu mejor amigo para seleccionar elementos",
        "daily_goal": "Practica seleccionar elementos de 5 formas diferentes"
    },
    7: {
        "title": "APIs y Fetch",
        "phase": "JavaScript Intermedio", 
        "goal": "Conectar frontend con datos externos",
        "videos": "• Traversy Media - Fetch API & Async JavaScript\n• freeCodeCamp - Working with APIs",
        "tools": "• JSONPlaceholder\n• OpenWeatherMap API\n• Random User API",
        "project": {
            "name": "Weather App",
            "requirements": "• Consume API de clima\n• Muestra datos en tiempo real\n• Manejo de errores\n• Indicador de loading"
        },
        "estimated_time": "15-20 horas",
        "tip": "Las APIs son solo URLs que devuelven datos JSON",
        "daily_goal": "Haz tu primera llamada fetch() exitosa"
    },
    8: {
        "title": "JavaScript Project Integration",
        "phase": "JavaScript Intermedio",
        "goal": "Integrar múltiples conceptos JS en un proyecto",
        "videos": "• Repaso de fetch, DOM, localStorage\n• Best practices JavaScript",
        "tools": "• Multiple APIs\n• Advanced DOM manipulation",
        "project": {
            "name": "Social Media Dashboard", 
            "requirements": "• Consume 3 APIs diferentes\n• Manejo de estados de loading/error\n• Filtros y búsqueda en tiempo real\n• Responsive y animado"
        },
        "estimated_time": "20-25 horas",
        "tip": "Este proyecto combina todo lo aprendido hasta ahora",
        "daily_goal": "Integra al menos 2 APIs en el mismo proyecto"
    },
    9: {
        "title": "E-commerce Frontend (Parte 1)",
        "phase": "Proyectos Reales",
        "goal": "Aplicar todo lo aprendido en un proyecto real",
        "videos": "• freeCodeCamp - Build an E-commerce Website\n• Advanced JavaScript patterns",
        "tools": "• JSON data management\n• LocalStorage for cart\n• Advanced CSS",
        "project": {
            "name": "Tienda Online de Tecnología",
            "requirements": "• Catálogo de productos (desde JSON)\n• Carrito de compras (localStorage)\n• Filtros por categoría/precio\n• Búsqueda en tiempo real"
        },
        "estimated_time": "25-30 horas",
        "tip": "Planifica la estructura de datos antes de programar",
        "daily_goal": "Diseña la estructura del carrito de compras"
    },
    10: {
        "title": "E-commerce Frontend (Parte 2)",
        "phase": "Proyectos Reales",
        "goal": "Completar funcionalidades avanzadas del e-commerce",
        "videos": "• Checkout process\n• Form validation\n• UX best practices",
        "tools": "• Form validation\n• Payment UI (sin backend)\n• Advanced filtering",
        "project": {
            "name": "Completar Tienda Online",
            "requirements": "• Checkout form (sin backend)\n• Validación de formularios\n• Persistencia de datos\n• Responsive completo"
        },
        "estimated_time": "20-25 horas", 
        "tip": "La validación de formularios es crucial para UX",
        "daily_goal": "Implementa validación en tiempo real"
    },
    11: {
        "title": "Portfolio Profesional (Parte 1)",
        "phase": "Proyectos Reales",
        "goal": "Crear herramienta para conseguir trabajo - Estructura",
        "videos": "• Portfolio best practices\n• Personal branding\n• Responsive design mastery",
        "tools": "• Design inspiration\n• Personal brand development\n• Content strategy",
        "project": {
            "name": "Portfolio para Conseguir Trabajo",
            "requirements": "• Hero con animación\n• Sobre mí (historia de transición)\n• Proyectos (mínimo 5)\n• Habilidades técnicas"
        },
        "estimated_time": "20-25 horas",
        "tip": "Tu portfolio es tu primera impresión, hazla memorable",
        "daily_goal": "Escribe tu historia de transición a developer"
    }
}

# Sistema de Exámenes y Validación por Semana
WEEKLY_EXAMS = {
    1: {
        "title": "Examen CSS Layouts Fundamentals",
        "questions": [
            {
                "question": "¿Cuál es la diferencia principal entre Flexbox y Grid?",
                "type": "multiple_choice",
                "options": [
                    "A) Flexbox es para layouts 2D, Grid para 1D",
                    "B) Flexbox es para layouts 1D, Grid para 2D", 
                    "C) No hay diferencia, ambos son iguales",
                    "D) Flexbox es más moderno que Grid"
                ],
                "correct": "B",
                "explanation": "Flexbox está diseñado para layouts unidimensionales (fila o columna), mientras que Grid maneja layouts bidimensionales (filas y columnas simultáneamente)."
            },
            {
                "question": "¿Qué comando completa Flexbox Froggy nivel 12?",
                "type": "code",
                "expected_concepts": ["flex-direction", "flex-wrap", "align-content"],
                "validation": "practical"
            },
            {
                "question": "Muestra tu recreación de la landing page de Apple iPhone",
                "type": "evidence",
                "required_evidence": ["screenshot_project", "deployed_url", "github_repository"],
                "validation_criteria": [
                    "Layout similar al original",
                    "Solo HTML y CSS (sin JavaScript)",
                    "Responsive design básico",
                    "Código limpio y comentado"
                ]
            }
        ]
    },
    2: {
        "title": "Examen Responsive Design",
        "questions": [
            {
                "question": "¿Qué significa 'mobile-first' en CSS?",
                "type": "multiple_choice",
                "options": [
                    "A) Diseñar solo para móviles",
                    "B) Escribir CSS base para móvil y usar min-width para pantallas más grandes",
                    "C) Usar max-width para todos los breakpoints",
                    "D) Priorizar la velocidad en móviles"
                ],
                "correct": "B",
                "explanation": "Mobile-first significa escribir el CSS base para dispositivos móviles y luego usar min-width en media queries para adaptar a pantallas más grandes."
            },
            {
                "question": "Muestra tu Portfolio Personal Responsive funcionando",
                "type": "evidence", 
                "required_evidence": ["screenshot_project", "deployed_url", "mobile_test"],
                "validation_criteria": [
                    "3 secciones: Hero, Proyectos, Contacto",
                    "Mobile-first approach",
                    "Sin framework CSS",
                    "Funciona en diferentes tamaños de pantalla"
                ]
            }
        ]
    }
    # ... Agregar exámenes para las 12 semanas
}

# Validación de Evidencias
EVIDENCE_VALIDATION = {
    "screenshot_project": {
        "description": "Captura de pantalla del proyecto funcionando",
        "requirements": "Debe mostrar el resultado final, navegador visible, fecha actual",
        "format": "imagen (jpg, png, gif)"
    },
    "deployed_url": {
        "description": "URL del proyecto desplegado y funcionando",
        "requirements": "Debe ser accesible públicamente (Netlify, Vercel, GitHub Pages)",
        "validation": "auto_check_url"
    },
    "github_repository": {
        "description": "Repositorio en GitHub con el código fuente",
        "requirements": "Código limpio, README descriptivo, commits frecuentes",
        "validation": "check_repo_structure"
    },
    "code_explanation": {
        "description": "Explicación técnica de 3 conceptos clave utilizados",
        "requirements": "Mínimo 100 palabras por concepto, ejemplos específicos",
        "validation": "manual_review"
    },
    "mobile_test": {
        "description": "Prueba del proyecto en dispositivo móvil",
        "requirements": "Captura en móvil real o DevTools, diferentes breakpoints",
        "format": "imagen o video"
    }
}

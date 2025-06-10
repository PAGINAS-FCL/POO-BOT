
# Sistema de Microlearning Educativo en Telegram

Este sistema educativo está diseñado para ofrecer microlecciones secuenciales sobre **Programación Orientada a Objetos aplicada a HTML, CSS y JavaScript**, a través de Telegram usando FastAPI como backend.

## 🎯 Objetivo

Guiar a los usuarios paso a paso a través de 18 módulos educativos, con contenido multimedia, textos explicativos y preguntas que deben ser respondidas correctamente para avanzar. El sistema también gestiona el progreso, detecta bots maliciosos y puede reanudar el aprendizaje automáticamente si el usuario no continúa tras 24 horas. Ayuda al docente a visualizar el progreso de los estudiantes.

---

## 📁 Estructura del Proyecto

```
├── main.py # Punto de entrada FastAPI
├── requirements.txt # Dependencias del proyecto
├── modulos/
│ └── modulos.json # Contenido de los módulos del curso
├── servicios/
│ ├── gestor_modulos.py # Lógica de interacción y progresión
│ └── manejador_telegram.py # Comunicación con Telegram
├── utilidades/
│ └── json_utils.py # Utilidades para manejar JSON
├── data/
│ └── data.json # Registro general de todos los usuarios
├── frontend/
│ ├── index.html # Vista HTML para administrador
│ ├── estilos.css # Estilos visuales
│ └── script.js # Código JS para obtener progreso
```

---

## 📚 Contenido de los Módulos

Los módulos están definidos en `modulos.json`. Cada uno incluye:

- `video_url`: Enlace al video explicativo del módulo.
- `textos`: Lista de textos instructivos que introducen el contenido.
- `preguntas`: Lista de preguntas con sus respuestas correctas que deben ser respondidas para continuar.

Ejemplo de módulo:

```json
{
  "id": 1,
  "video_url": "https://www.youtube.com/watch?v=dmNC9VZNREw",
  "textos": [
    "La programación orientada a objetos (POO) es un paradigma que organiza el software usando objetos y clases.",
    "En HTML podemos preparar la estructura para que JavaScript implemente POO en las interacciones.",
    "Escribe **seguir** para continuar empezar las preguntas de este modulo."
  ],
  "preguntas": [
    {
      "pregunta": "¿Cuál es el paradigma que organiza software con objetos y clases?",
      "respuesta": "programación orientada a objetos"
    },
    {
      "pregunta": "¿En qué lenguaje web se puede aplicar POO para interacciones?",
      "respuesta": "javascript"
    }
  ]
}
```

---

## 🧠 Funcionalidades Clave

- 🔑 Solicita un **código de estudiante** al inicio.
- 📊 Registra el módulo alcanzado por cada código en `data/data.json`.
- 👁️ Interfaz web para visualizar el avance de todos los usuarios.
- 🔐 Filtrado básico antispam.
---

## 🚀 Cómo ejecutar

1. Clona este repositorio:
```bash
git clone https://github.com/PAGINAS-FCL/BOT-POO.git
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta el servidor:
```bash
uvicorn main:app --reload
```

---

## 🛠️ Requisitos

- Python 3.8+
- fastapi
- uvicorn
- httpx
- python-dotenv

---

## 💬 Contacto

Si deseas colaborar, reportar errores o hacer sugerencias,contactate con paginas-FCL

---

**¡Feliz aprendizaje!**

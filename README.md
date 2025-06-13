# Kodely

**Kodely** es una plataforma web desarrollada con Django, inspirada en dev.to, diseñada para que usuarios autenticados puedan redactar, publicar y visualizar tutoriales técnicos. Este proyecto fue creado con fines académicos como parte del curso Programación Web 1 de la Universidad del Valle de Guatemala, Campus Altiplano.

---

## Propósito del Proyecto

El objetivo de Kodely es ofrecer un entorno funcional, simple y seguro donde los estudiantes puedan compartir contenido técnico. La aplicación permite la autenticación mediante Google, publicación de textos enriquecidos sin imágenes, reacciones con emojis y un perfil personalizado para cada usuario.

---

## Funcionalidades Principales

- Inicio de sesión mediante Google (Firebase Authentication)
- Creación y edición de tutoriales con editor enriquecido (sin imágenes)
- Visualización de publicaciones con orden cronológico
- Reacciones con emojis en los tutoriales
- Página de perfil para ver publicaciones personales

---

## Estructura del Proyecto

```bash
Kodely/
├── accounts/                            # Módulo de autenticación y usuarios
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_post.py
│   │   └── 0003_reaction.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── firebase_config.py
│   ├── models.py                        # Modelos de Post y Reaction
│   ├── tests.py
│   ├── urls.py                          # Rutas del módulo
│   └── views.py                         # Vistas de login/logout
│
├── core/                                # Módulo central de vistas y contenido
│   ├── migrations/
│   │   └── __init__.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── create_post.css
│   │   │   ├── dashboard.css
│   │   │   ├── editar_post.css
│   │   │   ├── login.css
│   │   │   ├── perfil.css
│   │   │   └── ver_post.css
│   │   ├── img/
│   │   │   ├── LogoKodely.svg
│   │   │   └── logo_kodely.svg
│   │   └── js/
│   │       ├── auth.js
│   │       ├── firebase-init.js
│   │       ├── login.js
│   │       ├── logout.js
│   │       └── main.js
│   ├── templates/
│   │   ├── create_post.html
│   │   ├── editar_post.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── perfil.html
│   │   └── ver_post.html
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── kodely/                               # Configuración global del proyecto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                       # Configuración general
│   ├── urls.py                           # Rutas principales del sitio
│   └── wsgi.py
│
├── db.sqlite3                            # Base de datos de desarrollo local
├── firebase_config.py                    # Configuración Firebase (uso global)
├── manage.py                             # Comando de gestión de Django
├── requirements.txt                      # Dependencias del proyecto
├── .gitignore
├── LICENSE
└── README.md

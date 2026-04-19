# Sistema Académico

Sistema de gestión académica para la **Unidad Educativa Fiscal Jaime Roldós Aguilera**, desarrollado con Django y MySQL.

## Stack

- Python 3.14 · Django 5.1 · Django REST Framework
- MySQL (PyMySQL) · Bootstrap 4 (SB Admin 2)
- ReportLab / xhtml2pdf · OpenPyXL

## Instalación

```bash
# 1. Clonar y entrar al proyecto
git clone <url>
cd AmbienteDesarrolloPython

# 2. Entorno virtual
python -m venv venv
# Windows PowerShell:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt

# 3. Variables de entorno
cp .env.example .env   # editar con tus datos

# 4. Base de datos
# Crear en MySQL:
# CREATE DATABASE bd_academico CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
python manage.py migrate

# 5. Ejecutar
python manage.py runserver
```

Acceder a `http://localhost:8000/`

## Variables de entorno (.env)

| Variable | Descripción |
|----------|-------------|
| `SECRET_KEY` | Clave secreta Django |
| `DEBUG` | `True` en desarrollo, `False` en producción |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` |
| `DB_NAME` | Nombre de la base de datos |
| `DB_USER` | Usuario MySQL |
| `DB_PASSWORD` | Contraseña MySQL |
| `DB_HOST` | Host MySQL (`localhost`) |
| `DB_PORT` | Puerto MySQL (`3306`) |

## Módulos

| Módulo | Descripción |
|--------|-------------|
| Configuraciones | Empresa, usuarios, roles, menús, permisos, SMTP |
| Mantenimiento | CRUD de estudiantes y empleados |
| Matriculación | Año lectivo, cursos, paralelos, asignación de materias |
| Registro de Notas | Notas por quimestre, promedios, supletorios |
| Horarios | Asignación por curso y profesor |
| Reportes | PDF y Excel |
| API REST | Endpoints para menús y validaciones |

## Estructura

```
├── manage.py
├── requirements.txt
├── .env
├── sistemaAcademico/          # Configuración Django + App principal
│   └── Apps/GestionAcademica/
│       ├── Controladores/     # Vistas por módulo
│       ├── Diccionario/       # Modelos (conf_, genr_, mant_, mov_)
│       ├── Forms/             # Formularios Django
│       ├── Services/          # Lógica de negocio (matriculación, exportación)
│       └── urls.py
├── templates/                 # HTML (base_layout, login, módulos)
├── static/                    # CSS, JS, imágenes
└── logs/
```

## Tests

```bash
python manage.py test sistemaAcademico.Apps.GestionAcademica.tests
```

## Seguridad

- Contraseñas con PBKDF2 (migración automática desde SHA1 legacy)
- CSRF en todos los formularios
- Sesiones con expiración de 1 hora
- Permisos cacheados en sesión al login
- Logs de intentos de acceso fallidos

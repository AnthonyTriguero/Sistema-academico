# Sistema Académico

Sistema de gestión académica desarrollado con Django y MySQL. Permite administrar estudiantes, empleados, matriculación, cursos, notas, horarios y reportes para instituciones educativas.

## Tecnologías

- Python 3.14+
- Django 5.1 LTS
- Django REST Framework 3.17
- MySQL (driver PyMySQL)
- Bootstrap 4 (SB Admin 2)
- ReportLab / xhtml2pdf (generación de PDF)
- OpenPyXL / xlrd (generación de Excel)

## Arquitectura del Proyecto

```
AmbienteDesarrolloPython/
├── manage.py                          # Punto de entrada Django
├── requirements.txt                   # Dependencias del proyecto
├── .env                               # Variables de entorno (NO commitear)
├── .env.example                       # Plantilla de variables de entorno
│
├── sistemaAcademico/                  # Configuración principal Django
│   ├── __init__.py                    # Inicialización PyMySQL
│   ├── settings.py                    # Configuración (usa python-decouple)
│   ├── urls.py                        # URLs raíz del proyecto
│   └── wsgi.py                        # Punto de entrada WSGI
│
│   └── Apps/
│       ├── Validaciones.py            # Validadores reutilizables (cédula, RUC, etc.)
│       │
│       └── GestionAcademica/          # App principal
│           ├── apps.py
│           ├── models.py              # Importa modelos desde Diccionario/
│           ├── views.py               # Vistas principales (login, inicio, errores)
│           ├── urls.py                # Todas las rutas de la aplicación
│           ├── context_processors.py  # Permisos y acciones por usuario
│           ├── middleware.py          # Autenticación centralizada
│           ├── utils.py               # Hashing seguro (PBKDF2, migración SHA1)
│           ├── admin.py
│           │
│           ├── Diccionario/           # Modelos (tablas de la BD)
│           │   ├── Estructuras_tablas_conf.py  # Empresa, Usuario, Rol, Menú, Permiso
│           │   ├── Estructuras_tablas_genr.py  # Tabla general (catálogos)
│           │   ├── Estructuras_tablas_mant.py  # Persona, Estudiante, Empleado
│           │   └── Estructuras_tablas_mov.py   # Matrícula, Curso, Notas, Horario
│           │
│           ├── Controladores/         # Lógica de vistas por módulo
│           │   ├── API/               # Endpoints REST (Menu, Unidad, Usuario)
│           │   ├── Configuraciones/   # CRUD: usuarios, roles, menús, empresa, SMTP
│           │   ├── Mantenimiento/     # CRUD: personas, empleados, reportes
│           │   ├── Matriculacion/     # Matrícula, cursos, notas, horarios
│           │   └── Reportes_especiales/
│           │
│           ├── Forms/                 # Formularios Django
│           │   ├── Configuracion/
│           │   └── Matriculacion/
│           │
│           ├── Filters/               # Filtros de autocompletado
│           ├── Serializers/           # Serializadores DRF
│           └── migrations/
│
├── templates/                         # Plantillas HTML
│   ├── base/                          # Layout base, login
│   ├── errores/                       # 404, 500
│   ├── sistemaAcademico/              # Vistas por módulo
│   └── Correos/                       # Plantillas de correo
│
├── static/                            # Archivos estáticos
├── media/                             # Archivos subidos por usuarios
├── sb_admin/                          # Tema SB Admin 2 (CSS, JS, vendor)
├── respaldo_bd/                       # Respaldos SQL de la base de datos
└── logs/                              # Logs de la aplicación
```

## Módulos Funcionales

| Módulo | Descripción |
|--------|-------------|
| Configuraciones | Gestión de empresa, usuarios, roles, menús, permisos, acciones y SMTP |
| Mantenimiento | CRUD de personas, estudiantes y empleados |
| Matriculación | Año lectivo, cursos, paralelos, asignación de materias, matrícula de estudiantes |
| Registro de Notas | Notas por quimestre, promedios, supletorios, remediales |
| Horarios | Asignación de horarios por curso y profesor |
| Reportes | Generación de reportes en PDF y Excel |
| API REST | Endpoints para validación de menús, unidades educativas y usuarios |

## Modelo de Datos

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│  GenrGeneral     │     │  MantPersona │     │  ConfEmpresa     │
│  (Catálogos)     │     │  (Personas)  │     │  (Inst. Educativa)│
└────────┬────────┘     └──────┬───────┘     └──────────────────┘
         │                     │
         │              ┌──────┴───────┐
         │              │              │
    ┌────┴─────┐  ┌─────┴────┐  ┌─────┴──────┐
    │ConfUsuario│  │MantEstud.│  │MantEmpleado│
    │(Usuarios) │  │(Alumnos) │  │(Docentes)  │
    └────┬─────┘  └─────┬────┘  └─────┬──────┘
         │              │              │
    ┌────┴─────┐  ┌─────┴──────────┐  │
    │ConfRol   │  │MovMatriculación│  │
    │ConfPermiso│  │  Estudiante   │  │
    └──────────┘  └─────┬──────────┘  │
                        │              │
              ┌─────────┴────────┐     │
              │Mov_Aniolectivo   │     │
              │  _curso          │     │
              └────────┬─────────┘     │
                       │               │
              ┌────────┴─────────┐     │
              │MovDetallMateria  │     │
              │    Curso         ├─────┘
              └────────┬─────────┘
                       │
              ┌────────┴─────────┐
              │Mov_Materia       │
              │  _profesor       │
              └────────┬─────────┘
                       │
              ┌────────┴─────────┐
              │MovDetalleRegistro│
              │     Notas        │
              └──────────────────┘
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd AmbienteDesarrolloPython
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv

# Windows (PowerShell)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copiar `.env.example` a `.env` y editar los valores:

```bash
cp .env.example .env
```

Variables requeridas:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de Django | `cambiar-esta-clave` |
| `DEBUG` | Modo debug | `False` |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost,127.0.0.1` |
| `DB_NAME` | Nombre de la base de datos | `bd_academico` |
| `DB_USER` | Usuario MySQL | `root` |
| `DB_PASSWORD` | Contraseña MySQL | `****` |
| `DB_HOST` | Host de MySQL | `localhost` |
| `DB_PORT` | Puerto de MySQL | `3306` |

### 4. Crear la base de datos

```sql
CREATE DATABASE bd_academico CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

O restaurar desde los respaldos en `respaldo_bd/`.

### 5. Ejecutar migraciones

```bash
python manage.py migrate
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

Acceder a `http://localhost:8000/`

## Seguridad

El proyecto implementa las siguientes medidas de seguridad:

- Credenciales externalizadas en `.env` (nunca en código fuente)
- Hashing de contraseñas con PBKDF2 (migración automática desde SHA1 legacy)
- Middleware de autenticación centralizado
- Debug toolbar solo habilitado en modo `DEBUG=True`
- `ALLOWED_HOSTS` restringido a dominios específicos
- `SESSION_COOKIE_HTTPONLY` y `SESSION_COOKIE_SECURE` habilitados
- Protección XSS, CSRF y Clickjacking activas
- APIs REST protegidas con `SessionAuthentication` + `IsAuthenticated`
- Sesiones con expiración de 1 hora (configurable)
- Logging de intentos de acceso fallidos

## API REST

Endpoints disponibles en `/api_menu/`, protegidos con autenticación de sesión:

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api_menu/` | POST | Validar existencia de menú |

## Generación de Reportes

El sistema genera reportes en dos formatos:

- PDF: usando ReportLab con encabezado, tabla de datos y pie de página
- Excel: usando OpenPyXL con estilos y formato de celdas

Disponibles desde los módulos de Configuraciones y Mantenimiento.

## Notas de Desarrollo

- El proyecto usa `PyMySQL` como driver MySQL (puro Python, sin compilación C)
- La inicialización de PyMySQL está en `sistemaAcademico/__init__.py`
- Los modelos están organizados en `Diccionario/` por prefijo: `conf_`, `genr_`, `mant_`, `mov_`
- Las validaciones de cédula y RUC ecuatoriano están en `Apps/Validaciones.py`
- El sistema de permisos es custom (no usa el de Django auth) basado en `ConfRol`, `ConfPermiso` y `ConfAccion`

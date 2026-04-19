# Mejoras Pendientes

## Completadas
- [x] Refactorizar controladores grandes (Estructura_view_usuarios.py 872 → 67 líneas)
- [x] Reemplazar print() por logging en todos los controladores (12 archivos)

## Prioridad alta

- [ ] Migrar SHA1 en Estructura_view_file.py y file_ex.py: ambos archivos aún usan `hashlib.new("sha1")` para crear contraseñas de UsuarioTemp al importar estudiantes desde Excel. Cambiar a `hash_password()` de utils.py
- [ ] Corregir wildcard imports (`from module import *`): views.py, urls.py y varios controladores usan `import *` lo que contamina el namespace y dificulta rastrear de dónde viene cada clase/función
- [ ] Eliminar las ~40 rutas duplicadas de timeout en urls.py: con el middleware de autenticación centralizado, las rutas tipo `path('modulo/timeout/', timeout)` son innecesarias
- [ ] Agregar paginación a los ListView: Usuarios, Estudiante, Empleado, Roles cargan todos los registros de golpe. Agregar `paginate_by = 20`

## Prioridad media

- [ ] Capa de servicios para lógica de negocio: la matriculación en `FilterEstudinatesestado.post()` tiene ~50 líneas de lógica (crear notas, verificar profesores) mezclada con la vista. Extraer a un servicio
- [ ] Cachear permisos en sesión: el context processor `acciones()` hace 2+ queries a la BD en cada request. Guardar en `request.session['permisos_cache']` después del login
- [ ] Corregir el handler500 en views.py: `Error500.as_error_view()` llama `r.render()` que falla con `HttpResponseNotAllowed`. Usar `django.views.defaults.server_error` o manejar el caso
- [ ] Agregar `select_related`/`prefetch_related` en las vistas que hacen N+1 queries: los reportes de roles iteran `confRol.id_rol.all()` por cada usuario sin prefetch
- [ ] Proteger las vistas de eliminación contra GET: `eliminar_usuario`, `eliminar_estudiante`, etc. aceptan GET y muestran confirmación, pero no validan CSRF en el formulario de confirmación

## Prioridad baja

- [ ] Reemplazar el iframe por templates Django con herencia normal: el sistema carga todo dentro de un iframe en base.html, lo que causa problemas de navegación y doble carga de CSS/JS
- [ ] Validación client-side en formularios: agregar validación JavaScript para mejorar UX antes de enviar al servidor
- [ ] Normalizar nombres de archivos y variables: mezcla de español/inglés y CamelCase/snake_case (ej: `Estructura_view_usuarios.py` vs `estructura_view_SMTP.py`, `MovMateriProfesorList` vs `filtro_estudiantes`)
- [ ] Agregar índices a la BD: campos frecuentemente filtrados como `id_genr_estado`, `estado`, `usuario` no tienen índices explícitos más allá de las FK
- [ ] Migrar los campos `usuario_ing` y `terminal_ing` a un mixin: estos campos se repiten en MantPersona, MantEstudiante, MantEmpleado, MovMatriculacionEstudiante, MovCabRegistroNotas, Mov_Horario_materia. Crear un `AuditMixin` abstracto
- [ ] Agregar API de consulta de estudiantes: actualmente solo hay endpoints para menú, unidad educativa y usuario. Falta un endpoint REST para consultar estudiantes y notas
- [ ] Documentar la API con Swagger/OpenAPI: los endpoints REST no tienen documentación
- [ ] Agregar rate limiting al login: no hay protección contra fuerza bruta. Implementar `django-axes` o similar
- [ ] Eliminar el import de `pickle` en urls.py de la app: `import pickle` está en la primera línea de GestionAcademica/urls.py pero nunca se usa

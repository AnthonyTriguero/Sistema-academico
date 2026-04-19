# Mejoras Pendientes

## Prioridad alta
- [x] Refactorizar controladores grandes (Estructura_view_usuarios.py 872 líneas) - separar reportes
- [x] Reemplazar print() restantes por logging en todos los controladores

## Prioridad media
- [ ] Capa de servicios para lógica de negocio (matriculación, notas)
- [ ] Eliminar rutas duplicadas de timeout (~40 rutas innecesarias con el middleware)
- [ ] Cachear permisos en sesión en lugar de consultar BD en cada request

## Prioridad baja
- [ ] Reemplazar iframe por templates Django con herencia normal
- [ ] Agregar paginación a listados (estudiantes, usuarios, etc.)
- [ ] Validación client-side en formularios

import logging
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfMenu, ConfAccion

logger = logging.getLogger(__name__)

CACHE_KEY = '_permisos_cache'


def _cargar_permisos_desde_bd(usuario_id):
    """Consulta permisos y acciones desde la BD y retorna un dict serializable."""
    resultado = {
        'permisos': [],
        'agregar': [],
        'editar': [],
        'eliminar': [],
        'imprimir': [],
    }

    resultado['permisos'] = list(ConfMenu.objects.filter(
        fk_permiso_modmenu__id_rol__fk_rol__id_usuario=usuario_id,
        id_genr_estado=97
    ).values('descripcion', 'id_menu', 'id_padre', 'url', 'icono', 'orden'))

    acciones_usuario = ConfAccion.objects.filter(
        id_rol_id__fk_permiso_rol__id_rol__fk_rol__id_usuario=usuario_id
    ).prefetch_related('id_menu')

    for accion in acciones_usuario:
        menus = list(accion.id_menu.all().values('id_menu', 'descripcion', 'url'))
        if accion.descripcion == 'Agregar':
            resultado['agregar'].extend(menus)
        elif accion.descripcion == 'Editar':
            resultado['editar'].extend(menus)
        elif accion.descripcion == 'Eliminar':
            resultado['eliminar'].extend(menus)
        elif accion.descripcion == 'Imprimir':
            resultado['imprimir'].extend(menus)

    return resultado


def cargar_permisos_en_sesion(request, usuario_id):
    """Precarga los permisos en la sesión después del login."""
    try:
        request.session[CACHE_KEY] = _cargar_permisos_desde_bd(usuario_id)
    except Exception as e:
        logger.error(f"Error al precargar permisos en sesión: {e}")


def invalidar_cache_permisos(request):
    """Invalida el caché de permisos (llamar al cambiar roles/permisos)."""
    request.session.pop(CACHE_KEY, None)


def acciones(request):
    """Context processor para permisos y acciones del usuario.
    Lee de la sesión si hay caché, si no consulta la BD y cachea."""
    vacio = {
        'permisos': [],
        'agregar': [],
        'editar': [],
        'eliminar': [],
        'imprimir': [],
    }

    try:
        usuario_id = request.session.get('usuario')
    except AttributeError:
        return vacio

    if not usuario_id:
        return vacio

    # Leer del caché en sesión
    cached = request.session.get(CACHE_KEY)
    if cached:
        return cached

    # Si no hay caché, consultar BD y guardar
    try:
        resultado = _cargar_permisos_desde_bd(usuario_id)
        request.session[CACHE_KEY] = resultado
        return resultado
    except Exception as e:
        logger.error(f"Error en context_processor acciones: {e}")
        return vacio

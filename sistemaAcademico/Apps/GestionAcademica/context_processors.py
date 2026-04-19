import logging
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfMenu, ConfAccion

logger = logging.getLogger(__name__)


def acciones(request):
    """Context processor para permisos y acciones del usuario."""
    resultado = {
        'permisos': [],
        'agregar': [],
        'editar': [],
        'eliminar': [],
        'imprimir': [],
    }

    try:
        usuario_id = request.session.get('usuario')
    except AttributeError:
        return resultado

    if not usuario_id:
        return resultado

    try:
        resultado['permisos'] = list(ConfMenu.objects.filter(
            fk_permiso_modmenu__id_rol__fk_rol__id_usuario=usuario_id,
            id_genr_estado=97
        ).values('descripcion', 'id_menu', 'id_padre', 'url', 'icono', 'orden'))

        acciones_usuario = ConfAccion.objects.filter(
            id_rol_id__fk_permiso_rol__id_rol__fk_rol__id_usuario=usuario_id
        ).prefetch_related('id_menu')

        for accion in acciones_usuario:
            if accion.descripcion == 'Agregar':
                resultado['agregar'].extend(accion.id_menu.all())
            elif accion.descripcion == 'Editar':
                resultado['editar'].extend(
                    accion.id_menu.all().values('id_menu', 'descripcion', 'url'))
            elif accion.descripcion == 'Eliminar':
                resultado['eliminar'].extend(
                    accion.id_menu.all().values('id_menu', 'descripcion', 'url'))
            elif accion.descripcion == 'Imprimir':
                resultado['imprimir'].extend(
                    accion.id_menu.all().values('id_menu', 'descripcion', 'url'))

    except Exception as e:
        logger.error(f"Error en context_processor acciones: {e}")

    return resultado

"""
Vistas para exportación de datos.
"""
import logging
from django.views import View
from django.http import HttpResponseRedirect
from django.db.models import Q

from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mant import MantPersona
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfUsuario
from sistemaAcademico.Apps.GestionAcademica.Services.export_service import ExportService

logger = logging.getLogger(__name__)


class ExportarEstudiantesView(View):
    """Vista para exportar estudiantes a Excel."""
    
    def get(self, request):
        """Exporta estudiantes según los filtros aplicados."""
        if 'usuario' not in request.session:
            return HttpResponseRedirect('/timeout/')
        
        # Obtener queryset base
        queryset = MantPersona.objects.filter(
            estado=97, 
            id_genr_tipo_usuario=19
        ).select_related('id_genr_tipo_usuario')
        
        # Aplicar filtros
        filtros = {}
        search = request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(nombres__icontains=search) |
                Q(apellidos__icontains=search) |
                Q(identificacion__icontains=search)
            )
            filtros['search'] = search
        
        # Ordenamiento
        order_by = request.GET.get('order_by', 'apellidos')
        direction = request.GET.get('direction', 'asc')
        
        valid_fields = ['nombres', 'apellidos', 'identificacion', 'id_persona']
        if order_by in valid_fields:
            if direction == 'desc':
                order_by = f'-{order_by}'
            queryset = queryset.order_by(order_by)
        
        # Exportar
        logger.info(f"Exportando {queryset.count()} estudiantes. Filtros: {filtros}")
        return ExportService.exportar_estudiantes(queryset, filtros)


class ExportarUsuariosView(View):
    """Vista para exportar usuarios a Excel."""
    
    def get(self, request):
        """Exporta usuarios según los filtros aplicados."""
        if 'usuario' not in request.session:
            return HttpResponseRedirect('/timeout/')
        
        # Obtener queryset base
        queryset = ConfUsuario.objects.filter(
            id_genr_estado=97
        ).select_related('id_persona', 'id_genr_tipo_usuario')
        
        # Aplicar filtros
        filtros = {}
        search = request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(usuario__icontains=search) |
                Q(id_persona__nombres__icontains=search) |
                Q(id_persona__apellidos__icontains=search)
            )
            filtros['search'] = search
        
        tipo_usuario = request.GET.get('tipo_usuario', '')
        if tipo_usuario:
            queryset = queryset.filter(id_genr_tipo_usuario=tipo_usuario)
            filtros['tipo_usuario'] = tipo_usuario
        
        # Ordenamiento
        order_by = request.GET.get('order_by', 'usuario')
        direction = request.GET.get('direction', 'asc')
        
        valid_fields = ['usuario', 'id_persona__nombres', 'id_persona__apellidos']
        if order_by in valid_fields:
            if direction == 'desc':
                order_by = f'-{order_by}'
            queryset = queryset.order_by(order_by)
        
        # Exportar
        logger.info(f"Exportando {queryset.count()} usuarios. Filtros: {filtros}")
        return ExportService.exportar_usuarios(queryset, filtros)


class ExportarEmpleadosView(View):
    """Vista para exportar empleados a Excel."""
    
    def get(self, request):
        """Exporta empleados según los filtros aplicados."""
        if 'usuario' not in request.session:
            return HttpResponseRedirect('/timeout/')
        
        # Obtener queryset base
        queryset = MantPersona.objects.filter(
            Q(estado=97),
            Q(id_genr_tipo_usuario=20) | Q(id_genr_tipo_usuario=21)
        ).select_related('id_genr_tipo_usuario')
        
        # Aplicar filtros si los hay
        filtros = {}
        search = request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(nombres__icontains=search) |
                Q(apellidos__icontains=search) |
                Q(identificacion__icontains=search)
            )
            filtros['search'] = search
        
        # Exportar
        logger.info(f"Exportando {queryset.count()} empleados. Filtros: {filtros}")
        return ExportService.exportar_empleados(queryset, filtros)

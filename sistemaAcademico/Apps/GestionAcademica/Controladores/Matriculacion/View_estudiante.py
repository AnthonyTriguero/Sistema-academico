import logging
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q

from sistemaAcademico.Apps.GestionAcademica.Forms.Matriculacion.forms_estudiantes_filter import (
    FilterEstudinatesestadoforms, FilterTipoEstudinatesforms,
)
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mov import (
    MovMatriculacionEstudiante,
)
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mant import MantEstudiante, MantPersona
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfUsuario
from sistemaAcademico.Apps.GestionAcademica.Services.matriculacion_service import MatriculacionService

logger = logging.getLogger(__name__)


def _get_matriculaciones_queryset():
    """Query base para matriculaciones usando ORM en lugar de raw SQL."""
    return MovMatriculacionEstudiante.objects.select_related(
        'id_estudiante__id_persona',
        'id_mov_anioelectivo_curso__id_curso',
        'id_mov_anioelectivo_curso__id_genr_paralelo',
        'id_mov_anioelectivo_curso__id_anio_electivo',
        'estado',
    )


def filtro_estudiantes_lista(request):
    cox = {}
    if request.GET:
        nombres = request.GET.get('nombres', '')
        apellidos = request.GET.get('apellidos', '')
        curso = request.GET.get('curso', '')
        paralelo = request.GET.get('paralelo', '')
        anio = request.GET.get('anio', '')

        query = _get_matriculaciones_queryset().filter(
            Q(id_estudiante__id_persona__nombres__icontains=nombres) |
            Q(id_estudiante__id_persona__apellidos__icontains=apellidos) |
            Q(id_mov_anioelectivo_curso__id_curso__nombre__icontains=curso) |
            Q(id_mov_anioelectivo_curso__id_genr_paralelo__nombre__icontains=paralelo) |
            Q(id_mov_anioelectivo_curso__id_anio_electivo__anio__icontains=anio)
        )
        cox['consultas'] = query

    return render(request, 'sistemaAcademico/Matriculacion/Estudiantes_filtros/Filtrar.html', cox)


def filtro_estudiantes(request):
    query = _get_matriculaciones_queryset()
    cox = {'consultas': query}
    return render(request, 'sistemaAcademico/Matriculacion/Estudiantes_filtros/Filtrar.html', cox)


class FilterEstudinatesestado(UpdateView):
    model = MovMatriculacionEstudiante
    form_class = FilterEstudinatesestadoforms
    context_object_name = 'id'
    template_name = 'sistemaAcademico/Matriculacion/Estudiantes_filtros/Actualizar_estado.html'
    success_url = reverse_lazy('Academico:estudiante_filtro')

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        self.object = self.get_object()
        form = self.form_class(request.POST)
        
        # Obtener usuario y estado del formulario
        usuario = ConfUsuario.objects.get(id_usuario=request.session.get('usuario'))
        id_estado_form = request.POST['estado']
        estado = GenrGeneral.objects.get(idgenr_general=id_estado_form)
        
        # Obtener la matriculación
        id_matricula = kwargs['pk']
        matricula = MovMatriculacionEstudiante.objects.get(
            id_matriculacion_estudiante=id_matricula
        )
        
        # Si el estado es MATRICULADO, usar el servicio de matriculación
        if estado.nombre == 'MATRICULADO':
            exito, errores = MatriculacionService.matricular_estudiante(
                matricula=matricula,
                usuario=usuario
            )
            
            if not exito:
                # Mostrar errores al usuario
                for error in errores:
                    messages.error(request, error)
                logger.warning(f"Matriculación fallida para estudiante {matricula.id_estudiante}: {errores}")
                return HttpResponseRedirect(self.success_url)
            
            # Matriculación exitosa, continuar con el guardado del estado
            logger.info(f"Estudiante {matricula.id_estudiante} matriculado exitosamente")
        
        # Guardar el cambio de estado
        return super().post(request, **kwargs)


class FilterTipoEstudinates(UpdateView):
    model = MantEstudiante
    form_class = FilterTipoEstudinatesforms
    context_object_name = 'id'
    template_name = 'sistemaAcademico/Matriculacion/Estudiantes_filtros/Actualizar_tipoEstudiantes.html'
    success_url = reverse_lazy('Academico:estudiante_filtro')

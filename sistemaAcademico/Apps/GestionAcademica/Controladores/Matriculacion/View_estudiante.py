import logging
import socket
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q

from sistemaAcademico.Apps.GestionAcademica.Forms.Matriculacion.forms_estudiantes_filter import (
    FilterEstudinatesestadoforms, FilterTipoEstudinatesforms,
)
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mov import (
    MovMatriculacionEstudiante, Mov_Aniolectivo_curso, MovDetalleMateriaCurso,
    Mov_Materia_profesor, MovDetalleRegistroNotas, MovCabRegistroNotas,
)
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mant import MantEstudiante, MantPersona
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfUsuario

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
        usuario = ConfUsuario.objects.get(id_usuario=request.session.get('usuario'))
        quimestres = GenrGeneral.objects.filter(tipo='QUI')
        listaErrores = []
        val = False

        id_estado_form = request.POST['estado']
        estado = GenrGeneral.objects.get(idgenr_general=id_estado_form)

        if estado:
            if estado.nombre == 'MATRICULADO':
                id_matricula = kwargs['pk']
                matricula = MovMatriculacionEstudiante.objects.get(
                    id_matriculacion_estudiante=id_matricula)

                if matricula.estado.nombre != 'MATRICULADO':
                    id_aniolectivo_curso = matricula.id_mov_anioelectivo_curso.id_mov_anioelectivo_curso
                    curso = Mov_Aniolectivo_curso.objects.get(
                        id_mov_anioelectivo_curso=id_aniolectivo_curso)
                    materia_curso = MovDetalleMateriaCurso.objects.filter(
                        id_mov_anio_lectivo_curso=curso.id_mov_anioelectivo_curso)

                    for i in materia_curso:
                        try:
                            materia = Mov_Materia_profesor.objects.get(
                                id_detalle_materia_curso=i.id_detalle_materia_curso)
                            if materia:
                                for qui in quimestres:
                                    anio_lectivo = Mov_Aniolectivo_curso.objects.get(
                                        id_mov_anioelectivo_curso=i.id_mov_anio_lectivo_curso.id_mov_anioelectivo_curso)
                                    detaRegistroNotas = MovDetalleRegistroNotas(
                                        id_matriculacion_estudiante=matricula,
                                        id_materia_profesor=materia,
                                        id_general_quimestre=qui,
                                    )
                                    detaRegistroNotas.save()
                                    cabRegistro = MovCabRegistroNotas(
                                        id_detalle_registro_notas=detaRegistroNotas,
                                        id_mov_anioelectivo_curso=anio_lectivo,
                                        promedio_curso_1q=0,
                                        promedio_curso_2q=0,
                                        promedio_curso_general=0,
                                        fecha_ingreso=timezone.now(),
                                        usuario_ing=usuario.usuario,
                                        terminal_ing=socket.gethostname(),
                                    )
                                    cabRegistro.save()
                            val = True
                        except Exception as e:
                            logger.error(f"Error al matricular: {e}")
                            val = False
                            listaErrores.append(f'{i} no tiene un profesor asignado')
            else:
                val = True

        if val:
            return super().post(request, **kwargs)
        else:
            return HttpResponseRedirect(self.success_url)


class FilterTipoEstudinates(UpdateView):
    model = MantEstudiante
    form_class = FilterTipoEstudinatesforms
    context_object_name = 'id'
    template_name = 'sistemaAcademico/Matriculacion/Estudiantes_filtros/Actualizar_tipoEstudiantes.html'
    success_url = reverse_lazy('Academico:estudiante_filtro')

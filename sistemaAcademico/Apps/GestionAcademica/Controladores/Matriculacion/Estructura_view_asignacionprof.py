import logging

from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mov import Mov_Materia_profesor
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.cache import cache_page

logger = logging.getLogger(__name__)


class List_docente(ListView):
    model = Mov_Materia_profesor
    template_name = 'sistemaAcademico/reportes/AsignacionProfesores.html'
    context_object_name = 'lista_profesor'

    def get_queryset(self):
        # Optimización: select_related para evitar N+1 queries
        return self.model.objects.filter(
            id_empleado__id_persona__estado=97
        ).select_related(
            'id_empleado',
            'id_empleado__id_persona'
        )

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['lista_profesor'] = self.get_queryset()
        return contexto

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            return render(request, self.template_name, self.get_context_data())
        else:
            return HttpResponseRedirect('timeout/')


class List_docente_asignado(ListView):
    model = Mov_Materia_profesor
    template_name = 'sistemaAcademico/reportes/ProfesoresAsignados.html'

    def get_context_data(self, *args, **kwargs):
            context = super(List_docente_asignado, self).get_context_data(**kwargs)
            lista = []

            # Optimización: select_related y prefetch_related para evitar N+1 queries
            queryset = self.model.objects.filter(
                id_empleado__id_persona__estado=97
            ).select_related(
                'id_empleado',
                'id_empleado__id_persona'
            ).prefetch_related(
                'id_detalle_materia_curso',
                'id_detalle_materia_curso__id_genr_materias',
                'id_detalle_materia_curso__id_mov_anio_lectivo_curso'
            )
            count = 1
            for materia in queryset:
                logger.debug("materia: %s", materia)
                roles = materia.id_detalle_materia_curso.all()
                for role in roles:
                    lista.append(
                        (count, materia.id_empleado, role.id_genr_materias.nombre, role.id_mov_anio_lectivo_curso, materia))
                count += 1
            context['lista_profesor'] = lista
            return context
        


class List_docente_sin_asignar(ListView):
    model = Mov_Materia_profesor
    template_name = 'sistemaAcademico/reportes/ProfesorSinAsignar.html'

    def get_queryset(self):
        # Optimización: usar annotate para filtrar en BD en vez de Python
        from django.db.models import Count
        return Mov_Materia_profesor.objects.filter(
            id_empleado__id_persona__estado=97
        ).select_related(
            'id_empleado',
            'id_empleado__id_persona'
        ).prefetch_related(
            'id_detalle_materia_curso'
        ).annotate(
            num_materias=Count('id_detalle_materia_curso')
        ).filter(num_materias=0)

    def get(self, request):
        if 'usuario' in request.session:
            # Ahora la query ya está optimizada y filtrada en BD
            profesores = self.get_queryset()
            logger.debug("profesores sin asignar: %s", list(profesores))
            context = {'lista_profesor_sin_asignar': profesores}
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect('timeout/')

def eliminar_profesor(request, id):
    if 'usuario' in request.session:
        profesor = Mov_Materia_profesor.objects.get(id_materia_profesor=id)
        inactivo = GenrGeneral.objects.get(idgenr_general=98)
        if request.method == 'POST':
            profesor.id_empleado.id_persona.estado = inactivo
            profesor.id_empleado.id_persona.save()
            logger.debug("estado profesor: %s", profesor.id_empleado.id_persona.estado)

            return redirect('Academico:asignacion_materiasprof')
        return render(request, 'sistemaAcademico/Matriculacion/Asignacion_Mprofesor/eliminarProfesor.html', {'asignacion_materiasprof': profesor})
    else:
        return HttpResponseRedirect('timeout/')

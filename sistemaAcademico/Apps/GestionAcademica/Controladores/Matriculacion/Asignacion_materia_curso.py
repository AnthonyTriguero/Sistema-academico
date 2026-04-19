import logging

from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from sistemaAcademico.Apps.GestionAcademica.Forms.Matriculacion.forms_mov_materia_curso import Mov_Materia_Curso_forms
from django.shortcuts import render, redirect
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mov import MovDetalleMateriaCurso
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

logger = logging.getLogger(__name__)


class Crear_materia_curso(CreateView):
    model = MovDetalleMateriaCurso
    form_class = Mov_Materia_Curso_forms
    template_name = 'sistemaAcademico/Matriculacion/Asignacion_Materia_Curso/crear.html'
    success_url = reverse_lazy('Academico:asignacion_materia_curso')

    def post(self,  request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.save()
            materia = data.id_genr_materias
            anio = data.id_mov_anio_lectivo_curso
            query =MovDetalleMateriaCurso.objects.filter(id_genr_materias=materia,id_mov_anio_lectivo_curso=anio,estado=97).count()

            if query >1:
                logger.debug("query duplicada: %s", query)
                data.delete()
                messages.error(request, 'Esta materia ya se encuentra asignada')
                return self.render_to_response(self.get_context_data(form=form))

            else:
                return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


        

    
class Editar_materia_curso(UpdateView):
    model = MovDetalleMateriaCurso
    form_class = Mov_Materia_Curso_forms
    context_object_name = 'mat'
    template_name = 'sistemaAcademico/Matriculacion/Asignacion_Materia_Curso/edit.html'
    success_url = reverse_lazy('Academico:asignacion_materia_curso')



    def post(self,  request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.save()
            materia = data.id_genr_materias
            anio = data.id_mov_anio_lectivo_curso
            query =MovDetalleMateriaCurso.objects.filter(id_genr_materias=materia,id_mov_anio_lectivo_curso=anio,estado=97).count()

            if query >1:
                logger.debug("query duplicada: %s", query)
                data.delete()
                messages.error(request, 'Esta materia ya se encuentra asignada')
                return self.render_to_response(self.get_context_data(form=form))

            else:
                return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    
class Listar_materia_curso(ListView):
    model = MovDetalleMateriaCurso
    context_object_name = 'mat'
    template_name = 'sistemaAcademico/Matriculacion/Asignacion_Materia_Curso/listar.html'

    def get_queryset(self):
        return self.model.objects.filter(estado=97)

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['mat'] = self.get_queryset()
        return contexto

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            return render(request, self.template_name, self.get_context_data())
        else:
            return HttpResponseRedirect('timeout/')


    
def eliminar_materia_curso(request, id):
    if 'usuario' in request.session:
        dic={}
        mat = MovDetalleMateriaCurso.objects.get(id_detalle_materia_curso=id)
        materia = MovDetalleMateriaCurso.objects.filter(id_detalle_materia_curso=id)
        inactivo = GenrGeneral.objects.get(idgenr_general=98)
        dic['mat']=mat
        dic['materia']=materia
        if request.method == 'POST':
            mat.estado = inactivo
            mat.save()
            return redirect('Academico:asignacion_materia_curso')
        return render(request, 'sistemaAcademico/Matriculacion/Asignacion_Materia_Curso/eliminar.html', dic)
    else:
        return HttpResponseRedirect('timeout/')
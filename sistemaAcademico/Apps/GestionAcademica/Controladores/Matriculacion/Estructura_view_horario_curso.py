import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView

from django.utils import timezone
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfUsuario
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mant import MantAnioLectivo
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mov import (
    Mov_Horario_materia, Mov_Aniolectivo_curso, MovDetalleMateriaCurso, Mov_Materia_profesor,
)
import socket
from django.utils import timezone
from sistemaAcademico.Apps.GestionAcademica.Forms.Matriculacion.forms_mov_horario_curso import HorarioCursoForm

logger = logging.getLogger(__name__)


class HorarioCurso (ListView):
    model= Mov_Horario_materia
    template_name = 'sistemaAcademico/Matriculacion/Horario_curso/horario_curso.html'
    context_object_name = 'horario'








    def get_context_data(self, **kwargs):
        context = super(HorarioCurso, self).get_context_data(**kwargs)
        context['jor'] = GenrGeneral.objects.filter(tipo='JOR')
        context['tre'] = GenrGeneral.objects.filter(tipo='TRE')
        context['mod'] = GenrGeneral.objects.filter(tipo='MOD')
        context['ted'] = GenrGeneral.objects.filter(tipo='TED')
        context['niv'] = GenrGeneral.objects.filter(tipo='NIV')
        context['tic'] = Mov_Aniolectivo_curso.objects.all()
        context['lec'] = MantAnioLectivo.objects.all()

        return context



    def post(self, request, *args, **kwargs):

        id_anio_lectivo_curso_paralelo = request.POST['curso']
        a =MovDetalleMateriaCurso.objects.filter(id_mov_anio_lectivo_curso=id_anio_lectivo_curso_paralelo).values()

        context={}
        count=1
        for i in a:
            id_materia_curso= i['id_detalle_materia_curso']
            materia_profesor = Mov_Materia_profesor.objects.filter(id_detalle_materia_curso=id_materia_curso).values()
            for e in materia_profesor:
                
                id_materia_profesor= e['id_materia_profesor']
                b = Mov_Horario_materia.objects.filter(id_materia_profesor=id_materia_profesor)
                context[str(count)]= b
            
                count=+1

        context['bool']=True

        logger.debug("context: %s", context)

        return render(request, self.template_name, context)


class ListViewHorario(ListView):
    model= Mov_Horario_materia
    template_name = 'sistemaAcademico/Matriculacion/Horario_curso/list_horario.html'
    context_object_name = 'h'

    
    def get_queryset(self):
        return self.model.objects.filter(estado=97)

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['h'] = self.get_queryset()
        return contexto

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            return render(request, self.template_name, self.get_context_data())
        else:
            return HttpResponseRedirect('timeout/')

class CrearHorarioCurso(CreateView):
    model = Mov_Horario_materia
    form_class = HorarioCursoForm
    template_name = 'sistemaAcademico/Matriculacion/Horario_curso/crear_HorarioCurso.html'
    success_url = reverse_lazy('Academico:lista_horario')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            horariocurso = form.save()
            usuario = ConfUsuario.objects.get(id_usuario=request.session.get('usuario'))
            horariocurso.fecha_ingreso = timezone.now()
            horariocurso.usuario_ing = usuario.usuario
            horariocurso.terminal_ing = socket.gethostname()
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class UpdateHorario(UpdateView):
    model = Mov_Horario_materia
    form_class = HorarioCursoForm
    template_name = 'sistemaAcademico/Matriculacion/Horario_curso/update_horario.html'
    success_url = reverse_lazy('Academico:lista_horario')
    context_object_name = 'h'

class DeleteHorario(DeleteView):
    model = Mov_Horario_materia
    template_name = 'sistemaAcademico/Matriculacion/Horario_curso/delete_horario.html'
    success_url = reverse_lazy('Academico:lista_horario')
    context_object_name = 'h'

def deleteHorario(request, id):
    if 'usuario' in request.session:
        horarios = Mov_Horario_materia.objects.get(id_horario=id)
        inactivo = GenrGeneral.objects.get(idgenr_general=98)
        if request.method == 'POST':
            horarios.estado = inactivo
            horarios.save()
            return redirect('Academico:lista_horario')
        return render(request, 'sistemaAcademico/Matriculacion/Horario_curso/delete_horario.html', {'horario': horarios})
    else:
        return self.render_to_response(self.get_context_data(form=form))
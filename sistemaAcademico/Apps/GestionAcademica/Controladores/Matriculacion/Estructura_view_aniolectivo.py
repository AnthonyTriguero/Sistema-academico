from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mant import MantAnioLectivo
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from sistemaAcademico.Apps.GestionAcademica.Forms.Matriculacion.forms_matriculacion import Aniolectivo, UpAniolectivo
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse


class List_AnioLectivo (ListView):
    model = MantAnioLectivo
    template_name = 'sistemaAcademico/Matriculacion/Aniolectivo/Aniolectivo.html'
    context_object_name = 'anio_lectivo'

    def get_queryset(self):
        return self.model.objects.filter(Q(id_genr_estado=97) | Q(id_genr_estado=99) |Q(id_genr_estado=1784))

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['object_list'] = self.get_queryset()
        return contexto

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            return render(request, self.template_name, self.get_context_data())
        else:
            return HttpResponseRedirect('timeout/')

class UpdateAniolectivo (UpdateView):
    model = MantAnioLectivo
    template_name = 'sistemaAcademico/Matriculacion/Aniolectivo/Update_Aniolectivo.html'
    form_class = UpAniolectivo
    success_url = reverse_lazy('Academico:anio_lectivo')
    context_object_name = 'a'

class CreateAniolectivo (CreateView):
    model = MantAnioLectivo
    template_name = 'sistemaAcademico/Matriculacion/Aniolectivo/Create_Aniolectivo.html'
    form_class = Aniolectivo
    success_url = reverse_lazy('Academico:anio_lectivo')

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['form'] = self.form_class()
        return contexto

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            return render(request,self.template_name,self.get_context_data())
        else:
            return HttpResponseRedirect('timeout/')



def eliminar_Aniolectivo(request, id):
    if 'usuario' in request.session:
        anio = MantAnioLectivo.objects.get(id_anio_lectivo=id)
        inactivo = GenrGeneral.objects.get(idgenr_general=98)
        if request.method == 'POST':
            anio.id_genr_estado = inactivo
            anio.save()
            return redirect('Academico:anio_lectivo')
        return render(request, 'sistemaAcademico/Matriculacion/Aniolectivo/DeleteAniolectivo.html', {'anio': anio})
    else:
        return HttpResponseRedirect('timeout/')

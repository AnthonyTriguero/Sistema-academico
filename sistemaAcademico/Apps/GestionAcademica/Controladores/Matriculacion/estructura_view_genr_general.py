from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.urls import reverse_lazy
from sistemaAcademico.Apps.GestionAcademica.Forms.Matriculacion.froms_general import GenrGeneral_1
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
class General(ListView):
    model = GenrGeneral
    template_name = 'sistemaAcademico/Matriculacion/General/Listar_general.html'


    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['general'] = self.get_queryset()
        return contexto

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            return render(request, self.template_name, self.get_context_data())
        else:
            return HttpResponseRedirect('timeout/')



class CreateGeneral (CreateView):
    model = GenrGeneral
    template_name = 'sistemaAcademico/Matriculacion/General/Agregar_general.html'
    form_class = GenrGeneral_1
    context_object_name = 'F'
    success_url = reverse_lazy('Academico:general')

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['form'] = self.form_class()
        return contexto

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            return render(request,self.template_name,self.get_context_data())
        else:
            return HttpResponseRedirect('timeout/')

    


class UpdateGeneral (UpdateView):
    model = GenrGeneral
    template_name = 'sistemaAcademico/Matriculacion/General/Editar_general.html'
    form_class = GenrGeneral_1
    success_url = reverse_lazy('Academico:general')
    context_object_name = 'F'

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return render(request, self.template_name,context )
        else:
            return HttpResponseRedirect('/timeout/')
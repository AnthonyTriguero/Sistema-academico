from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect
from django.utils import timezone
from django.urls import reverse_lazy
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfPermiso
from django.views.generic import ListView, CreateView, UpdateView
import socket
from sistemaAcademico.Apps.GestionAcademica.Forms.Configuracion.forms_configuraciones import Permisosform


class ListPermisos(ListView):
    model = ConfPermiso
    template_name = 'sistemaAcademico/Configuraciones/Permisos/permisos.html'
    context_object_name = 'p'
    def get_queryset(self):
        return self.model.objects.all().select_related('id_rol')

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['p'] = self.get_queryset()
        return contexto

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            return render(request, self.template_name, self.get_context_data())
        else:
            return HttpResponseRedirect('timeout/')

class CreatePermiso(CreateView):
    model = ConfPermiso
    form_class = Permisosform
    template_name = "sistemaAcademico/Configuraciones/Permisos/add_permisos.html"
    success_url = reverse_lazy("Academico:permisos")

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['form'] = self.form_class()
        return contexto

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            return render(request,self.template_name,self.get_context_data())
        else:
            return HttpResponseRedirect('timeout/')


class UpdatePermisos(UpdateView):
    model = ConfPermiso
    form_class = Permisosform
    context_object_name = 'p'
    template_name = "sistemaAcademico/Configuraciones/Permisos/asignar_permisos.html"
    success_url = reverse_lazy('Academico:permisos')

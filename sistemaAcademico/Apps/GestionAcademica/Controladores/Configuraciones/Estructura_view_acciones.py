from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView,View

from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfAccion
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
import socket
from django.views.decorators.cache import cache_page

from sistemaAcademico.Apps.GestionAcademica.Forms.Configuracion.forms_configuraciones import AccionesForm


class Add_Accion(CreateView):
    model = ConfAccion
    template_name = 'sistemaAcademico/Configuraciones/Acciones/add_acciones.html'
    form_class = AccionesForm
    success_url = reverse_lazy('Academico:acciones')

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['form'] = self.form_class()
        return contexto

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            return render(request,self.template_name,self.get_context_data())
        else:
            return HttpResponseRedirect('timeout/')


class Acciones(View):
    model = ConfAccion
    template_name = 'sistemaAcademico/Configuraciones/Acciones/acciones.html'

    def get_queryset(self):
        return self.model.objects.all().select_related('id_rol')

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['a'] = self.get_queryset()
        return contexto

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            return render(request, self.template_name, self.get_context_data())
        else:
            return HttpResponseRedirect('timeout/')


def eliminar_accion(request, id):
    try:
        a = ConfAccion.objects.get(id_accion=id)
        if request.method == 'POST':
            a.id_genr_estado = GenrGeneral.objects.get(idgenr_general=98)
            a.save()
            return redirect('Academico:acciones')
        return render(request, 'sistemaAcademico/Configuraciones/Acciones/delete_acciones.html', {'a': a})
    except Exception as e:
        raise e


class Nueva_Accion(CreateView):
    model = ConfAccion
    form_class = AccionesForm
    template_name = 'sistemaAcademico/Configuraciones/Acciones/add_acciones.html'
    success_url = reverse_lazy('Academico:acciones')
    
    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['form'] = self.form_class()
        return contexto

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            return render(request,self.template_name,self.get_context_data())
        else:
            return HttpResponseRedirect('timeout/')

class Edit_acciones(UpdateView):
    model = ConfAccion
    template_name = 'sistemaAcademico/Configuraciones/Acciones/add_acciones.html'
    success_url = reverse_lazy('Academico:acciones')
    form_class = AccionesForm
    context_object_name = 'm'

# Este codigo funciona para el timeout de pantallas update, delete con tengan un modal    
"""    
    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return render(request, self.template_name,context )
        else:
            return HttpResponseRedirect('timeout/')
"""
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfMenu, ConfModulo
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
import socket
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from dal import autocomplete
from sistemaAcademico.Apps.GestionAcademica.Forms.Configuracion.forms_configuraciones import modulo_form,menu_form


class Menu(ListView):
    model = ConfMenu
    template_name = 'sistemaAcademico/Configuraciones/Menus/menu.html'
    queryset = ConfMenu.objects.filter(id_genr_estado=97)
    context_object_name = 'menu'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['menu'] = self.get_queryset()
        return contexto

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            return render(request, self.template_name, self.get_context_data())
        else:
            return HttpResponseRedirect('timeout/')

    
#--------------------------------

class UpdateMenu(UpdateView):
    model = ConfMenu
    template_name = 'sistemaAcademico/Configuraciones/Menus/edit_menu.html'
    form_class = menu_form
    success_url = reverse_lazy('Academico:menu')
    context_object_name = 'm'


#--------------------------------

def eliminar_menu(request,id):
    if 'usuario' in request.session:
        menu = ConfMenu.objects.get(id_menu = id)
        inactivo = GenrGeneral.objects.get(idgenr_general=98)
        if request.method == 'POST':
            menu.id_genr_estado = inactivo
            menu.save()
            return redirect('Academico:menu')
        return render(request,'sistemaAcademico/Configuraciones/Menus/eliminar_menu.html',{'menu':menu})
    else:
        return HttpResponseRedirect('timeout/')
        
class CreateMenu(CreateView):
    model = ConfMenu
    form_class = menu_form
    template_name = 'sistemaAcademico/Configuraciones/Menus/agregar_menu.html'
    success_url= reverse_lazy('Academico:menu')

    def get_context_data(self, **kwargs):
        context=super(CreateMenu,self).get_context_data(**kwargs)
        pk=self.kwargs.get('id_menu',0)
        context['id_menu'] = pk
        return context


    def post(self,request,*args,**kargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
           var_orden = 0
           c = form.save()
           lista_orden= self.model.objects.filter(id_padre=c.id_padre).order_by('-orden')[:1]
           for registro in lista_orden:
               b = int(registro.orden)
               var_orden = b+1
           c.orden = var_orden
           c.save()
           menu = ConfMenu.objects.get(descripcion=c.descripcion)
           menu_padre = ConfMenu.objects.get(id_menu=c.id_padre)    
           return redirect(self.get_success_url())
            
        else:
           return self.render_to_response(self.get_context_data(form=form))











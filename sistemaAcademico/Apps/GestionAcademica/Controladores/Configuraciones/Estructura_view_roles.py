from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfRol
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from django.views.decorators.cache import cache_page


class Roles(ListView):
    model = ConfRol
    template_name = 'sistemaAcademico/Configuraciones/Roles/rol.html'
    context_object_name = 'roles'
    
    def get_queryset(self):
        return self.model.objects.filter(id_genr_estado=97).values('id_rol','codigo','nombre')

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['roles'] = self.get_queryset()
        return contexto

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            return render(request, self.template_name, self.get_context_data())
        else:
            return HttpResponseRedirect('timeout/')

def roles(request):
    if 'usuario' in request.session:
        roles = ConfRol.objects.filter(id_genr_estado=97).values('id_rol','codigo','nombre')
        return render(request, 'sistemaAcademico/Configuraciones/Roles/rol.html',{"roles":roles})
    else:
        return HttpResponseRedirect('timeout/')


def nuevo_rol(request):
    if 'usuario' in request.session:
        if request.method == 'POST':
            codigo = request.POST.get('codigo')
            nombre = request.POST.get('nombre')
            ConfRol.objects.create(codigo=codigo, nombre=nombre)
            return redirect('Academico:roles')
        return render(request, 'sistemaAcademico/Configuraciones/Roles/add_rol.html')
    else:
        return HttpResponseRedirect('timeout/')


def editar_rol(request, id):
    if 'usuario' in request.session:
        contexto = {}
        roles = ConfRol.objects.get(id_rol=id)
        contexto['roles'] = roles
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            codigo = request.POST.get('codigo')
            rol= ConfRol(id_rol=id, codigo=codigo, nombre=nombre)
            rol.save()
            return redirect('Academico:roles')
        return render(request, 'sistemaAcademico/Configuraciones/Roles/add_rol.html', contexto)
    else:
        return HttpResponseRedirect('timeout/')


def eliminar_rol(request, id):
    if 'usuario' in request.session:
        roles = ConfRol.objects.get(id_rol=id)
        inactivo = GenrGeneral.objects.get(idgenr_general=98)
        if request.method == 'POST':
            roles.id_genr_estado = inactivo
            roles.save()
            return redirect('Academico:roles')
        return render(request, 'sistemaAcademico/Configuraciones/Roles/eliminar_rol.html', {'roles': roles})
    else:
        return HttpResponseRedirect('timeout/')

import socket
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
import os
from django.views.decorators.cache import cache_page
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfUsuario, ConfRol
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from sistemaAcademico.Apps.GestionAcademica import forms
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from sistemaAcademico.Apps.GestionAcademica.Forms.Configuracion.forms_configuraciones import UsuarioModelForm,UsuarioeditModelForm
from django.urls import reverse


class Usuarios(ListView):
    model = ConfUsuario
    template_name = 'sistemaAcademico/Configuraciones/Usuarios/usuario.html'
    context_object_name = 'lista_usuarios'
    paginate_by = 20

    def get_queryset(self):
        queryset = ConfUsuario.objects.filter(id_genr_estado=97).select_related(
            'id_persona', 'id_genr_tipo_usuario')
        
        # Búsqueda
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(usuario__icontains=search) |
                Q(id_persona__nombres__icontains=search) |
                Q(id_persona__apellidos__icontains=search)
            )
        
        # Filtro por tipo de usuario
        tipo_usuario = self.request.GET.get('tipo_usuario', '')
        if tipo_usuario:
            queryset = queryset.filter(id_genr_tipo_usuario=tipo_usuario)
        
        # Ordenamiento
        order_by = self.request.GET.get('order_by', 'usuario')
        direction = self.request.GET.get('direction', 'asc')
        
        valid_fields = ['usuario', 'id_persona__nombres', 'id_persona__apellidos']
        if order_by in valid_fields:
            if direction == 'desc':
                order_by = f'-{order_by}'
            queryset = queryset.order_by(order_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['order_by'] = self.request.GET.get('order_by', 'usuario')
        context['direction'] = self.request.GET.get('direction', 'asc')
        context['tipo_usuario'] = self.request.GET.get('tipo_usuario', '')
        context['tipos_usuario'] = GenrGeneral.objects.filter(tipo='TUS')
        context['total_usuarios'] = ConfUsuario.objects.filter(id_genr_estado=97).count()
        return context


class CreateUsuario(CreateView):
    model=ConfUsuario
    form_class = UsuarioModelForm
    context_object_name = 'm'
    template_name = 'sistemaAcademico/Configuraciones/Usuarios/crear-usuario.html'
    success_url = reverse_lazy('Academico:usuarios')

    def get_context_data(self, **kwargs):
        context = super(CreateUsuario, self).get_context_data(**kwargs)
        context['rol'] = ConfRol.objects.all()
        return context

    def post(self, request, *args, **kargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            usuario = form.save()
            # Usar hashing seguro PBKDF2 en lugar de SHA1
            from sistemaAcademico.Apps.GestionAcademica.utils import hash_password
            usuario.clave = hash_password(usuario.clave)
            usuario.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class UpdateUsuario(UpdateView):
    model = ConfUsuario
    form_class = UsuarioeditModelForm
    context_object_name = 'n'
    template_name = 'sistemaAcademico/Configuraciones/Usuarios/editar-usuario.html'
    success_url = reverse_lazy('Academico:usuarios')


def eliminar_usuario(request, id):
    # Protección: requiere autenticación
    if 'usuario' not in request.session:
        return HttpResponseRedirect('/timeout/')
    
    usuarios = ConfUsuario.objects.get(id_usuario=id)
    inactivo = GenrGeneral.objects.get(idgenr_general=98)
    
    if request.method == 'POST':
        # Solo POST puede eliminar
        usuarios.id_genr_estado = inactivo
        usuarios.save()
        logger.info(f"Usuario {usuarios.usuario} eliminado por {request.session.get('usuario')}")
        return redirect('Academico:usuarios')
    
    # GET muestra confirmación (cargado en modal)
    return render(request, 'sistemaAcademico/Configuraciones/Usuarios/eliminar.html', {'usuario': usuarios})

import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .Controladores.Configuraciones.Estructura_view_empresa import *
from .Controladores.Configuraciones.Estructura_view_usuarios import *
from .Controladores.Configuraciones.Estructura_view_reportes_conf import *
from .Controladores.Configuraciones.Estructura_view_menu import *
from .Controladores.Configuraciones.Estructura_view_acciones import *
from .Controladores.Configuraciones.Estructura_view_modulo import *
from .Controladores.Configuraciones.Estructura_view_permisos import *
from .Controladores.Configuraciones.Estructura_view_roles import *
from .Controladores.Mantenimiento.Estructura_view_reportes import *
from .Controladores.Mantenimiento.Estructura_view_consultas import *
from .Controladores.Mantenimiento.Estructura_view_mantenimientos import *
from .Controladores.Mantenimiento.Estructura_view_movimientos import *
from .Controladores.Mantenimiento.Estructura_view_procesos import *
from .Controladores.Matriculacion.View_estudiante import *

from .Diccionario.Estructuras_tablas_conf import ConfMenu, ConfUsuario, ConfModulo_menu, ConfPermiso
from .Diccionario.Estructuras_tablas_mant import *
from .utils import verify_password, hash_password, needs_password_migration

logger = logging.getLogger(__name__)


def inicio(request):
    contexto = {}
    permiso = ConfMenu.objects.filter(
        fk_permiso_modmenu__id_rol__fk_rol__id_usuario=request.session.get('usuario'),
        id_genr_estado=97
    ).values()
    usuario = ConfUsuario.objects.get(
        id_usuario=request.session.get('usuario'))
    contexto['permisos'] = permiso
    contexto['info_usuario'] = usuario
    return render(request, 'base/base.html', contexto)


def login(request):
    contexto = {}
    try:
        if request.method == 'POST':
            var_usuario = request.POST.get('usu', '').strip()
            var_contra = request.POST.get('pass', '')

            if not var_usuario or not var_contra:
                contexto['error'] = "Por favor ingrese usuario y contraseña"
                return render(request, 'base/login.html', contexto)

            # Buscar usuario normal activo
            usu = ConfUsuario.objects.filter(
                usuario=var_usuario, id_genr_estado=97).first()
            if usu and verify_password(var_contra, usu.clave):
                # Migrar contraseña de SHA1 a PBKDF2 si es necesario
                if needs_password_migration(usu.clave):
                    usu.clave = hash_password(var_contra)
                    usu.save(update_fields=['clave'])
                    logger.info(f"Contraseña migrada a PBKDF2 para usuario: {var_usuario}")

                request.session['usuario'] = usu.id_usuario
                request.session['val'] = False
                return redirect("Academico:inicio")

            # Buscar usuario temporal
            usu_temp = UsuarioTemp.objects.filter(usuario=var_usuario).first()
            if usu_temp and verify_password(var_contra, usu_temp.clave):
                request.session['usuario'] = usu_temp.id_usuario_temp
                request.session['val'] = True
                return redirect("Academico:editar_estudiante", pk=usu_temp.id_persona.id_persona)

            # Credenciales incorrectas
            logger.warning(f"Intento de login fallido para usuario: {var_usuario}")
            contexto['error'] = "Usuario o contraseña incorrectos"
            return render(request, 'base/login.html', contexto)

    except Exception as e:
        logger.error(f"Error en login: {e}")
        contexto['error'] = "Usuario o contraseña incorrectos"
        return render(request, 'base/login.html', contexto)

    return render(request, 'base/login.html', contexto)


def salir(request):
    request.session.flush()
    return HttpResponseRedirect('../')


def pantalla_principal(request):
    usuarios = ConfUsuario.objects.filter(id_genr_estado=97).count()
    personas = MantPersona.objects.count()
    alumnos = MantEstudiante.objects.count()
    empleados = MantEmpleado.objects.count()
    return render(request, 'sistemaAcademico/Pantalla_principal.html', {
        'usuarios': usuarios,
        'personas': personas,
        'alumnos': alumnos,
        'empleados': empleados,
    })


def timeout(request):
    return render(request, 'sistemaAcademico/timeout.html')


class Error404(TemplateView):
    template_name = 'errores/404.html'


class Error500(TemplateView):
    template_name = 'errores/500.html'

    @classmethod
    def as_error_view(cls):
        v = cls.as_view()

        def view(request):
            r = v(request)
            r.render()
            return r
        return view

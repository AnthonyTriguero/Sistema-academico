import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .Diccionario.Estructuras_tablas_conf import (
    ConfMenu, ConfUsuario, ConfModulo_menu, ConfPermiso, UsuarioTemp,
)
from .Diccionario.Estructuras_tablas_mant import MantPersona, MantEstudiante, MantEmpleado
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
                # Precargar permisos en sesión para evitar queries en cada request
                from .context_processors import cargar_permisos_en_sesion
                cargar_permisos_en_sesion(request, usu.id_usuario)
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


def handler_500(request):
    """
    Handler personalizado para errores 500.
    Renderiza el template de error 500 de forma segura.
    """
    try:
        return render(request, 'errores/500.html', status=500)
    except Exception:
        # Si falla el render del template, usar respuesta básica
        from django.http import HttpResponse
        return HttpResponse(
            '<h1>Error 500</h1><p>Error interno del servidor. Contacte con el administrador.</p>',
            status=500
        )

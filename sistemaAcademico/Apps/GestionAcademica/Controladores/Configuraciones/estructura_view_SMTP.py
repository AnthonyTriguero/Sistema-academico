import logging
from sistemaAcademico.Apps.GestionAcademica.utils import hash_password
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from decouple import config
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from sistemaAcademico import settings
from sistemaAcademico.Apps.GestionAcademica import forms
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfCorreosSmpt, UsuarioTemp
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mant import MantPersona

from django.core.mail import EmailMultiAlternatives

from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTP, SMTPException

logger = logging.getLogger(__name__)

def smtp_reenviar(request,pk):
    logger.debug("POST data: %s", request.POST)
    error = None
    persona= MantPersona.objects.get(id_persona=pk)
    if (request.method == "POST"):
        form = forms.UsuarioTempForm(request.POST)
        if(form.is_valid()):
            cualquiera = form.save()
            pwd = cualquiera.clave
            cualquiera.clave = hash_password(cualquiera.clave)
            cualquiera.save()
            update = UsuarioTemp.objects.get(id_usuario_temp=cualquiera.id_usuario_temp)
            update.id_persona=persona
            update.save()
            usuario = {"nombre_usuario":cualquiera.usuario,"password":pwd}
            enviar_correo_usuario(cualquiera.correo,None,usuario)
            return redirect("Academico:estudiante")
        else:
            error = "No se pudo guardar"
    else:
        form = forms.UsuarioTempForm()
    return render(request, "sistemaAcademico/Configuraciones/SMTP/Usuario_temp.html", {"form":form,"error": error,"persona":persona})

def smtp_view(request):
    if 'usuario' in request.session:
        error = None
        form = None
        if(request.method == "POST"):
            form = forms.SMTPForm(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect("Academico:menu")
            else:
                error = "No se pudo Guardar el formulario"
        else:
                campo = ConfCorreosSmpt.objects.all().exists()
                if campo is True:
                    return redirect("Academico:edit_smtp", 1)
                else:
                    form = forms.SMTPForm()
        return render(request, "sistemaAcademico/Configuraciones/SMTP/Ingresar_SMTP.html", {"form": form, "error": error})
    else:
        return HttpResponseRedirect('timeout/')

class smtp_edit(UpdateView):
    model = ConfCorreosSmpt
    template_name = "sistemaAcademico/Configuraciones/SMTP/Ingresar_SMTP.html"
    form_class = forms.SMTPForm
    context_object_name = "form"
    success_url = reverse_lazy("Academico:usuarios")

def obtener_parametros():
    configuracion = ConfCorreosSmpt.objects.get(
        id_genr_estado=97)
    return configuracion


def enviar_correo_usuario(correo, url_template, usuario):
    smtp = obtener_parametros()
    subject = 'Preinscripción de estudiantes'
    if(url_template):
        template = get_template(url_template)
    else:
        template = get_template('Correos/correo_verificacion.html')
    content = template.render({'user': usuario, })
    mine_message = MIMEText(content, "html", _charset='utf-8')
    mine_message['From'] = 'Sistema Academico'
    mine_message['To'] = 'Usuario Temporal'
    mine_message['Subject'] = subject
    if(smtp.ssl == 'True'):
        try:
            logger.debug("SMTP login usuario: %s", smtp.usuario_c)
            client = SMTP_SSL(str(smtp.dominio), int(
                smtp.puerto))
            client.login(str(smtp.usuario_c),str(smtp.contrasenia_c))
            client.set_debuglevel(int(1))
            client.sendmail(smtp.usuario_c, correo, mine_message.as_string())
            client.quit()
        except SMTPException as e:
            logger.error("Error SMTP: %s", e)
    else:
        try:
            client = SMTP(str(smtp.dominio), int(smtp.puerto))
            client.login(str(smtp.usuario_c), str(smtp.contrasenia_c))
            client.set_debuglevel(int(1))
            client.login(str(smtp.usuario_c),
                        str(smtp.contrasenia_c))
            client.sendmail(smtp.usuario_c, correo, mine_message.as_string())
            client.quit()
        except SMTPException as e:
            logger.error("Error SMTP: %s", e)
        

def view_temporal(request):
    error = None
    if(request.method == "POST"):
        logger.debug("POST data: %s", request.POST)
        form = forms.SMTPForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect("Academico:menu")
        else:
            error = "no se pudo guardar el formulario"
    else:
        campo = ConfCorreosSmpt.objects.all().exists()
    if campo is True:
        return redirect("Academico:edit_smtp", 1)
    else:
        form = forms.SMTPForm()

    return render(request, "sistemaAcademico/Configuraciones/SMTP/Ingresar_SMTP.html", {"form": form, "error": error})

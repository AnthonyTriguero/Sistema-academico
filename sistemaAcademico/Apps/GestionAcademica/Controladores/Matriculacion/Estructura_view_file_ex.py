import logging

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from sistemaAcademico.Apps.GestionAcademica.models  import MantPersona, MantEstudiante,MovDetalleMateriaCurso
from sistemaAcademico.Apps.GestionAcademica.models  import GenrGeneral, UsuarioTemp
from sistemaAcademico.Apps.GestionAcademica.models  import ConfUsuario, ConfRol
from sistemaAcademico.Apps.GestionAcademica.models import MovMatriculacionEstudiante, Mov_Aniolectivo_curso
from sistemaAcademico.Apps.GestionAcademica.Forms.Admision.form_file import UploadFileForm
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from sistemaAcademico.Apps.GestionAcademica.utils import hash_password

import os
from django.shortcuts import render
import pandas as pd
import xlrd

from django.utils import timezone
import socket

logger = logging.getLogger(__name__)


class Upload_FileEX(View):

    template_name = 'sistemaAcademico/Matriculacion/PreRegistro/preregistro_ex.html'
    success_url = reverse_lazy('Academico:estudiante')
    form_class = UploadFileForm

    def clearString(self, entrada):
        entrada = entrada.replace("'", "")
        entrada = entrada.replace(".", "")
        entrada = entrada.replace(":", "")
        entrada = entrada.replace("\\", "")
        entrada = entrada.replace("/", "")
        entrada = entrada.replace("*", "")
        entrada = entrada.replace("!", "")
        entrada = entrada.replace("-", "")

        return entrada


   
    def handle_uploaded_file(self, file, filename, request,id_mov_anioelectivo_curso):
            global apellidos
            global nombres
            logger.info("Leyendo archivo...")
            usuario = ConfUsuario.objects.get(
               id_usuario=request.session.get('usuario'))

            if not os.path.exists('files/'):
                os.mkdir('files/')

            materias = MovDetalleMateriaCurso.objects.filter(id_mov_anio_lectivo_curso=id_mov_anioelectivo_curso).count()
            
            
            if materias>0:
                array = filename.split('.')
                if array[1] == 'xlsx' or array[1] =='xlsx':
                    with open('files/' + filename, 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)

                    documento = xlrd.open_workbook(('files/{0}').format(filename))
                    listado_est = documento.sheet_by_index(0)

                    for i in range(12, listado_est.nrows):
                        nombre = None
                        cedula = None
                        for j in range(listado_est.ncols):
                            tipo = listado_est.cell_type(i, j)
                            if tipo != 0:
                                if j == 1:
                                    cedula = repr(listado_est.cell_value(i, j))
                                    cedula = self.clearString(cedula)

                                elif j == 2:
                                    nombre = repr(listado_est.cell_value(i, j))
                                    nombre = self.clearString(nombre)

                                    nombreCompleto = nombre.split(" ")
                                    if len(nombreCompleto) == 4:
                                        apellidos = nombreCompleto[0] + \
                                            " "+nombreCompleto[1]
                                        nombres = nombreCompleto[2] + \
                                            " "+nombreCompleto[3]
                                    else:
                                        continue
                        
                        if nombres !='' or nombres is not None and apellidos !='' or apellidos is not None and cedula !='' or cedula is not None:
                            persona = MantPersona.objects.filter(identificacion=cedula).first()
                            if persona:
                                    messages.error(request, 'Uno de los estudiantes ya esta ingresado' )
                                    logger.debug("Estudiante ya ingresado")
                            else:
                                personSave = MantPersona(nombres=nombres,apellidos=apellidos,identificacion=cedula,
                                estado=GenrGeneral.objects.get(nombre='ACTIVO'),fecha_ingreso=timezone.now(),usuario_ing= usuario.usuario,terminal_ing=socket.gethostname(),id_genr_tipo_usuario=GenrGeneral.objects.get(idgenr_general=19))
                                personSave.save()

                                estudiante = MantEstudiante(id_persona=MantPersona.objects.get(id_persona=personSave.id_persona),tipo_estudiante='Asignado',fecha_ingreso=timezone.now(),
                                usuario_ing= usuario.usuario,terminal_ing=socket.gethostname())
                                estudiante.save()

                                matriculacion = MovMatriculacionEstudiante(id_estudiante=MantEstudiante.objects.get(id_estudiante=estudiante.id_estudiante),
                                id_mov_anioelectivo_curso=Mov_Aniolectivo_curso.objects.get(id_mov_anioelectivo_curso=id_mov_anioelectivo_curso),estado=GenrGeneral.objects.get(nombre='INACTIVO'),fecha_ingreso=timezone.now(),usuario_ing=usuario.usuario,terminal_ing=socket.gethostname())
                                matriculacion.save()
                                logger.debug("Persona guardada: %s", personSave)
                                try:
                                    rol = ConfRol.objects.filter(codigo='003').first()
                                    if rol:
                                        UsuarioTemp.objects.create(usuario=cedula,clave=hash_password(cedula),id_rol=rol,id_persona=personSave)
                                except Exception:
                                    logger.exception("Error al crear UsuarioTemp para cédula %s", cedula)
                                messages.success(request, 'Ingreso correcto', extra_tags='safe')
                        else:
                            logger.warning("Campo incorrecto")
                            messages.error(request, 'Campo incorrecto' )
                    
                else:
                    messages.error(request, 'Formato de archivo no sorportado')
                    form = UploadFileForm
            else:
                messages.error(request, 'Este Curso no tiene materias asignadas')
                form = UploadFileForm

    def get(self, request, *args, **kwargs):
     
        form= self.form_class
       
        return render(request, self.template_name, {  'form' : form})

    def post(self, request, *args, **kwargs):
        
        form = UploadFileForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            
            self.handle_uploaded_file(self.request.FILES['file'], str(
                self.request.FILES['file']), request, form.cleaned_data['curso'])
        else:
            form = UploadFileForm
        return render(request, self.template_name, {  'form' : self.form_class, })

import logging

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mov import MovDetalleRegistroNotas,Mov_Materia_profesor,MovMatriculacionEstudiante,MovDetalleMateriaCurso,MovCabRegistroNotas,Mov_Aniolectivo_curso
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfUsuario
from sistemaAcademico.Apps.GestionAcademica.Forms.Matriculacion.forms_registro_notas import Registro_notas_form
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mant import MantEmpleado,MantPersona
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404


#PRIMER QUIMESTRE
from sistemaAcademico.Apps.GestionAcademica.Forms.Quimestrales.Primer_Quimestre.forms_primer_quimestre import EstudianteForm
from sistemaAcademico.Apps.GestionAcademica.Forms.Quimestrales.Primer_Quimestre.forms_quimestral_edi import EstudianteFormEdit

#SEGUNDO QUIMESTRE
from sistemaAcademico.Apps.GestionAcademica.Forms.Quimestrales.Segundo_Quimestre.forms_segundo_quimestre import EstudianteForm2
from sistemaAcademico.Apps.GestionAcademica.Forms.Quimestrales.Segundo_Quimestre.forms_quimestral_edi2 import EstudianteFormEdit2


#Supretorio
from sistemaAcademico.Apps.GestionAcademica.Forms.Quimestrales.forms_generales import Generales_notas_form

logger = logging.getLogger(__name__)


#CREAR LA NOTA

class CrearRegistroNotas(CreateView):
    model = MovDetalleRegistroNotas
    form_class = EstudianteForm
    template_name = 'sistemaAcademico/RegistrodeNotas/Nota1Quimestre/crear.html'
    success_url = reverse_lazy('Academico:listar_materia')


# VER LAS NOTAS GENERAL

class List_Notas(ListView):
    model = MovDetalleRegistroNotas
    template_name = 'sistemaAcademico/Matriculacion/RegistroNotas/RegistroNotas.html'
    context_object_name = 'm'


#POR SI SE QUEDA SUPRETORIO, REMEDIAL O GRACIA
class Update_notasSupre(UpdateView):
    model = MovDetalleRegistroNotas
    template_name = 'sistemaAcademico/RegistrodeNotas/NotaGeneral/NotasSupre.html'
    form_class = Generales_notas_form
    success_url = reverse_lazy('Academico:registro_notas')
    context_object_name = 'notas'

    def get_context_data(self, *args, **kwargs):
        context = super(Update_notasSupre, self).get_context_data(**kwargs)
        objecto = context['notas']
        context['alumno'] = objecto.id_matriculacion_estudiante
        # id de la materia profesor
        id_materia_prof = objecto.id_materia_profesor.id_materia_profesor
        # obtiene el registro de matricula
        matricula = MovMatriculacionEstudiante.objects.get(
            id_matriculacion_estudiante=objecto.id_matriculacion_estudiante.id_matriculacion_estudiante)
        # id del año lectivo
        id_anio_lectivocurso = matricula.id_mov_anioelectivo_curso.id_mov_anioelectivo_curso
        # recorre todas las materias que tiene ese curso en ese paralelo
        for i in MovDetalleMateriaCurso.objects.filter(id_mov_anio_lectivo_curso=id_anio_lectivocurso):
            try:
                # obtiene el profesor de esa materia
                materia = Mov_Materia_profesor.objects.get(id_detalle_materia_curso=i.id_detalle_materia_curso)
                if materia:
                    if materia.id_materia_profesor == id_materia_prof:
                        context['profesor'] = materia
                        context['materia'] = i
            except Exception as e:
                logger.error("Error: %s", e)

        return context





#1 QUIMESTRE

class ListarMateria(ListView):
    model = MovDetalleRegistroNotas
    queryset = model.objects.all()
    template_name = 'sistemaAcademico/RegistrodeNotas/Nota1Quimestre/listar_materia.html'
    context_object_name = 'inst'



class Update_notas(UpdateView):
    model = MovDetalleRegistroNotas
    template_name = 'sistemaAcademico/RegistrodeNotas/Nota1Quimestre/ActualizarNotas.html'
    form_class = EstudianteFormEdit
    success_url = reverse_lazy('Academico:listar_materia')
    context_object_name = 'notas'

    def get_context_data(self, *args, **kwargs):
        context = super(Update_notas, self).get_context_data(**kwargs)
        objecto = context['notas']
        context['alumno'] = objecto.id_matriculacion_estudiante
        context['quimestre'] = objecto.id_general_quimestre_1
        # id de la materia profesor
        id_materia_prof = objecto.id_materia_profesor.id_materia_profesor
        # obtiene el registro de matricula
        matricula = MovMatriculacionEstudiante.objects.get(
            id_matriculacion_estudiante=objecto.id_matriculacion_estudiante.id_matriculacion_estudiante)
        # id del año lectivo
        id_anio_lectivocurso = matricula.id_mov_anioelectivo_curso.id_mov_anioelectivo_curso
        # recorre todas las materias que tiene ese curso en ese paralelo
        for i in MovDetalleMateriaCurso.objects.filter(id_mov_anio_lectivo_curso=id_anio_lectivocurso):
            try:
                # obtiene el profesor de esa materia
                materia = Mov_Materia_profesor.objects.get(id_detalle_materia_curso=i.id_detalle_materia_curso)
                if materia:
                    if materia.id_materia_profesor == id_materia_prof:
                        context['profesor'] = materia
                        context['materia'] = i
            except Exception as e:
                logger.error("Error: %s", e)

        return context





#2 QUIMESTRE


class ListarMateria2(ListView):
    model = MovDetalleRegistroNotas
    queryset = model.objects.all()
    template_name = 'sistemaAcademico/RegistrodeNotas/Nota2Quimestre/listar_materia.html'
    context_object_name = 'inst'


class Update_notas2(UpdateView):
    model = MovDetalleRegistroNotas
    template_name = 'sistemaAcademico/RegistrodeNotas/Nota2Quimestre/ActualizarNotas.html'
    form_class = EstudianteFormEdit2
    success_url = reverse_lazy('Academico:listar_materia2')
    context_object_name = 'notas'

    def get_context_data(self, *args, **kwargs):
        context = super(Update_notas2, self).get_context_data(**kwargs)
        objecto = context['notas']
        context['alumno'] = objecto.id_matriculacion_estudiante
        context['quimestre'] = objecto.id_general_quimestre_2
        # id de la materia profesor
        id_materia_prof = objecto.id_materia_profesor.id_materia_profesor
        # obtiene el registro de matricula
        matricula = MovMatriculacionEstudiante.objects.get(
            id_matriculacion_estudiante=objecto.id_matriculacion_estudiante.id_matriculacion_estudiante)
        # id del año lectivo
        id_anio_lectivocurso = matricula.id_mov_anioelectivo_curso.id_mov_anioelectivo_curso
        # recorre todas las materias que tiene ese curso en ese paralelo
        for i in MovDetalleMateriaCurso.objects.filter(id_mov_anio_lectivo_curso=id_anio_lectivocurso):
            try:
                # obtiene el profesor de esa materia
                materia = Mov_Materia_profesor.objects.get(id_detalle_materia_curso=i.id_detalle_materia_curso)
                if materia:
                    if materia.id_materia_profesor == id_materia_prof:
                        context['profesor'] = materia
                        context['materia'] = i
            except Exception as e:
                logger.error("Error: %s", e)

        return context



#Eliminar la Nota
class Delete_notas(DeleteView):
    model = MovDetalleRegistroNotas
    template_name = 'sistemaAcademico/Matriculacion/RegistroNotas/EliminarNotas.html'
    success_url = reverse_lazy('Academico:registro_notas')
    context_object_name = 'a'





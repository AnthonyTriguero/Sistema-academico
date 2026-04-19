# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db.models import AutoField
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import (
    GenrGeneral, GenrHistorial,
)
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mant import (
    MantPersona, MantRepresentante, MantEstudiante, MantAnioLectivo, MantEmpleado,
)
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import (
    ConfEmpresa, ConfModulo, ConfRol, ConfMenu, ConfUsuario, ConfModulo_menu,
    ConfAccion, UsuarioTemp, ConfPermiso, ConfCorreosSmpt,
)
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mov import (
    MovAdmision, MovCabCurso, MovCabRegistroNotas, Mov_Aniolectivo_curso,
    MovDetalleMateriaCurso, MovDetalleRegistroNotas, MovMatriculacionEstudiante,
    Mov_Materia_profesor, Mov_Horario_materia, Mov_Horas_docente,
)




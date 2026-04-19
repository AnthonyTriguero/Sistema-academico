
from django import forms

from sistemaAcademico.Apps.GestionAcademica.Forms.Configuracion.forms_configuraciones import (
    SMTPForm, modulo_form, menu_form, unidad_form, EditarU_form,
    UsuarioModelForm, UsuarioeditModelForm, UsuarioTempForm, AccionesForm, Permisosform,
)
from sistemaAcademico.Apps.GestionAcademica.Forms.Admision.forms_mantenimientos import (
    EmpleadoForm, EditarEmpleadoForm, ConsultarEmpleadoForm,
    EstudianteForm, EstudianteEditForm, ConsultarEstudianteForm, Editarste,
)
from sistemaAcademico.Apps.GestionAcademica.Forms.Admision.form_file import UploadFileForm



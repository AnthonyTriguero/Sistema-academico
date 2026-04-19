from datetime import datetime

from dal import autocomplete
from django.forms import CharField, ChoiceField, ModelForm
from django.db.models import Q
from sistemaAcademico.Apps.GestionAcademica import models
from django import forms
import django_filters
from django.utils import timezone
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mov import Mov_Horario_materia


class HorarioCursoForm(ModelForm):
    class Meta:
        model = Mov_Horario_materia
        fields = [
            "hora_inicio",
            "hora_fin",
            "id_genr_dia",
            "id_materia_profesor",

        ]
        labels = {
            "hora_inicio": "Hora De Inicio",
            "hora_fin": "Hora De Fin",
            "id_genr_dia":"Dia",
            "id_materia_profesor": "Profesor",
        }
        widgets ={
            "hora_inicio": forms.TimeInput() ,
            "hora_fin":  forms.TimeInput()
        }

    def __init__(self, *args, **kwargs):
        super(HorarioCursoForm, self).__init__(*args, **kwargs)
        self.fields['id_genr_dia'].queryset =GenrGeneral.objects.filter(tipo='DLS')

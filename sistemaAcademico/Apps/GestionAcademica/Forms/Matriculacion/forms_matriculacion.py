from django.db.models import Q

from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mant import MantAnioLectivo
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from django import forms

from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mov import MovCabCurso


class Aniolectivo (forms.ModelForm):
    class Meta:
        model =MantAnioLectivo
        fields = ['anio',
                  'ciclo',
                  'fecha_incio_ciclo',
                  'fecha_fin_ciclo',
                  'id_genr_estado']
        labels = {'anio': 'Año',
                  'ciclo': 'Ciclo',
                  'fecha_incio_ciclo': 'Inicio del ciclo',
                  'fecha_fin_ciclo': 'Fin del ciclo',
                  'id_genr_estado':'Estado'}
        widgets = {'anio': forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ingrese el año lectivo"}),
                   'ciclo': forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ingrese el ciclo"}),
                   'fecha_incio_ciclo': forms.DateTimeInput(attrs={"class": "form-control text-dark", "type": "date"}),
                   'fecha_fin_ciclo': forms.DateTimeInput(attrs={"class": "form-control text-dark", "type": "date"})}

    def __init__(self, *args, **kwargs):
        super(Aniolectivo, self).__init__(*args, **kwargs)
        self.fields['id_genr_estado'].queryset = GenrGeneral.objects.filter(Q(idgenr_general=97) | Q(idgenr_general=99) | Q(idgenr_general=1784))

class UpAniolectivo (forms.ModelForm):
    class Meta:
        model = MantAnioLectivo
        fields = ['anio',
                  'ciclo',
                  'fecha_incio_ciclo',
                  'fecha_fin_ciclo',
                  'id_genr_estado'
                  ]
        labels = {'anio': 'Año',
                  'ciclo': 'Ciclo',
                  'fecha_incio_ciclo': 'Inicio del ciclo',
                  'fecha_fin_ciclo': 'Fin del ciclo',
                  'id_genr_estado':'Estado'
                  }
        widgets = {'anio': forms.NumberInput(attrs={"class": "form-control"}),
                   'ciclo': forms.NumberInput(attrs={"class": "form-control"}),
                   'fecha_incio_ciclo': forms.DateInput(attrs={"class": "form-control text-dark"}),
                   'fecha_fin_ciclo': forms.DateInput(attrs={"class": "form-control text-dark"}),
                   }
    def __init__(self, *args, **kwargs):
        super(UpAniolectivo, self).__init__(*args, **kwargs)
        self.fields['id_genr_estado'].queryset = GenrGeneral.objects.filter(Q(idgenr_general=97) | Q(idgenr_general=99) | Q(idgenr_general=1784))



class CabCursoForm (forms.ModelForm):

    class Meta:
        model= MovCabCurso
        fields=[
            'codigo',
            'nombre',
            'id_genr_regimen',
            'id_genr_modalidad',
            'id_genr_tipo_edu',
            'id_genr_formacion',
            'id_genr_curso',
            'id_genr_jornada',
            'cupo'
        ]

        labels={
            'codigo':'Codigo',
            'nombre':'Nombre',
            'id_genr_regimen':'Regimen',
            'id_genr_modalidad':'Modalidad',
            'id_genr_tipo_edu':'Tipo de Educación',
            'id_genr_formacion': 'Nivel',
            'id_genr_curso': 'Curso',

            'id_genr_jornada':'Jornada',
            'cupo':'Numero de cupos'
        }
        widgets={
            'codigo':forms.TextInput(attrs={'class':'form-control'}),
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'cupo':forms.NumberInput(attrs={'class':'form-control'})
        }


    def __init__(self, *args, **kwargs):
        super(CabCursoForm, self).__init__(*args, **kwargs)
        self.fields['id_genr_regimen'].queryset = GenrGeneral.objects.filter(
            tipo='TRE')
        self.fields['id_genr_modalidad'].queryset = GenrGeneral.objects.filter(
            tipo='MOD')
        self.fields['id_genr_tipo_edu'].queryset = GenrGeneral.objects.filter(
            tipo='TED')
        self.fields['id_genr_curso'].queryset = GenrGeneral.objects.filter(
            tipo='TIC')
        self.fields['id_genr_formacion'].queryset = GenrGeneral.objects.filter(
            tipo='NIV')
        self.fields['id_genr_jornada'].queryset = GenrGeneral.objects.filter(
            tipo='JOR')


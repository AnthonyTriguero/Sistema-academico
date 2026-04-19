from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from django import forms


class GenrGeneral_1(forms.ModelForm):
    class Meta:
        model = GenrGeneral
        fields =['tipo',
                 'codigo',
                 'nombre',
                 ]

        labels={
            'tipo':'Tipo',
            'codigo':'Codigo',
            'nombre':'Nombre',
        }

        widgets = {

            'tipo': forms.TextInput(attrs={'class':'from-control',"placeholder": "Ingrese el tipo"}),
            'codigo': forms.TextInput(attrs={'class':'from-control',"placeholder": "Ingrese el codigo"}),
            'nombre': forms.TextInput(attrs={'class':'from-control',"placeholder": "Ingrese el nombre"}),
        }



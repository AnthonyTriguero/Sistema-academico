from sistemaAcademico.Apps.GestionAcademica import models
from django import forms
from django.forms import ModelForm
from betterforms.multiform import MultiModelForm
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import (
    ConfCorreosSmpt, ConfModulo, ConfMenu, ConfEmpresa, ConfUsuario,
    UsuarioTemp, ConfAccion, ConfPermiso,
)
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from django_select2.forms import Select2MultipleWidget
from django_select2.forms import ModelSelect2MultipleWidget
from collections import OrderedDict
from django.db.models import Q



class SMTPForm(forms.ModelForm):
    class Meta:
        model = ConfCorreosSmpt
        fields = [
            "ssl",
            "dominio",
            "puerto",
            "usuario_c",
            "contrasenia_c",
            "descripcion",
        ]
        labels = {
            "ssl": "Seguridad SSL",
            "dominio": "Servidor",
            "puerto": "Puerto",
            "usuario_c": "Usuario",
            "contrasenia_c": "Clave",
            "descripcion": "Descripcion"
        }
        widgets = {
            "ssl": forms.CheckboxInput(),
            "dominio": forms.TextInput(attrs={"class": "form-control"}),
            "puerto": forms.TextInput(attrs={"class": "form-control", "type": "number"}),
            "usuario_c": forms.TextInput(attrs={"class": "form-control"}),
            "contrasenia_c": forms.TextInput(attrs={"class": "form-control", "type": "password"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"})
        }


class modulo_form(forms.ModelForm):

    class Meta:
        model = ConfModulo
        fields = ['codigo', 'nombre', ]
        labels = {
            'codigo': 'Codigo',
            'nombre': 'Nombre',
        }

        widgets = {
            'codigo': forms.TextInput(attrs={"class": "form-control", "max": "100", "min": "0", "placeholder": "Ingrese codigo para este nuevo modulo", "type": "number "}),
            'nombre': forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese nombre para este nuevo modulo"}),
        }

        def clean_codigo(self):
            codigo = self.cleaned_data.get('codigo')
            return codigo


class menu_form(forms.ModelForm):

    class Meta:
        model = ConfMenu
        fields = [
            'id_padre',
            'descripcion',
            'url',
            'icono',
            'lazy_name',
            'name',
            'view'
        ]
        labels = {
            'descripcion': 'Nombre del menu: ',
            'id_padre': 'Modulo: ',
            'url': 'Url del menu: ',
            'icono': 'Icono: ',
            'lazy_name': 'Lazy name: ',
            'name': 'Name:',
                    'view': 'Controlador del menu(View):'
        }
        widgets = {
            'descripcion': forms.TextInput(attrs={"class": "form-control text-dark", "placeholder": "Ingrese nombre para este menu"}),
            'url': forms.TextInput(attrs={"class": "form-control text-dark", "placeholder": "Ingrese una url para este  menu"}),
            'lazy_name': forms.TextInput(attrs={"class": "form-control text-dark", "placeholder": "Ingrese lazy name para este menu"}),
            'name': forms.TextInput(attrs={"class": "form-control text-dark", "placeholder": "Ingrese un name para este nuevo menu"}),
            'view': forms.TextInput(attrs={"class": "form-control text-dark", "placeholder": "Ingrese el nombre controlador para este menu"}),
            'id_padre': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(menu_form, self).__init__(*args, **kwargs)
        self.fields['id_padre'] = forms.ChoiceField(choices=[(
            m.id_menu, m.descripcion ) for m in ConfMenu.objects.filter(Q(id_padre=0) | Q(url__contains
    ='#'))], widget={})


class unidad_form(forms.ModelForm):

    class Meta:
        model = ConfEmpresa
        fields = [
            'nombre',
            'razon_social',
            'id_genr_tipo_identificacion',
            'identificacion',
            'direccion',
            'representante_legal',
            'correo',
            'telefono',
            'fecha_creacion',
            'fecha_ingreso',
            'usuario_ing',
            'terminal_ing',
        ]
        labels = {
            'nombre': 'Nombre de la Unidad: ',
            'razon_social': 'Razon Social: ',
            'id_genr_tipo_identificacion': 'Tipo de Identificacion',
            'identificacion': 'Identificacion: ',
            'direccion': 'Direccion: ',
            'representante_legal': 'Representante Legal: ',
            'correo': 'Correo:',
            'telefono': 'Telefono:',
            'fecha_creacion': 'Fecha de creacion',
            'usuario_ing': '',
            'terminal_ing': ''

        }

        widgets = {
            'nombre': forms.TextInput(attrs={"class": "form-control text-dark", "placeholder": "Ingrese nombre para esta unidad"}),
            'razon_social': forms.TextInput(attrs={"class": "form-control text-dark", "placeholder": "Ingrese una razon para esta unidad"}),
            'identificacion': forms.TextInput(attrs={"class": "form-control text-dark", 'minlength':'10','maxlength':'20', "placeholder": "Ingrese identificacion no duplicada"}),
            'direccion': forms.TextInput(attrs={"class": "form-control text-dark", "placeholder": "Ingrese una direccion"}),
            'representante_legal': forms.TextInput(attrs={"class": "form-control text-dark", "placeholder": "Ingrese el representante_legal"}),
            'correo': forms.TextInput(attrs={"class": "form-control text-dark", "type": "email", "placeholder": "Ingrese una correo"}),
            'telefono': forms.TextInput(attrs={"class": "form-control text-dark", "type": "number",'minleCCCCngth':'10', "placeholder": "Ingrese un telefono"}),
            'fecha_creacion': forms.DateInput(attrs={"class": "form-control text-dark", "type": "date"}),

        }

    def __init__(self, *args, **kwargs):
        super(unidad_form, self).__init__(*args, **kwargs)
        self.fields['id_genr_tipo_identificacion'].queryset = GenrGeneral.objects.filter(
            tipo='TID')

    def clean_cedula(self):
        ced = self.cleaned_data['cedula']
        msg = "La Cédula introducida no es válida"
        valores = [int(ced[x]) * (2 - x % 2) for x in range(9)]
        suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
        veri = 10 - (suma - (10 * (suma / 10)))
        if int(ced[9]) == int(str(veri)[-1:]):
            return ced
        else:
            raise forms.ValidationError(msg)


class EditarU_form(forms.ModelForm):
    class Meta:
        model = ConfEmpresa
        fields = [
            'nombre',
            'razon_social',
            'id_genr_tipo_identificacion',
            'identificacion',
            'direccion',
            'representante_legal',
            'correo',
            'telefono',
            'fecha_creacion',

        ]
        labels = {
        'nombre': 'Nombre de la unidad: ',
        'razon_social': 'nombre de la razon: ',
        'id_genr_tipo_identificacion': 'Tipo de identificacion',
        'identificacion': 'ingrese su identificacion: ',
        'direccion': 'nombre de la direccion: ',
        'representante_legal': 'representante_legal: ',
        'correo': 'correo:',
        'telefono': 'ingrese su telefono:',
        'fecha_creacion': 'fecha de creacion'
        }
        widgets = {
            'nombre': forms.TextInput(
                attrs={"class": "form-control text-dark", "placeholder": "Ingrese nombre para esta unidad"}),
            'razon_social': forms.TextInput(
                attrs={"class": "form-control text-dark", "placeholder": "Ingrese una razon para esta unidad"}),
            'identificacion': forms.TextInput(
                attrs={"class": "form-control text-dark",'minlength':'10','maxlength':'20', "placeholder": "Ingrese identificacion no duplicada"}),
            'direccion': forms.TextInput(
                attrs={"class": "form-control text-dark", "placeholder": "Ingrese una direccion"}),
            'representante_legal': forms.TextInput(
                attrs={"class": "form-control text-dark", "placeholder": "Ingrese el representante_legal"}),
            'correo': forms.TextInput(
                attrs={"class": "form-control text-dark", "type": "email", "placeholder": "Ingrese una correo"}),
            'telefono': forms.NumberInput(
                attrs={"class": "form-control text-dark",'minlength':'10',"placeholder": "Ingrese una telefono"}),
            'fecha_creacion': forms.DateInput(attrs={"class": "form-control text-dark"}),

        }

    def __init__(self, *args, **kwargs):
        super(EditarU_form, self).__init__(*args, **kwargs)
        self.fields['id_genr_tipo_identificacion'].queryset = GenrGeneral.objects.filter(
            tipo='TID')




class UsuarioModelForm(ModelForm):
    class Meta:
        model = ConfUsuario
        fields = [
            "usuario",
            "clave",
            "id_persona",
            "id_genr_tipo_usuario",
            "id_rol",
        ]
        labels = {
            "usuario": "Nombre de usuario :",
            "clave": "Clave :",
            "id_persona": " Persona :",
            "id_genr_tipo_usuario": " Tipo de Usuario ",
            "id_rol": "Tipo de Rol "
        }
        widgets = {
            "usuario": forms.TextInput(attrs={"class": "form-control text-dark", "placeholder": "Ingrese el nombre del usuario"}),
            "clave": forms.TextInput(attrs={"class": "form-control", "type": "password", "placeholder": "Ingrese la clave del usuario"}),
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioModelForm, self).__init__(*args, **kwargs)
        self.fields['id_genr_tipo_usuario'].queryset = GenrGeneral.objects.filter(
            tipo='TUS')


class UsuarioeditModelForm(ModelForm):
    class Meta:
        model = ConfUsuario
        fields = [
            "usuario",
            "id_persona",
            "id_genr_tipo_usuario",
            "id_rol",
        ]
        labels = {
            "usuario": "Nombre de usuario :",
            "id_persona": " Persona :",
            "id_genr_tipo_usuario": " Tipo de Usuario ",
            "id_rol": "Tipo de Rol "
        }
        widgets = {
            "usuario": forms.TextInput(attrs={"class": "form-control text-dark", "placeholder": "Ingrese el nombre del usuario"}),
            "clave": forms.TextInput(attrs={"class": "form-control", "type": "password", "placeholder": "Ingrese la clave del usuario"}),
        }
    def __init__(self, *args, **kwargs):
        super(UsuarioeditModelForm, self).__init__(*args, **kwargs)
        self.fields['id_genr_tipo_usuario'].queryset = GenrGeneral.objects.filter(
            tipo='TUS')



class UsuarioTempForm(forms.ModelForm):
    class Meta:
        model = UsuarioTemp
        exclude = ('fecha_creacion','id_rol','id_persona')
        labels = {
            "Usuario Temporal:":"usuario",
            "Clave Temporal:":"clave",
            "Fecha de Expiracion:":"fecha_limite",
            "Correo del Usuario Temporal:":"correo",
        }
        widgets = {
            "usuario": forms.TextInput(attrs={"class":"form-control"}),
            "clave":forms.TextInput(attrs={"class":"form-control","type":"password"}),
            "fecha_limite":forms.TextInput(attrs={"class":"form-control","type":"date"}),
            "correo":forms.TextInput(attrs={"class":"form-control","type":"email"}),
        }


class AccionesForm(forms.ModelForm):
    class Meta:
        model = ConfAccion
        fields =[
            "id_rol",
            "id_menu",
            "descripcion",
        ]

        labels = {
            "id_rol": "Rol",
            "descripcion": "Acciones disponibles en el sistema",
            "id_menu": "Menus disponibles",
        }



class Permisosform(forms.ModelForm):
    class Meta:
        model = ConfPermiso
        fields = [
            "menu",
            "id_rol",
        ]
        labels = {
            "menu": "Menus disponibles",
            "id_rol": "Rol",
        }

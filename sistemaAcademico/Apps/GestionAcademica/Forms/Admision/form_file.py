import logging

from django import forms
from sistemaAcademico.Apps.GestionAcademica.models import Mov_Aniolectivo_curso

logger = logging.getLogger(__name__)


class UploadFileForm(forms.Form):
    try:
        Lista = Mov_Aniolectivo_curso.objects.filter(id_estado_gnral=97)
        curso = forms.ChoiceField(
            choices=(
                (x.id_mov_anioelectivo_curso, x) for x in Lista
            ),
            widget=forms.Select(
                attrs={'class': 'form-control'}
            )
        )
        file = forms.FileField(
            required=True,
            widget=forms.FileInput(
                attrs={'class': 'form-control'}
            )
        )
    except Exception as e:
        logger.error("Error en formulario de archivo")
    

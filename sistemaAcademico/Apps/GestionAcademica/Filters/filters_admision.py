from dal import autocomplete
from django.db.models import Q

from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral


# TIPO DE IDENTIFICACION
class TID_autocomplete(autocomplete.Select2QuerySetView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = GenrGeneral.objects.filter(tipo='TID').order_by("nombre")
        if self.q:
            qs = qs.filter(Q(nombre__icontains=self.q))
        return qs

    def has_add_permission(self, request):
        return True


# TIPO DE GENERO
class GEN_autocomplete(autocomplete.Select2QuerySetView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = GenrGeneral.objects.filter(tipo='GEN').order_by("nombre")
        if self.q:
            qs = qs.filter(Q(nombre__icontains=self.q))
        return qs

    def has_add_permission(self, request):
        return True

class TID_autocomplete(autocomplete.Select2QuerySetView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = GenrGeneral.objects.filter(tipo='TID').order_by("nombre")
        if self.q:
            qs = qs.filter(Q(nombre__icontains=self.q))
        return qs

    def has_add_permission(self, request):
        return True


class MenuAutocomplete(autocomplete.Select2QuerySetView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = GenrGeneral.objects.filter(tipo='TID').order_by("nombre")
        if self.q:
            qs = qs.filter(Q(nombre__icontains=self.q))
        return qs

    def has_add_permission(self, request):
        return True

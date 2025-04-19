from django import forms
from .models import Arma

class ArmaForm(forms.ModelForm):
    class Meta:
        model = Arma
        fields = ['serial', 'tipo', 'estado', 'almacen_actual', 'asignada_a', 'fija_en_puesto', 'licencia_digital', 'fecha_vencimiento_licencia']

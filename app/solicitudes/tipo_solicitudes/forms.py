from django import forms
from .models import TipoSolicitud

class FormTipoSolicitud(forms.ModelForm):
    class Meta:
        model = TipoSolicitud
        fields = '__all__'
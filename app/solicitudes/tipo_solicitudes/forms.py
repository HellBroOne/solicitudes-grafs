from django import forms
from .models import TipoSolicitud, FormularioSolicitud, CampoFormulario, Solicitud, ArchivoAdjunto

class FormTipoSolicitud(forms.ModelForm):
    class Meta:
        model = TipoSolicitud
        fields = '__all__'

class FormFormularioSolicitud(forms.ModelForm):
    class Meta:
        model = FormularioSolicitud
        fields = '__all__'

class FormCampoFormulario(forms.ModelForm):
    def __init__(self, *args, formulario=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.formulario = formulario
    
    class Meta:
        model = CampoFormulario
        fields = ['nombre', 'etiqueta', 'tipo', 'requerido', 'opciones', 'cantidad_archivos', 'orden']
        widgets = {
            'opciones': forms.Textarea(attrs={'rows': 3}),
        }

class FormSolicitud(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = '__all__'

class FormArchivoAdjunto(forms.ModelForm):
    class Meta:
        model = ArchivoAdjunto
        fields = '__all__'

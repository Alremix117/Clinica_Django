from django import forms
from .models import Paciente, Paciente_Pais, Paciente_Discapacidad, Pais, Discapacidad

class FormPaciente(forms.ModelForm):    
    fecha_nacimiento = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'text', 'placeholder': 'YYYY-MM-DD HH:mm'}
        ),
        input_formats=['%Y-%m-%d %H:%M'],
        label="Fecha de Nacimiento"
    )
    class Meta:
        model = Paciente
        fields = [
            'numero_documento', 'primer_nombre', 'segundo_nombre',
            'primer_apellido', 'segundo_apellido', 'fecha_nacimiento',
            'sexo_biologico', 'identidad_genero', 'zona_territorial_residencia',
            'tipo_documento', 'residencia', 'ocupacion', 'etnia',
            'comunidad_Etnica', 'entidad_prestadora_salud'
        ]

class FormNacionalidad(forms.Form):
    paises = forms.ModelMultipleChoiceField(
        queryset=Pais.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Nacionalidades"
    )

class FormDiscapacidad(forms.Form):
    discapacidades = forms.ModelMultipleChoiceField(
        queryset=Discapacidad.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Discapacidades"
    )

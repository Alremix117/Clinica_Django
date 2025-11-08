from django import forms
from .models import Paciente, Voluntad_Anticipada, Oposicion_Donacion, Pais, Discapacidad

class FormPaciente(forms.ModelForm):    
    fecha_nacimiento = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD HH:mm'}
        ),
        input_formats=['%Y-%m-%d %H:%M'],
        label="Fecha de Nacimiento"
    )
    segundo_nombre = forms.CharField(
        required=False,
    )

    segundo_apellido = forms.CharField(
        required=False,
    )

    class Meta:
        model = Paciente
        fields = [
            'tipo_documento', 'numero_documento', 'primer_nombre', 'segundo_nombre',
            'primer_apellido', 'segundo_apellido', 'fecha_nacimiento',
            'sexo_biologico', 'identidad_genero', 'zona_territorial_residencia',
            'residencia', 'ocupacion', 'etnia',
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

class FormVoluntadAnticipada(forms.ModelForm):
    fecha_suscripcion_documento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d %H:%M'],
        required=False
    )
    
    class Meta:
        model = Voluntad_Anticipada
        fields = ['documento_voluntad_anticipada', 'fecha_suscripcion_documento', 'codigo_entidad_prestadora']
        labels = {
            'documento_voluntad_anticipada': "¿Existe Voluntad Anticipada?",
            'fecha_suscripcion_documento': "Fecha de Documento",
            'codigo_entidad_prestadora': "Entidad donde se registró",
        }

class FormOposicionDonacion(forms.ModelForm):
    fecha_suscripcion_documento = forms.DateField(
        widget=forms.DateTimeInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d %H:%M'],
        required=False
    )

    class Meta:
        model = Oposicion_Donacion
        fields = ['manifestacion_oposicion', 'fecha_suscripcion_documento']
        labels = {
            'manifestacion_oposicion': "¿Se opone a la donación?",
            'fecha_suscripcion_documento': "Fecha de Documento",
        }
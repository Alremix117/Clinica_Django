from django import forms
from .models import Paciente, Voluntad_Anticipada, Oposicion_Donacion, Pais, Discapacidad, Contacto_Servicio_Salud

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
        
#contacto_salud
class FormContactoSalud(forms.ModelForm):
    fecha_hora_inicio_atencion = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Fecha y Hora Inicio Atención"
    )
    fecha_hora_triage = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Fecha y Hora Triage"
    )

    class Meta:
        model = Contacto_Servicio_Salud
        fields = [
            'paciente_UUID',
            'fecha_hora_inicio_atencion',
            'codigo_entidad_prestadora',
            'codigo_modalidad_realizacion_tecnologia_salud',
            'grupo_servicios',
            'entorno_atencion',
            'codigo_via_ingreso_usuario_servicio_salud',
            'codigo_causa_motivo_atencion',
            'fecha_hora_triage',
            'clasificacion_triage',
            'codigo_diagnostico',
            'codigo_enfermedad_huerfana',
            'tipo_diagnostico',
        ]
        labels = {
            'paciente_UUID': 'Paciente',
            'codigo_entidad_prestadora': 'Entidad Prestadora de Salud',
            'codigo_modalidad_realizacion_tecnologia_salud': 'Modalidad de Realización',
            'grupo_servicios': 'Grupo de Servicios',
            'entorno_atencion': 'Entorno de Atención',
            'codigo_via_ingreso_usuario_servicio_salud': 'Vía de Ingreso',
            'codigo_causa_motivo_atencion': 'Motivo de Atención',
            'clasificacion_triage': 'Clasificación Triage',
            'codigo_diagnostico': 'Código Diagnóstico',
            'codigo_enfermedad_huerfana': 'Enfermedad Huérfana',
            'tipo_diagnostico': 'Tipo de Diagnóstico',
        }

        widgets = {
            'grupo_servicios': forms.Select(attrs={'class': 'form-control'}),
            'entorno_atencion': forms.Select(attrs={'class': 'form-control'}),
            'clasificacion_triage': forms.Select(attrs={'class': 'form-control'}),
            'tipo_diagnostico': forms.Select(attrs={'class': 'form-control'}),
        }
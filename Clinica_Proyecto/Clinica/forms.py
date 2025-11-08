from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import Paciente, Paciente_Pais, Paciente_Discapacidad

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "numero_documento", "primer_nombre", "segundo_nombre",
            "primer_apellido", "segundo_apellido",
            "fecha_nacimiento", "sexo_biologico", "identidad_genero",
            "zona_territorial_residencia",
            "tipo_documento", "residencia", "ocupacion",
            "etnia", "comunidad_Etnica", "entidad_prestadora_salud",
        ]
        widgets = {
            "fecha_nacimiento": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar placeholders y ordenar combos por nombre
        if "tipo_documento" in self.fields:
            self.fields["tipo_documento"].empty_label = "Seleccione tipo documento"
            self.fields["tipo_documento"].queryset = self.fields["tipo_documento"].queryset.order_by("nombre_tipo_documento")
        if "residencia" in self.fields:
            self.fields["residencia"].empty_label = "Seleccione municipio"
            self.fields["residencia"].queryset = self.fields["residencia"].queryset.order_by("nombre_municipio")
        if "ocupacion" in self.fields:
            self.fields["ocupacion"].empty_label = "Seleccione ocupación"
            self.fields["ocupacion"].queryset = self.fields["ocupacion"].queryset.order_by("nombre_ocupacion")
        if "etnia" in self.fields:
            self.fields["etnia"].empty_label = "Seleccione etnia"
            self.fields["etnia"].queryset = self.fields["etnia"].queryset.order_by("nombre_etnia")
        if "comunidad_Etnica" in self.fields:
            self.fields["comunidad_Etnica"].empty_label = "—"
            self.fields["comunidad_Etnica"].queryset = self.fields["comunidad_Etnica"].queryset.order_by("nombre_comunidad_etnica")
        if "entidad_prestadora_salud" in self.fields:
            self.fields["entidad_prestadora_salud"].empty_label = "Seleccione entidad prestadora"
            self.fields["entidad_prestadora_salud"].queryset = self.fields["entidad_prestadora_salud"].queryset.order_by("nombre_entidad_prestadora")

    def clean(self):
        cleaned = super().clean()
        # Aquí podrías validar coherencias adicionales si aplica
        return cleaned
    
# --- Form del through Paciente_Pais ---
class PacientePaisForm(forms.ModelForm):
    class Meta:
        model = Paciente_Pais
        fields = ["codigo_pais"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar por nombre y etiqueta amigable
        self.fields["codigo_pais"].queryset = self.fields["codigo_pais"].queryset.order_by("nombre_pais")
        self.fields["codigo_pais"].empty_label = "Seleccione país"

# --- Form del through Paciente_Discapacidad ---
class PacienteDiscapacidadForm(forms.ModelForm):
    class Meta:
        model = Paciente_Discapacidad
        fields = ["id_discapacidad"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["id_discapacidad"].queryset = self.fields["id_discapacidad"].queryset.order_by("nombre_discapacidad")
        self.fields["id_discapacidad"].empty_label = "Seleccione discapacidad"

PacientePaisFormSet = inlineformset_factory(
    parent_model=Paciente,
    model=Paciente_Pais,
    form=PacientePaisForm,
    fields=["codigo_pais"],
    extra=1,            # cuántas filas vacías mostrar por defecto
    can_delete=True,    # permite borrar filas existentes
)

PacienteDiscapacidadFormSet = inlineformset_factory(
    parent_model=Paciente,
    model=Paciente_Discapacidad,
    form=PacienteDiscapacidadForm,
    fields=["id_discapacidad"],
    extra=1,
    can_delete=True,
)
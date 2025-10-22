# FILE: Clinica_Proyecto/Clinica/admin.py

from django.contrib import admin
from .models import (
    Paciente, Pais, Municipio, Ocupacion, Etnia, Discapacidad,
    # El resto de modelos se dejan sin registrar, a menos que se definan después
)


class PacienteAdmin(admin.ModelAdmin):
    list_display = ('identificacion', 'primer_nombre', 'primer_apellido', 'nacionalidad', 'residencia')
    list_filter = ('nacionalidad', 'etnia', 'ocupacion')
    search_fields = ('identificacion', 'primer_nombre', 'primer_apellido')
    filter_horizontal = ('discapacidades',)


admin.site.register(Paciente, PacienteAdmin)


admin.site.register(Pais)
admin.site.register(Municipio)
admin.site.register(Ocupacion)
admin.site.register(Etnia)
admin.site.register(Discapacidad)


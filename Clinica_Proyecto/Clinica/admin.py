from django.contrib import admin
from .models import (
    Comunidad_Etnica,
    Contacto_Servicio_Salud,
    Diagnostico,
    Discapacidad,
    Entidad_Prestadora_Salud,
    Enfermedad_Huerfana,
    Etnia,
    Modalidad_Realizacion_Tecnologia_Salud,
    Motivo_Atencion,
    Municipio,
    Ocupacion,
    Oposicion_Donacion,
    Paciente,
    Paciente_Discapacidad,
    Paciente_Pais,
    Pais,
    Tipo_documento,
    Via_Ingreso_Servicio_Salud,
    Voluntad_Anticipada,
)

# ============================================================================
# BASIC REFERENCE MODELS
# ============================================================================


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ("codigo_pais", "nombre_pais")
    search_fields = ("codigo_pais", "nombre_pais")
    ordering = ("codigo_pais",)


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ("codigo_municipio", "nombre_municipio")
    search_fields = ("codigo_municipio", "nombre_municipio")
    ordering = ("nombre_municipio",)


@admin.register(Ocupacion)
class OcupacionAdmin(admin.ModelAdmin):
    list_display = ("codigo_ocupacion", "nombre_ocupacion")
    search_fields = ("codigo_ocupacion", "nombre_ocupacion")


@admin.register(Etnia)
class EtniaAdmin(admin.ModelAdmin):
    list_display = ("identificador_etnia", "nombre_etnia")
    search_fields = ("identificador_etnia", "nombre_etnia")


@admin.register(Comunidad_Etnica)
class ComunidadEtnicaAdmin(admin.ModelAdmin):
    list_display = ("codigo_comunidad_etnica", "nombre_comunidad_etnica")
    search_fields = ("codigo_comunidad_etnica", "nombre_comunidad_etnica")


@admin.register(Discapacidad)
class DiscapacidadAdmin(admin.ModelAdmin):
    list_display = ("id_discapacidad", "nombre_discapacidad")
    search_fields = ("id_discapacidad", "nombre_discapacidad")


@admin.register(Tipo_documento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ("codigo_tipo_documento", "nombre_tipo_documento")
    search_fields = ("codigo_tipo_documento", "nombre_tipo_documento")


@admin.register(Entidad_Prestadora_Salud)
class EntidadPrestadoraSaludAdmin(admin.ModelAdmin):
    list_display = (
        "codigo_entidad_prestadora",
        "nombre_entidad_prestadora",
        "es_eps",
        "es_ips",
        "es_arl",
        "es_aseguradora",
    )
    search_fields = ("codigo_entidad_prestadora", "nombre_entidad_prestadora")
    list_filter = ("es_eps", "es_ips", "es_arl", "es_aseguradora")

# ============================================================================
# REFERENCE CATALOGS
# ============================================================================

@admin.register(Modalidad_Realizacion_Tecnologia_Salud)
class ModalidadRealizacionAdmin(admin.ModelAdmin):
    list_display = (
        "codigo_modalidad_realizacion_tecnologia_salud",
        "nombre_modalidad_realizacion_tecnologia_salud",
    )
    search_fields = (
        "codigo_modalidad_realizacion_tecnologia_salud",
        "nombre_modalidad_realizacion_tecnologia_salud",
    )

@admin.register(Via_Ingreso_Servicio_Salud)
class ViaIngresoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo_via_ingreso_usuario_servicio_salud",
        "nombre_via_ingreso_usuario_servicio_salud",
    )
    search_fields = (
        "codigo_via_ingreso_usuario_servicio_salud",
        "nombre_via_ingreso_usuario_servicio_salud",
    )

@admin.register(Motivo_Atencion)
class MotivoAtencionAdmin(admin.ModelAdmin):
    list_display = ("codigo_causa_motivo_atencion", "nombre_causa_motivo_atencion")
    search_fields = ("codigo_causa_motivo_atencion", "nombre_causa_motivo_atencion")

@admin.register(Enfermedad_Huerfana)
class EnfermedadHuerfanaAdmin(admin.ModelAdmin):
    list_display = ("codigo_enfermedad_huerfana", "nombre_enfermedad_huerfana")
    search_fields = ("codigo_enfermedad_huerfana", "nombre_enfermedad_huerfana")

@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ("codigo_diagnostico", "nombre_diagnostico")
    search_fields = ("codigo_diagnostico", "nombre_diagnostico")






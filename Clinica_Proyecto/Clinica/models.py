from django.db import models
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator
)
import uuid


# ===========================================================
#           TABLAS MAESTRAS / CATÁLOGOS
# ===========================================================

class Pais(models.Model):
    codigo_iso = models.CharField(
        max_length=3,
        unique=True,
        validators=[
            MinLengthValidator(3),
            RegexValidator(r'^[A-Za-z0-9]{3}$', "El código ISO debe tener 3 caracteres alfanuméricos.")
        ],
        verbose_name="Código ISO 3"
    )
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del País")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ["nombre"]


class Municipio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Municipio")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        ordering = ["nombre"]


class Ocupacion(models.Model):
    nombre = models.CharField(max_length=150, unique=True, verbose_name="Nombre de la Ocupación")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Ocupación"
        verbose_name_plural = "Ocupaciones"
        ordering = ["nombre"]


class Etnia(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Etnia")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Etnia"
        verbose_name_plural = "Etnias"
        ordering = ["nombre"]


class Comunidad_Etnica(models.Model):
    codigo_comunidad_etnica = models.CharField(
        primary_key=True,
        max_length=3,
        validators=[
            MinLengthValidator(3),
            RegexValidator(r'^[A-Za-z0-9]{3}$', "El código debe tener 3 caracteres alfanuméricos."),
        ],
        verbose_name="Código de Comunidad Étnica"
    )
    nombre_comunidad_etnica = models.CharField(max_length=150, verbose_name="Nombre Comunidad Étnica")

    def __str__(self):
        return self.nombre_comunidad_etnica

    class Meta:
        verbose_name = "Comunidad Étnica"
        verbose_name_plural = "Comunidades Étnicas"
        ordering = ["codigo_comunidad_etnica"]


class Discapacidad(models.Model):
    id_discapacidad = models.CharField(
        primary_key=True,
        max_length=2,
        validators=[
            MinLengthValidator(2),
            RegexValidator(r'^[0-9]{2}$', "El código debe tener 2 dígitos numéricos.")
        ],
        verbose_name="Código de Discapacidad"
    )
    nombre_discapacidad = models.CharField(max_length=150, unique=True, verbose_name="Tipo de Discapacidad")

    def __str__(self):
        return f"{self.id_discapacidad} - {self.nombre_discapacidad}"

    class Meta:
        verbose_name = "Discapacidad"
        verbose_name_plural = "Discapacidades"
        ordering = ["id_discapacidad"]


# ===========================================================
#                   TABLA PACIENTE
# ===========================================================

class Paciente(models.Model):
    paciente_UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TIPO_DOC_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
    ]
    tipo_documento = models.CharField(max_length=5, choices=TIPO_DOC_CHOICES, verbose_name="Tipo de Documento")
    identificacion = models.CharField(max_length=20, unique=True, verbose_name="Nro. Identificación")
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100, blank=True, null=True)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")

    nacionalidad = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, verbose_name="País de Nacimiento")
    residencia = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, verbose_name="Municipio de Residencia")
    ocupacion = models.ForeignKey(Ocupacion, on_delete=models.SET_NULL, null=True)
    etnia = models.ForeignKey(Etnia, on_delete=models.SET_NULL, null=True, verbose_name="Pertenencia Étnica")

    discapacidades = models.ManyToManyField(Discapacidad, through='Paciente_Discapacidad', blank=True)

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} ({self.identificacion})"

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ["primer_apellido", "primer_nombre"]


# ===========================================================
#            RELACIÓN PACIENTE - DISCAPACIDAD
# ===========================================================

class Paciente_Discapacidad(models.Model):
    id_discapacidad = models.ForeignKey(Discapacidad, on_delete=models.CASCADE)
    paciente_UUID = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_discapacidad', 'paciente_UUID')
        verbose_name = "Paciente Discapacidad"
        verbose_name_plural = "Pacientes Discapacidades"
        ordering = ["paciente_UUID"]


# ===========================================================
#            OPOSICIÓN A DONACIÓN
# ===========================================================

class Oposicion_Donacion(models.Model):
    id_oposicion = models.AutoField(primary_key=True)
    paciente_UUID = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    manifestacion_oposicion = models.CharField(
        max_length=2,
        validators=[RegexValidator(r'^(01|02)$', "Debe ser 01 (Sí) o 02 (No).")],
        verbose_name="Manifestación de Oposición"
    )
    fecha_suscripcion_documento = models.DateField(verbose_name="Fecha de Suscripción del Documento")

    class Meta:
        verbose_name = "Oposición a Donación"
        verbose_name_plural = "Oposiciones a Donación"
        ordering = ["id_oposicion"]


# ===========================================================
#            PACIENTE NACIONALIDAD (PAIS)
# ===========================================================

class Paciente_Pais(models.Model):
    paciente_UUID = models.ForeignKey(Paciente, on_delete=models.CASCADE, primary_key=True)
    codigo_pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('paciente_UUID', 'codigo_pais')
        verbose_name = "Paciente País"
        verbose_name_plural = "Pacientes Países"
        ordering = ["paciente_UUID"]


# ===========================================================
#            ENTIDADES PRESTADORAS DE SALUD
# ===========================================================

class Entidad_Prestadora_Salud(models.Model):
    codigo_entidad_prestadora = models.CharField(
        primary_key=True,
        max_length=12,
        validators=[RegexValidator(r'^[A-Za-z0-9]{12}$')],
        verbose_name="Código Entidad Prestadora"
    )
    nombre_entidad_prestadora = models.CharField(max_length=200, verbose_name="Nombre Entidad Prestadora")

    def __str__(self):
        return self.nombre_entidad_prestadora

    class Meta:
        verbose_name = "Entidad Prestadora de Salud"
        verbose_name_plural = "Entidades Prestadoras de Salud"
        ordering = ["codigo_entidad_prestadora"]


# ===========================================================
#            VOLUNTAD ANTICIPADA
# ===========================================================

class Voluntad_Anticipada(models.Model):
    id_voluntad = models.AutoField(primary_key=True)
    paciente_UUID = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    documento_voluntad_anticipada = models.CharField(
        max_length=2,
        validators=[RegexValidator(r'^(01|02)$')],
        verbose_name="Documento Voluntad Anticipada"
    )
    fecha_suscripcion_documento = models.DateField(verbose_name="Fecha de Suscripción del Documento")
    codigo_entidad_prestadora = models.ForeignKey(
        Entidad_Prestadora_Salud, on_delete=models.CASCADE, verbose_name="Entidad Prestadora"
    )

    class Meta:
        verbose_name = "Voluntad Anticipada"
        verbose_name_plural = "Voluntades Anticipadas"
        ordering = ["id_voluntad"]


# ===========================================================
#          CATÁLOGOS COMPLEMENTARIOS DE SERVICIOS
# ===========================================================

class Modalidad_Realizacion_Tecnologia_Salud(models.Model):
    codigo_modalidad_realizacion_tecnologia_salud = models.CharField(
        primary_key=True,
        max_length=2,
        validators=[RegexValidator(r'^[A-Za-z0-9]{2}$')],
        verbose_name="Código Modalidad Realización Tecnología en Salud"
    )
    nombre_modalidad_realizacion_tecnologia_salud = models.CharField(
        max_length=200, verbose_name="Nombre Modalidad Realización Tecnología en Salud"
    )

    def __str__(self):
        return self.nombre_modalidad_realizacion_tecnologia_salud

    class Meta:
        verbose_name = "Modalidad de Realización de Tecnología en Salud"
        verbose_name_plural = "Modalidades de Realización de Tecnología en Salud"
        ordering = ["codigo_modalidad_realizacion_tecnologia_salud"]


class Via_Ingreso_Servicio_Salud(models.Model):
    codigo_via_ingreso_usuario_servicio_salud = models.CharField(
        primary_key=True,
        max_length=2,
        validators=[RegexValidator(r'^[A-Za-z0-9]{2}$')],
        verbose_name="Código Vía de Ingreso"
    )
    nombre_via_ingreso_usuario_servicio_salud = models.CharField(max_length=200, verbose_name="Nombre Vía de Ingreso")

    def __str__(self):
        return self.nombre_via_ingreso_usuario_servicio_salud

    class Meta:
        verbose_name = "Vía de Ingreso al Servicio de Salud"
        verbose_name_plural = "Vías de Ingreso al Servicio de Salud"
        ordering = ["codigo_via_ingreso_usuario_servicio_salud"]


class Motivo_Atencion(models.Model):
    codigo_causa_motivo_atencion = models.CharField(
        primary_key=True,
        max_length=2,
        validators=[RegexValidator(r'^[A-Za-z0-9]{2}$')],
        verbose_name="Código Causa Motivo de Atención"
    )
    nombre_causa_motivo_atencion = models.CharField(max_length=200, verbose_name="Nombre Causa Motivo Atención")

    def __str__(self):
        return self.nombre_causa_motivo_atencion

    class Meta:
        verbose_name = "Motivo de Atención"
        verbose_name_plural = "Motivos de Atención"
        ordering = ["codigo_causa_motivo_atencion"]


class Enfermedad_Huerfana(models.Model):
    codigo_enfermedad_huerfana = models.CharField(
        primary_key=True,
        max_length=4,
        validators=[RegexValidator(r'^[A-Za-z0-9]{4}$')],
        verbose_name="Código Enfermedad Huérfana"
    )
    nombre_enfermedad_huerfana = models.CharField(max_length=200, verbose_name="Nombre Enfermedad Huérfana")

    def __str__(self):
        return self.nombre_enfermedad_huerfana

    class Meta:
        verbose_name = "Enfermedad Huérfana"
        verbose_name_plural = "Enfermedades Huérfanas"
        ordering = ["codigo_enfermedad_huerfana"]


class Diagnostico(models.Model):
    codigo_diagnostico = models.CharField(
        primary_key=True,
        max_length=4,
        validators=[RegexValidator(r'^[A-Za-z0-9]{4}$')],
        verbose_name="Código Diagnóstico"
    )
    nombre_diagnostico = models.CharField(max_length=200, verbose_name="Nombre del Diagnóstico")
    codigo_enfermedad_huerfana = models.ForeignKey(
        Enfermedad_Huerfana, on_delete=models.SET_NULL, null=True, verbose_name="Enfermedad Huérfana"
    )

    def __str__(self):
        return self.nombre_diagnostico

    class Meta:
        verbose_name = "Diagnóstico"
        verbose_name_plural = "Diagnósticos"
        ordering = ["codigo_diagnostico"]


# ===========================================================
#          CONTACTO SERVICIO DE SALUD
# ===========================================================

class Contacto_Servicio_Salud(models.Model):
    id_contacto_UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paciente_UUID = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_hora_inicio_atencion = models.DateTimeField(verbose_name="Fecha y Hora Inicio Atención")
    codigo_entidad_prestadora = models.ForeignKey(Entidad_Prestadora_Salud, on_delete=models.CASCADE)
    codigo_modalidad_realizacion_tecnologia_salud = models.ForeignKey(
        Modalidad_Realizacion_Tecnologia_Salud, on_delete=models.CASCADE
    )
    grupo_servicios = models.CharField(max_length=2, validators=[RegexValidator(r'^[A-Za-z0-9]{2}$')])
    entorno_atencion = models.CharField(max_length=2, validators=[RegexValidator(r'^[A-Za-z0-9]{2}$')])
    codigo_via_ingreso_usuario_servicio_salud = models.ForeignKey(
        Via_Ingreso_Servicio_Salud, on_delete=models.CASCADE
    )
    codigo_causa_motivo_atencion = models.ForeignKey(Motivo_Atencion, on_delete=models.CASCADE)
    fecha_hora_triage = models.DateTimeField(verbose_name="Fecha y Hora Triage")
    clasificacion_triage = models.CharField(max_length=2, validators=[RegexValidator(r'^[A-Za-z0-9]{2}$')])
    codigo_diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE)
    codigo_enfermedad_huerfana = models.ForeignKey(Enfermedad_Huerfana, on_delete=models.SET_NULL, null=True)
    tipo_diagnostico = models.CharField(max_length=2, validators=[RegexValidator(r'^[A-Za-z0-9]{2}$')])

    class Meta:
        verbose_name = "Contacto Servicio de Salud"
        verbose_name_plural = "Contactos Servicios de Salud"
        ordering = ["fecha_hora_inicio_atencion"]

from django.db import models
from django.core.validators import (
    MinLengthValidator,
    RegexValidator
)
import uuid

class Pais(models.Model):
    codigo_pais = models.CharField(
        primary_key=True,
        max_length=3,
        unique=True,
        validators=[
            MinLengthValidator(3),
            RegexValidator(
                regex='^[A-Za-z0-9]{3}$',
                message='El código ISO debe contener caracteres alfanuméricos.'
            )
        ],
        verbose_name="Código ISO 3166-1 del País"
    )
    nombre_pais = models.CharField(
        max_length=200, 
        unique=True,
        validators=[
            MinLengthValidator(3),
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 ]+$',
                message='El nombre del país debe contener solo caracteres alfanuméricos y espacios.'
            )
        ],  
        verbose_name="Nombre del País"
    )

    def __str__(self):
        return self.nombre_pais

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Paises"
        ordering = ["nombre_pais"]

class Municipio(models.Model):
    codigo_municipio = models.CharField(
        primary_key=True,
        max_length=5,
        unique=True,
        validators=[
            MinLengthValidator(5),
            RegexValidator(
                regex='^[A-Za-z0-9]{5}$',
                message='El código debe contener caracteres alfanuméricos.'
            )
        ],
        verbose_name="Código municipio DIVIPOLA del DANE"
    )
    nombre_municipio = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(3),
            # Expresion regular para validar que sean solo caracteres alfanumericos con espacios
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 ]+$',
                message='El nombre del país debe contener solo caracteres alfanuméricos y espacios.'
            )
        ],  
        verbose_name="Nombre del municipio"
    )

    def __str__(self):
        return self.nombre_municipio

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        ordering = ["nombre_municipio"]

class Ocupacion(models.Model):
    codigo_ocupacion = models.CharField(
        primary_key=True,
        max_length=4,
        unique=True,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex='^[A-Za-z0-9]{4}$',
                message='El código debe contener caracteres alfanuméricos.'
            )
        ],
        verbose_name="Código Catálogo CIUO-88A.C de ocupación"
    )
    nombre_ocupacion = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(3),
            # Expresion regular para validar que sean solo caracteres alfanumericos con espacios
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 ]+$',
                message='El nombre de la ocupación debe contener solo caracteres alfanuméricos y espacios.'
            )
        ],  
        verbose_name="Nombre de la ocupación"
    )

    def __str__(self):
        return self.nombre_ocupacion

    class Meta:
        verbose_name = "Ocupación"
        verbose_name_plural = "Ocupaciones"
        ordering = ["nombre_ocupacion"]

class Etnia(models.Model):
    identificador_etnia = models.CharField(
        primary_key=True,
        max_length=2,
        unique=True,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex='^[A-Za-z0-9]{2}$',
                message='El identificador debe contener caracteres alfanuméricos.'
            )
        ],
        verbose_name="Identificador de la etnia"
    )
    nombre_etnia = models.CharField(
        max_length=200, 
        unique=True,
        validators=[
            MinLengthValidator(3),
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 ]+$',
                message='El nombre de la etnia debe contener solo caracteres alfanuméricos y espacios.'
            )
        ],  
        verbose_name="Nombre de la etnia"
    )

    def __str__(self):
        return f"{self.identificador_etnia} - {self.nombre_etnia}"

    class Meta:
        verbose_name = "Etnia"
        verbose_name_plural = "Etnias"
        ordering = ["identificador_etnia"]

class Comunidad_Etnica(models.Model):
    codigo_comunidad_etnica = models.CharField(
        primary_key=True,
        max_length=3,
        unique=True,
        validators=[
            MinLengthValidator(3),
            RegexValidator(
                regex='^[A-Za-z0-9]{3}$',
                message='El código debe contener caracteres alfanuméricos.'
            )
        ],
        verbose_name="Código de la Comunidad Étnica"
    )
    nombre_comunidad_etnica = models.CharField(
        max_length=200, 
        unique=True,
        validators=[
            MinLengthValidator(3),
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 ]+$',
                message='El nombre de la comunidad debe contener solo caracteres alfanuméricos y espacios.'
            )
        ],  
        verbose_name="Nombre de la comunidad étnica"
    )

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
        unique=True,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex='^[A-Za-z0-9]{2}$',
                message='El identificador debe contener caracteres alfanuméricos.'
            )
        ],
        verbose_name="IIdentificador de la Discapacidad"
    )
    nombre_discapacidad = models.CharField(
        max_length=200, 
        unique=True,
        validators=[
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 ]+$',
                message='El nombre de la discapacidadd debe contener solo caracteres alfanuméricos y espacios.'
            )
        ],  
        verbose_name="Nombre de la discapacidad"
    )

    def __str__(self):
        return f"{self.id_discapacidad} - {self.nombre_discapacidad}"

    class Meta:
        verbose_name = "Discapacidad"
        verbose_name_plural = "Discapacidades"
        ordering = ["id_discapacidad"]

class Tipo_documento(models.Model):
    codigo_tipo_documento = models.CharField(
        primary_key=True,
        max_length=2,
        unique=True,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex='^[A-Za-z0-9]{2}$',
                message='El código debe contener caracteres alfanuméricos.'
            )
        ],
        verbose_name="Código Tipo de Documento"
    )
    nombre_tipo_documento = models.CharField(
        max_length=200, 
        unique=True,
        validators=[
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 ]+$',
                message='El nombre del tipo de documento debe contener solo caracteres alfanuméricos y espacios.'
            )
        ],  
        verbose_name="Nombre del Tipo de Documento"
    )

    def __str__(self):
        return f'{self.codigo_tipo_documento} - {self.nombre_tipo_documento}'

    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"
        ordering = ["codigo_tipo_documento"]

class Entidad_Prestadora_Salud(models.Model):
    codigo_entidad_prestadora = models.CharField(
        primary_key=True,
        max_length=6,
        unique=True,
        validators=[
            MinLengthValidator(6),
            RegexValidator(
                regex='^[A-Za-z0-9]{6}$',
                message='El código debe contener caracteres alfanuméricos.'
            )
        ],
        verbose_name="Codigo Entidad Prestadora de Salud SGSSS"
    )
    nombre_entidad_prestadora = models.CharField(
        max_length=200, 
        validators=[
            MinLengthValidator(3),
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 ]+$',
                message='El nombre de la entidadd prestadora debe contener solo caracteres alfanuméricos y espacios.'
            )
        ],
        verbose_name="Nombre Entidad Prestadora"
    )
    es_eps = models.CharField(verbose_name="¿Es EPS?", max_length=2, choices=[('01', 'Sí'), ('02', 'No')])
    es_ips = models.CharField(verbose_name="¿Es IPS?", max_length=2, choices=[('01', 'Sí'), ('02', 'No')])
    es_arl = models.CharField(verbose_name="¿Es ARL?", max_length=2, choices=[('01', 'Sí'), ('02', 'No')])
    es_aseguradora = models.CharField(verbose_name="¿Es ASEGURADORA?", max_length=2, choices=[('01', 'Sí'), ('02', 'No')])

    def __str__(self):
        return self.nombre_entidad_prestadora

    class Meta:
        verbose_name = "Entidad Prestadora de Salud"
        verbose_name_plural = "Entidades Prestadoras de Salud"
        ordering = ["codigo_entidad_prestadora"]

class Paciente(models.Model):
    SEXO_BIOLOGICO_CHOICES = [('01', 'Hombre'), ('02', 'Mujer'), ('O3', 'Indeterminad/Intersexual')]
    IDENTIDAD_GENERO_CHOICES = [('01', 'Masculino'), ('02', 'Femenino'), ('03', 'Transgénero'), ('04', 'Neutro'), ('05', 'No lo declara')]
    ZONA_TERRITORIAL_RESIDENCIAL_CHOICES = [('01', 'Urbana'), ('02', 'Rural')]
    paciente_UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero_documento = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            MinLengthValidator(3),
            RegexValidator(
                regex='^[A-Za-z0-9]{3,20}$',
                message='El número de documento debe contener caracteres alfanuméricos.'
            )
        ],
        verbose_name="Número de Documento"
    )
    primer_nombre = models.CharField(
        max_length=60, 
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9]+$',
                message='El primer nombre debe contener solo caracteres alfanuméricos'
            )
        ],  
        verbose_name="Primer Nombre"
    )
    segundo_nombre = models.CharField(
        max_length=60, 
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9]+$',
                message='El primer nombre debe contener solo caracteres alfanuméricos'
            )
        ],  
        verbose_name="Segundo Nombre"
    )
    primer_apellido = models.CharField(
        max_length=60,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9]+$',
                message='El primer nombre debe contener solo caracteres alfanuméricos'
            )
        ],  
        verbose_name="Primer Apellido"
    )
    segundo_apellido = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9]+$',
                message='El primer nombre debe contener solo caracteres alfanuméricos'
            )
        ],  
        verbose_name="Segundo Apellido"
    )
    #fecha de nacimiento con formato YYYY-MM-DD HH:MM
    fecha_nacimiento = models.DateTimeField(verbose_name="Fecha de Nacimiento")
    sexo_biologico = models.CharField(max_length=2, choices=SEXO_BIOLOGICO_CHOICES, verbose_name="Sexo Biológico")
    identidad_genero = models.CharField(max_length=2, choices=IDENTIDAD_GENERO_CHOICES, verbose_name="Identidad de Género")
    zona_territorial_residencia = models.CharField(max_length=2, choices=ZONA_TERRITORIAL_RESIDENCIAL_CHOICES, verbose_name="Zona Territorial de Residencia")

    tipo_documento = models.ForeignKey(Tipo_documento, on_delete=models.SET_NULL, null=True, verbose_name="Código Tipo de Documento")
    residencia = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, verbose_name="Código Municipio de Residencia")
    ocupacion = models.ForeignKey(Ocupacion, on_delete=models.SET_NULL, null=True, verbose_name="Código Ocupación")
    etnia = models.ForeignKey(Etnia, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Código Étnia")
    comunidad_Etnica = models.ForeignKey(Comunidad_Etnica, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Código Comunidad Étnica")
    entidad_prestadora_salud = models.ForeignKey(Entidad_Prestadora_Salud, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Código Entidad Prestadora de Salud")


    nacionalidad = models.ManyToManyField(Pais, through='Paciente_Pais', related_name='pacientes', blank=True)
    discapacidades = models.ManyToManyField(Discapacidad, through='Paciente_Discapacidad', related_name='pacientes', blank=True)

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} ({self.numero_documento})"

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ["primer_apellido", "primer_nombre"]

class Paciente_Discapacidad(models.Model):
    id_discapacidad = models.ForeignKey(Discapacidad, on_delete=models.CASCADE, related_name='pacientes_rel')
    paciente_UUID = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='discapacidades_rel')

    def __str__(self):
        return f"Discapacidad {self.id_discapacidad} del Paciente {self.paciente_UUID}"
    
    class Meta:
        unique_together = ('id_discapacidad', 'paciente_UUID')
        verbose_name = "Paciente Discapacidad"
        verbose_name_plural = "Pacientes Discapacidades"
        ordering = ["paciente_UUID"]

class Oposicion_Donacion(models.Model):
    MANIFESTACION_OPOSICION_CHOICES = [('01', 'Sí'), ('02', 'No')]
    id_oposicion = models.AutoField(primary_key=True)
    paciente_UUID = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    manifestacion_oposicion = models.CharField(
        max_length=2,
        choices=MANIFESTACION_OPOSICION_CHOICES,
        verbose_name="Manifestación de Oposición"
    )
    fecha_suscripcion_documento = models.DateField(verbose_name="Fecha de Suscripción del Documento,", null=True, blank=True)

    def __str__(self):
        return f"Oposición Donación Paciente {self.paciente_UUID}"
    
    class Meta:
        verbose_name = "Oposición a Donación"
        verbose_name_plural = "Oposiciones a Donación"
        ordering = ["id_oposicion"]

class Paciente_Pais(models.Model):
    paciente_UUID = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='paises_rel')
    codigo_pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='pacientes_rel')
    
    def __str__(self):
        return f"País {self.codigo_pais} del Paciente {self.paciente_UUID}"
    
    class Meta:
        unique_together = ('paciente_UUID', 'codigo_pais')
        verbose_name = "Paciente País"
        verbose_name_plural = "Pacientes Países"
        ordering = ["paciente_UUID"]

class Voluntad_Anticipada(models.Model):
    DOCUMENTO_VOLUNTAD_ANTICIPADA_CHOICES = [('01', 'Sí'), ('02', 'No')]
    id_voluntad = models.AutoField(primary_key=True)
    paciente_UUID = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    documento_voluntad_anticipada = models.CharField(
        max_length=2,
        choices=DOCUMENTO_VOLUNTAD_ANTICIPADA_CHOICES,
        verbose_name="Documento Voluntad Anticipada"
    )
    fecha_suscripcion_documento = models.DateField(verbose_name="Fecha de Suscripción del Documento", null=True, blank=True)
    codigo_entidad_prestadora = models.ForeignKey(
        Entidad_Prestadora_Salud, on_delete=models.CASCADE, verbose_name="Entidad Prestadora"
    )

    def __str__(self):
        return f"Voluntad Anticipada Paciente {self.paciente_UUID}"

    class Meta:
        verbose_name = "Voluntad Anticipada"
        verbose_name_plural = "Voluntades Anticipadas"
        ordering = ["id_voluntad"]

class Modalidad_Realizacion_Tecnologia_Salud(models.Model):
    codigo_modalidad_realizacion_tecnologia_salud = models.CharField(
        primary_key=True,
        max_length=2,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex='^[A-Za-z0-9]{2}$',
                message='El código debe contener caracteres alfanuméricos.'
            )
        ],
        verbose_name="Código de Modalidad de Realización de la Tecnología en Salud"
    )
    nombre_modalidad_realizacion_tecnologia_salud = models.CharField(
        max_length=200, 
        validators=[
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 ]+$',
                message='El nombre de la modalidad debe contener solo caracteres alfanuméricos y espacios.'
            )
        ],
        verbose_name="Nombre Modalidad Realización Tecnología en Salud"
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
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex='^[A-Za-z0-9]{2}$',
                message='El código debe contener caracteres alfanuméricos.'
            )
        ],
        verbose_name="Código Vía de Ingreso"
    )
    nombre_via_ingreso_usuario_servicio_salud = models.CharField(
        max_length=200,
        validators=[
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 ]+$',
                message='El nombre de la via de ingreso debe contener solo caracteres alfanuméricos y espacios.'
            )
        ],
        verbose_name="Nombre Vía de Ingreso")

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
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex='^[A-Za-z0-9]{2}$',
                message='El código debe contener caracteres alfanuméricos.'
            )
        ],
        verbose_name="Código Causa Motivo de Atención"
    )
    nombre_causa_motivo_atencion = models.CharField(
        max_length=200,
        validators=[
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 ]+$',
                message='El nombre de la causa del motivo de atención debe contener solo caracteres alfanuméricos y espacios.'
            )
        ],
        verbose_name="Nombre de la Causa del Motivo de Atención")

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
        validators=[
            MinLengthValidator(1),
            RegexValidator(
                regex='^[A-Za-z0-9]{1,4}$',
                message='El código debe contener caracteres alfanuméricos.'
            )
        ],
        verbose_name="Código Enfermedad Huérfana"
    )
    nombre_enfermedad_huerfana = models.CharField(
        max_length=200,
        validators=[
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 ]+$',
                message='El nombre de la enfermedad huerfana debe contener solo caracteres alfanuméricos y espacios.'
            )
        ],
        verbose_name="Nombre Enfermedad Huérfana"
    )

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
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex='^[A-Za-z0-9]{4}$',
                message='El código debe contener caracteres alfanuméricos.'
            )
        ],
        verbose_name="Código del Diagnóstico"
    )
    nombre_diagnostico = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(3),
            RegexValidator(
                regex='^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 ]+$',
                message='El nombre de la enfermedad huerfana debe contener solo caracteres alfanuméricos y espacios.'
            )
        ],
        verbose_name="Nombre del Diagnóstico")

    def __str__(self):
        return self.nombre_diagnostico

    class Meta:
        verbose_name = "Diagnóstico"
        verbose_name_plural = "Diagnósticos"
        ordering = ["codigo_diagnostico"]

class Contacto_Servicio_Salud(models.Model):
    GRUPO_SERVICIOS_CHOICES = [
        ('01', 'Consulta Externa'),
        ('02', 'Apoyo diagnóstico y complementación terapéutica'),
        ('03', 'Internación'),
        ('04', 'Quirúrgico'),
        ('05', 'Atención Inmediata')
    ]
    ENTORNO_ATENCION_CHOICES = [
        ('01', 'Hogar'),
        ('02', 'Comunitario'),
        ('03', 'Escolar'),
        ('04', 'Laborall'),
        ('05', 'Institucional'),
    ]
    CLASIFIACION_TRIAGE_CHOICES = [
        ('01', 'Triage I'),
        ('02', 'Triage II'),
        ('03', 'Triage III'),
        ('04', 'Triage IV'),
        ('05', 'Triage V'),
    ]
    TIPO_DIAGNOSTICO_CHOICES = [
        ('01', 'Impresión diagnóstica'),
        ('02', 'Coonfirmado nuevo'),
        ('03', 'Confirmado repetido'),
    ]
    id_contacto_UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paciente_UUID = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_hora_inicio_atencion = models.DateTimeField(verbose_name="Fecha y Hora Inicio Atención")
    codigo_entidad_prestadora = models.ForeignKey(Entidad_Prestadora_Salud, on_delete=models.CASCADE, verbose_name="Entidad Prestadora de Salud")
    codigo_modalidad_realizacion_tecnologia_salud = models.ForeignKey(
        Modalidad_Realizacion_Tecnologia_Salud, on_delete=models.CASCADE, verbose_name="Modalidad de Realización de Tecnología en Salud"
    )
    grupo_servicios = models.CharField(max_length=2, choices=GRUPO_SERVICIOS_CHOICES, verbose_name="Grupo de Servicios")
    entorno_atencion = models.CharField(max_length=2, choices=ENTORNO_ATENCION_CHOICES, verbose_name="Entorno de Atención")
    codigo_via_ingreso_usuario_servicio_salud = models.ForeignKey(
        Via_Ingreso_Servicio_Salud, on_delete=models.CASCADE
    )
    codigo_causa_motivo_atencion = models.ForeignKey(Motivo_Atencion, on_delete=models.CASCADE)
    fecha_hora_triage = models.DateTimeField(verbose_name="Fecha y Hora Triage")
    clasificacion_triage = models.CharField(max_length=2, choices=CLASIFIACION_TRIAGE_CHOICES, verbose_name="Clasificación Triage")
    codigo_diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE, verbose_name="Código Diagnóstico")
    codigo_enfermedad_huerfana = models.ForeignKey(Enfermedad_Huerfana, on_delete=models.SET_NULL, null=True, verbose_name="Enfermedad Huérfana")
    tipo_diagnostico = models.CharField(max_length=2, choices=TIPO_DIAGNOSTICO_CHOICES, verbose_name="Tipo de Diagnóstico")

    class Meta:
        verbose_name = "Contacto Servicio de Salud"
        verbose_name_plural = "Contactos Servicios de Salud"
        ordering = ["fecha_hora_inicio_atencion"]
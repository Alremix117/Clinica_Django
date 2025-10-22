

from django.db import models


class Pais(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del País")
    codigo_iso = models.CharField(max_length=3, unique=True, verbose_name="Código ISO 3")

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Países"

class Municipio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Municipio")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Municipios"

class Ocupacion(models.Model):
    nombre = models.CharField(max_length=150, unique=True, verbose_name="Nombre de la Ocupación")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Ocupaciones"

class Etnia(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Etnia")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Etnias"

class Discapacidad(models.Model):
    nombre = models.CharField(max_length=150, unique=True, verbose_name="Tipo de Discapacidad")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Discapacidades"
    
class Paciente(models.Model):
    # Datos 
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
    
    # (ForeignKey)
    nacionalidad = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, verbose_name="País de Nacimiento")
    residencia = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, verbose_name="Municipio de Residencia")
    ocupacion = models.ForeignKey(Ocupacion, on_delete=models.SET_NULL, null=True)
    etnia = models.ForeignKey(Etnia, on_delete=models.SET_NULL, null=True, verbose_name="Pertenencia Étnica")
    
  
    discapacidades = models.ManyToManyField(Discapacidad, blank=True, verbose_name="Tipos de Discapacidad")
    
    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} ({self.identificacion})"
    
    class Meta:
        verbose_name_plural = "Pacientes"



class Paciente_Discapacidad(models.Model):
    pass

class Oposicion_Donacion(models.Model):
    pass

class Comunidad_Etnica(models.Model):
    pass

class Paciente_Pais(models.Model):
    pass

class Voluntad_Anticipada(models.Model):
    pass

class Entidad_Prestadora_Salud(models.Model):
    pass

class Contacto_Servicio_Salud(models.Model):
    pass

class Modalidad_Realizacion_Tecnologia_Salud(models.Model):
    pass

class Via_Ingreso_Servicio_Salud(models.Model):
    pass

class Motivo_Atencion(models.Model):
    pass

class Diagnostico(models.Model):
    pass

class Enfermedad_Huerfana(models.Model):
    pass
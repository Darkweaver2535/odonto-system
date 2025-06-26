from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
import os

def patient_photo_path(instance, filename):
    # Guarda las fotos en: media/pacientes/fotos/id_paciente/filename
    return f'pacientes/fotos/{instance.ci}/{filename}'

class Paciente(models.Model):
    GENERO_CHOICES = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('tratamiento', 'En Tratamiento'),
        ('moroso', 'Moroso'),
    ]
    
    PARENTESCO_CHOICES = [
        ('padre', 'Padre'),
        ('madre', 'Madre'),
        ('hermano', 'Hermano/a'),
        ('hijo', 'Hijo/a'),
        ('pareja', 'Cónyuge/Pareja'),
        ('amigo', 'Amigo/a'),
        ('otro', 'Otro'),
    ]
    
    GRUPO_SANGUINEO_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('desconocido', 'Desconocido'),
    ]
    
    # Datos personales
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    ci = models.CharField(max_length=20, unique=True, verbose_name="Cédula de Identidad")
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES)
    foto = models.ImageField(upload_to=patient_photo_path, blank=True, null=True)
    
    # Información de contacto
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, default='Bolivia')
    
    # Contacto de emergencia
    emergencia_nombre = models.CharField(max_length=200)
    emergencia_telefono = models.CharField(max_length=20)
    emergencia_parentesco = models.CharField(max_length=20, choices=PARENTESCO_CHOICES)
    
    # Datos médicos
    grupo_sanguineo = models.CharField(max_length=20, choices=GRUPO_SANGUINEO_CHOICES, blank=True, null=True)
    medicamentos = models.TextField(blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    enfermedades_cronicas = models.TextField(blank=True, null=True)
    
    # Seguro médico
    tiene_seguro = models.BooleanField(default=False)
    seguro_compania = models.CharField(max_length=100, blank=True, null=True)
    seguro_poliza = models.CharField(max_length=100, blank=True, null=True)
    seguro_cobertura = models.TextField(blank=True, null=True)
    
    # Observaciones
    observaciones = models.TextField(blank=True, null=True)
    
    # Metadatos
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    fecha_registro = models.DateField(default=timezone.now)
    ultima_visita = models.DateField(blank=True, null=True)
    consentimiento_datos = models.BooleanField(default=False)
    
    # Timestamps
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} (CI: {self.ci})"
    
    def get_edad(self):
        """Calcula la edad del paciente"""
        today = timezone.now().date()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
    
    def get_nombre_completo(self):
        """Retorna el nombre completo del paciente"""
        return f"{self.nombres} {self.apellidos}"
    
    def get_iniciales(self):
        """Retorna las iniciales del paciente para el avatar"""
        try:
            iniciales = self.nombres[0] + self.apellidos[0]
            return iniciales.upper()
        except IndexError:
            return "P"

from django.db import models
from django.utils import timezone
from apps.pacientes.models import Paciente
from django.contrib.auth.models import User

class HistoriaBase(models.Model):
    """Modelo base para los diferentes tipos de registros de historia clínica."""
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="%(class)ss")
    fecha = models.DateTimeField(default=timezone.now)
    doctor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="%(class)ss")
    observaciones = models.TextField(blank=True, null=True)
    creado_el = models.DateTimeField(auto_now_add=True)
    modificado_el = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-fecha']

class Anamnesis(HistoriaBase):
    """Modelo para almacenar la información de la anamnesis del paciente."""
    TIPO_OPCIONES = [
        ('inicial', 'Inicial'),
        ('seguimiento', 'Seguimiento'),
        ('control', 'Control')
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_OPCIONES, default='inicial')
    motivo_consulta = models.TextField(verbose_name="Motivo de la consulta")
    
    # Antecedentes Médicos
    hipertension = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    cardiopatia = models.BooleanField(default=False)
    hepatitis = models.BooleanField(default=False)
    alergias = models.BooleanField(default=False)
    alergias_detalle = models.TextField(blank=True, null=True, verbose_name="Detalles de alergias")
    medicamentos_actuales = models.TextField(blank=True, null=True)
    otros_antecedentes = models.TextField(blank=True, null=True)
    
    # Antecedentes Odontológicos
    tratamiento_dental_previo = models.BooleanField(default=False)
    protesis = models.BooleanField(default=False)
    cirugia_oral = models.BooleanField(default=False)
    dolor_mandibular = models.BooleanField(default=False)
    sangrado_encias = models.BooleanField(default=False)
    ultima_visita_odontologica = models.CharField(max_length=100, blank=True, null=True)
    motivo_ultima_visita = models.CharField(max_length=200, blank=True, null=True)
    habitos_higiene = models.TextField(blank=True, null=True)
    
    # Síntomas actuales
    dolor = models.BooleanField(default=False)
    sensibilidad = models.BooleanField(default=False)
    inflamacion = models.BooleanField(default=False)
    sangrado = models.BooleanField(default=False)
    mal_aliento = models.BooleanField(default=False)
    inicio_sintomas = models.CharField(max_length=100, blank=True, null=True)
    intensidad_dolor = models.IntegerField(blank=True, null=True, choices=[(i, i) for i in range(1, 11)])
    descripcion_sintomas = models.TextField(blank=True, null=True)

    # Hábitos y Factores de Riesgo
    fuma = models.BooleanField(default=False)
    alcohol = models.BooleanField(default=False)
    bruxismo = models.BooleanField(default=False)
    onicofagia = models.BooleanField(default=False)
    respirador_bucal = models.BooleanField(default=False)
    otros_habitos = models.TextField(blank=True, null=True)
    
    # Consentimiento
    consentimiento = models.BooleanField(default=False, verbose_name="Paciente dio su consentimiento")
    firma_paciente = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Anamnesis"
        verbose_name_plural = "Anamnesis"
    
    def __str__(self):
        return f"Anamnesis de {self.paciente} - {self.fecha.strftime('%d/%m/%Y')}"

class ExamenClinico(HistoriaBase):
    """Modelo para almacenar la información del examen clínico del paciente."""
    TIPO_OPCIONES = [
        ('inicial', 'Inicial'),
        ('seguimiento', 'Seguimiento'),
        ('preoperatorio', 'Preoperatorio'),
        ('postoperatorio', 'Postoperatorio')
    ]
    
    ESTADO_OPCIONES = [
        ('normal', 'Normal'),
        ('atencion', 'Requiere atención'),
        ('patologico', 'Patológico'),
        ('no_aplica', 'No aplica')
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_OPCIONES, default='inicial')
    
    # Signos vitales
    presion_arterial = models.CharField(max_length=20, blank=True, null=True)
    pulso = models.IntegerField(blank=True, null=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    frecuencia_respiratoria = models.IntegerField(blank=True, null=True)
    
    # Examen Extraoral - ATM
    atm_ruidos = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    atm_dolor = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    atm_movimiento = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    atm_observaciones = models.TextField(blank=True, null=True)
    
    # Examen Extraoral - Cara y cuello
    ganglios = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    cicatrices = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    asimetrias = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    extra_observaciones = models.TextField(blank=True, null=True)
    
    # Examen Intraoral - Tejidos blandos
    labios = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    mejillas = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    paladar = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    lengua = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    piso_boca = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    encias = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    tejidos_observaciones = models.TextField(blank=True, null=True)
    
    # Examen Intraoral - Periodonto
    sangrado_encias = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    retraccion_gingival = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    calculo_dental = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    movilidad_dental = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    periodonto_observaciones = models.TextField(blank=True, null=True)
    
    # Examen Intraoral - Oclusión y Dentición
    tipo_mordida = models.CharField(max_length=100, blank=True, null=True)
    malposiciones = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    dientes_ausentes = models.CharField(max_length=100, blank=True, null=True)
    higiene_oral = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    caries_dental = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='normal')
    oclusion_observaciones = models.TextField(blank=True, null=True)
    
    # Diagnóstico Clínico
    diagnostico_principal = models.TextField()
    diagnosticos_secundarios = models.TextField(blank=True, null=True)
    plan_tratamiento = models.TextField(blank=True, null=True)
    
    # Fotografías
    # Aquí implementaríamos un modelo relacionado para fotos si fuera necesario
    
    class Meta:
        verbose_name = "Examen Clínico"
        verbose_name_plural = "Exámenes Clínicos"
    
    def __str__(self):
        return f"Examen clínico de {self.paciente} - {self.fecha.strftime('%d/%m/%Y')}"

class Odontograma(HistoriaBase):
    """Modelo para almacenar la información del odontograma del paciente."""
    TIPO_OPCIONES = [
        ('inicial', 'Inicial'),
        ('control', 'Control'),
        ('final', 'Final')
    ]
    
    DENTICION_OPCIONES = [
        ('permanente', 'Permanente'),
        ('temporal', 'Temporal'),
        ('mixta', 'Mixta')
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_OPCIONES, default='inicial')
    denticion = models.CharField(max_length=20, choices=DENTICION_OPCIONES, default='permanente')
    datos_odontograma = models.JSONField(blank=True, null=True, help_text="Datos del odontograma en formato JSON")
    notas_tratamiento = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Odontograma"
        verbose_name_plural = "Odontogramas"
    
    def __str__(self):
        return f"Odontograma de {self.paciente} - {self.fecha.strftime('%d/%m/%Y')}"

# Modelos relacionados para dientes y tratamientos
class DienteEstado(models.Model):
    """Modelo para almacenar el estado de cada diente en el odontograma."""
    odontograma = models.ForeignKey(Odontograma, on_delete=models.CASCADE, related_name="dientes")
    numero_diente = models.IntegerField()
    estado = models.CharField(max_length=50)  # caries, restauración, extracción, etc.
    superficie = models.CharField(max_length=20, blank=True, null=True)  # oclusal, mesial, distal, etc.
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Estado de Diente"
        verbose_name_plural = "Estados de Dientes"
        unique_together = ['odontograma', 'numero_diente', 'superficie']
    
    def __str__(self):
        return f"Diente {self.numero_diente} - {self.estado}"

# Añadir este nuevo modelo para gestionar fotos clínicas

def foto_clinica_path(instance, filename):
    """Define la ruta donde se guardará la foto clínica."""
    return f'pacientes/{instance.examen.paciente.id}/examenes/{instance.examen.id}/fotos/{filename}'

class FotoClinica(models.Model):
    """Modelo para almacenar fotos clínicas asociadas a un examen clínico."""
    examen = models.ForeignKey(ExamenClinico, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to=foto_clinica_path)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Foto Clínica"
        verbose_name_plural = "Fotos Clínicas"
    
    def __str__(self):
        return f"Foto de {self.examen.paciente} - {self.fecha_subida.strftime('%d/%m/%Y')}"

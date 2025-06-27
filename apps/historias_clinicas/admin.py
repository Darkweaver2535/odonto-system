from django.contrib import admin
from .models import Anamnesis, ExamenClinico, Odontograma, DienteEstado, FotoClinica

class DienteEstadoInline(admin.TabularInline):
    model = DienteEstado
    extra = 0

class FotoClinicaInline(admin.TabularInline):
    model = FotoClinica
    extra = 0

@admin.register(Anamnesis)
class AnamnesisAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'fecha', 'doctor', 'tipo', 'motivo_consulta']
    list_filter = ['tipo', 'fecha', 'doctor']
    search_fields = ['paciente__nombres', 'paciente__apellidos', 'paciente__ci', 'motivo_consulta']
    date_hierarchy = 'fecha'
    fieldsets = (
        ('Información Básica', {
            'fields': ('paciente', 'doctor', 'fecha', 'tipo', 'motivo_consulta')
        }),
        ('Antecedentes Médicos', {
            'fields': ('hipertension', 'diabetes', 'cardiopatia', 'hepatitis', 'alergias', 
                      'alergias_detalle', 'medicamentos_actuales', 'otros_antecedentes')
        }),
        ('Antecedentes Odontológicos', {
            'fields': ('tratamiento_dental_previo', 'protesis', 'cirugia_oral', 'dolor_mandibular',
                     'sangrado_encias', 'ultima_visita_odontologica', 'motivo_ultima_visita', 'habitos_higiene')
        }),
        ('Síntomas Actuales', {
            'fields': ('dolor', 'sensibilidad', 'inflamacion', 'sangrado', 'mal_aliento',
                      'inicio_sintomas', 'intensidad_dolor', 'descripcion_sintomas')
        }),
        ('Hábitos y Factores de Riesgo', {
            'fields': ('fuma', 'alcohol', 'bruxismo', 'onicofagia', 'respirador_bucal', 'otros_habitos')
        }),
        ('Observaciones y Consentimiento', {
            'fields': ('observaciones', 'consentimiento', 'firma_paciente')
        }),
    )

@admin.register(ExamenClinico)
class ExamenClinicoAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'fecha', 'doctor', 'tipo', 'diagnostico_principal']
    list_filter = ['tipo', 'fecha', 'doctor']
    search_fields = ['paciente__nombres', 'paciente__apellidos', 'paciente__ci', 'diagnostico_principal']
    date_hierarchy = 'fecha'
    inlines = [FotoClinicaInline]
    fieldsets = (
        ('Información Básica', {
            'fields': ('paciente', 'doctor', 'fecha', 'tipo')
        }),
        ('Signos Vitales', {
            'fields': ('presion_arterial', 'pulso', 'temperatura', 'frecuencia_respiratoria')
        }),
        ('Examen Extraoral - ATM', {
            'fields': ('atm_ruidos', 'atm_dolor', 'atm_movimiento', 'atm_observaciones')
        }),
        ('Examen Extraoral - Cara y Cuello', {
            'fields': ('ganglios', 'cicatrices', 'asimetrias', 'extra_observaciones')
        }),
        ('Examen Intraoral - Tejidos Blandos', {
            'fields': ('labios', 'mejillas', 'paladar', 'lengua', 'piso_boca', 'encias', 'tejidos_observaciones')
        }),
        ('Examen Intraoral - Periodonto', {
            'fields': ('sangrado_encias', 'retraccion_gingival', 'calculo_dental', 'movilidad_dental', 'periodonto_observaciones')
        }),
        ('Examen Intraoral - Oclusión y Dentición', {
            'fields': ('tipo_mordida', 'malposiciones', 'dientes_ausentes', 'higiene_oral', 'caries_dental', 'oclusion_observaciones')
        }),
        ('Diagnóstico', {
            'fields': ('diagnostico_principal', 'diagnosticos_secundarios', 'plan_tratamiento', 'observaciones')
        }),
    )

@admin.register(Odontograma)
class OdontogramaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'fecha', 'doctor', 'tipo', 'denticion']
    list_filter = ['tipo', 'denticion', 'fecha', 'doctor']
    search_fields = ['paciente__nombres', 'paciente__apellidos', 'paciente__ci']
    date_hierarchy = 'fecha'
    inlines = [DienteEstadoInline]
    fieldsets = (
        ('Información Básica', {
            'fields': ('paciente', 'doctor', 'fecha', 'tipo', 'denticion')
        }),
        ('Detalles', {
            'fields': ('datos_odontograma', 'notas_tratamiento', 'observaciones')
        }),
    )

@admin.register(DienteEstado)
class DienteEstadoAdmin(admin.ModelAdmin):
    list_display = ['odontograma', 'numero_diente', 'estado', 'superficie']
    list_filter = ['estado']
    search_fields = ['odontograma__paciente__nombres', 'odontograma__paciente__apellidos', 'numero_diente']

@admin.register(FotoClinica)
class FotoClinicaAdmin(admin.ModelAdmin):
    list_display = ['examen', 'descripcion', 'fecha_subida']
    list_filter = ['fecha_subida']
    search_fields = ['examen__paciente__nombres', 'examen__paciente__apellidos', 'descripcion']

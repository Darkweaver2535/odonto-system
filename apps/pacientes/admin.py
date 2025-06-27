from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'ci', 'telefono', 'ocupacion', 'fecha_registro', 'estado']
    list_filter = ['estado', 'genero', 'ciudad', 'tiene_seguro', 'vacuna_covid']
    search_fields = ['nombres', 'apellidos', 'ci', 'telefono', 'email', 'ocupacion']
    date_hierarchy = 'fecha_registro'
    fieldsets = [
        ('Información Personal', {
            'fields': ['nombres', 'apellidos', 'ci', 'fecha_nacimiento', 'genero', 'ocupacion', 'foto']
        }),
        ('Información de Contacto', {
            'fields': ['telefono', 'email', 'direccion', 'ciudad', 'departamento', 'pais']
        }),
        ('Contacto de Emergencia', {
            'fields': ['emergencia_nombre', 'emergencia_telefono', 'emergencia_parentesco']
        }),
        ('Información Médica', {
            'fields': ['grupo_sanguineo', 'medicamentos', 'alergias', 'enfermedades_cronicas', 'vacuna_covid']
        }),
        ('Seguro Médico', {
            'fields': ['tiene_seguro', 'seguro_compania', 'seguro_poliza', 'seguro_cobertura']
        }),
        ('Información Adicional', {
            'fields': ['como_localizo', 'como_localizo_detalle']
        }),
        ('Observaciones', {
            'fields': ['observaciones']
        }),
        ('Metadatos', {
            'fields': ['estado', 'fecha_registro', 'ultima_visita', 'consentimiento_datos']
        })
    ]
    readonly_fields = ['creado_en', 'actualizado_en']

from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'ci', 'telefono', 'fecha_registro', 'estado']
    list_filter = ['estado', 'genero', 'ciudad', 'tiene_seguro']
    search_fields = ['nombres', 'apellidos', 'ci', 'telefono', 'email']
    date_hierarchy = 'fecha_registro'
    fieldsets = [
        ('Información Personal', {
            'fields': ['nombres', 'apellidos', 'ci', 'fecha_nacimiento', 'genero', 'foto']
        }),
        ('Información de Contacto', {
            'fields': ['telefono', 'email', 'direccion', 'ciudad', 'departamento', 'pais']
        }),
        ('Contacto de Emergencia', {
            'fields': ['emergencia_nombre', 'emergencia_telefono', 'emergencia_parentesco']
        }),
        ('Información Médica', {
            'fields': ['grupo_sanguineo', 'medicamentos', 'alergias', 'enfermedades_cronicas']
        }),
        ('Seguro Médico', {
            'fields': ['tiene_seguro', 'seguro_compania', 'seguro_poliza', 'seguro_cobertura']
        }),
        ('Observaciones', {
            'fields': ['observaciones']
        }),
        ('Metadatos', {
            'fields': ['estado', 'fecha_registro', 'ultima_visita', 'consentimiento_datos']
        })
    ]
    readonly_fields = ['creado_en', 'actualizado_en']

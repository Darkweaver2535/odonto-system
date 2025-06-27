from django import forms
from django.core.exceptions import ValidationError
from .models import Paciente
from django.utils import timezone

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        exclude = ['creado_en', 'actualizado_en', 'ultima_visita']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 2}),
            'medicamentos': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Separe los medicamentos con comas'}),
            'alergias': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Describa las alergias del paciente (medicamentos, alimentos, etc.)'}),
            'enfermedades_cronicas': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Describa las enfermedades crónicas del paciente'}),
            'seguro_cobertura': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Detalle la cobertura del seguro'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ingrese información adicional relevante del paciente'}),
            'ocupacion': forms.TextInput(attrs={'placeholder': 'Ej. Ingeniero, Profesor, Estudiante...'}),
            'como_localizo_detalle': forms.TextInput(attrs={'placeholder': 'Proporcione detalles si es necesario'}),
        }
        labels = {
            'ci': 'Cédula de Identidad',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'emergencia_nombre': 'Nombre Completo',
            'emergencia_telefono': 'Teléfono',
            'emergencia_parentesco': 'Parentesco',
            'grupo_sanguineo': 'Grupo Sanguíneo',
            'tiene_seguro': 'Paciente cuenta con seguro médico',
            'seguro_compania': 'Compañía Aseguradora',
            'seguro_poliza': 'Número de Póliza',
            'seguro_cobertura': 'Cobertura',
            'consentimiento_datos': 'El paciente ha dado su consentimiento para el tratamiento de sus datos personales y médicos',
            'ocupacion': 'Ocupación',
            'vacuna_covid': 'Vacuna contra COVID-19',
            'como_localizo': '¿Cómo nos localizó?',
            'como_localizo_detalle': 'Detalles',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que algunos campos no sean requeridos en el formulario
        self.fields['email'].required = False
        self.fields['grupo_sanguineo'].required = False
        self.fields['medicamentos'].required = False
        self.fields['alergias'].required = False
        self.fields['enfermedades_cronicas'].required = False
        self.fields['observaciones'].required = False
        self.fields['ocupacion'].required = False
        self.fields['como_localizo'].required = False
        self.fields['como_localizo_detalle'].required = False
        
        # Configurar valores predeterminados para estado y fecha_registro
        if not self.instance.pk:  # Solo para nuevas instancias (no en edición)
            self.initial['estado'] = 'activo'
            self.initial['fecha_registro'] = timezone.now().date()
            
            # Modificar estos campos directamente para manejarlos mejor
            self.fields['estado'].required = False
            self.fields['fecha_registro'].required = False
            self.fields['estado'].widget = forms.HiddenInput()
            self.fields['fecha_registro'].widget = forms.HiddenInput()
    
    def clean_ci(self):
        ci = self.cleaned_data.get('ci')
        # Verificar si la CI ya existe (excepto para el paciente actual en caso de edición)
        if Paciente.objects.filter(ci=ci).exists() and self.instance.pk is None:
            raise ValidationError("Ya existe un paciente con esta cédula de identidad.")
        return ci
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Asignar valores predeterminados para estos campos siempre
        cleaned_data['estado'] = cleaned_data.get('estado') or 'activo'
        cleaned_data['fecha_registro'] = cleaned_data.get('fecha_registro') or timezone.now().date()
        
        # Lógica para manejo de campos de seguro
        tiene_seguro = cleaned_data.get('tiene_seguro')
        if not tiene_seguro:
            # Si no tiene seguro, limpiamos los campos relacionados
            cleaned_data['seguro_compania'] = None
            cleaned_data['seguro_poliza'] = None
            cleaned_data['seguro_cobertura'] = None
        
        return cleaned_data
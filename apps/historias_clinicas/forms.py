from django import forms
from .models import Anamnesis, ExamenClinico, Odontograma, DienteEstado

class AnamnesisForm(forms.ModelForm):
    class Meta:
        model = Anamnesis
        exclude = ['paciente', 'doctor', 'creado_el', 'modificado_el']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'motivo_consulta': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describa el motivo principal de la consulta del paciente'}),
            'alergias_detalle': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Especifique las alergias del paciente'}),
            'medicamentos_actuales': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Liste los medicamentos que toma actualmente'}),
            'otros_antecedentes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Describa otros antecedentes médicos relevantes'}),
            'habitos_higiene': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Describa los hábitos de higiene bucal del paciente'}),
            'descripcion_sintomas': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Describa los síntomas en detalle'}),
            'otros_habitos': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Describa otros hábitos relevantes'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observaciones adicionales importantes'}),
            'intensidad_dolor': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'firma_paciente': forms.TextInput(attrs={'placeholder': 'Nombre completo del paciente como firma'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        alergias = cleaned_data.get('alergias')
        alergias_detalle = cleaned_data.get('alergias_detalle')
        
        # Si marca alergias pero no proporciona detalles
        if alergias and not alergias_detalle:
            self.add_error('alergias_detalle', 'Por favor, detalle las alergias del paciente.')
        
        return cleaned_data

class ExamenClinicoForm(forms.ModelForm):
    class Meta:
        model = ExamenClinico
        exclude = ['paciente', 'doctor', 'creado_el', 'modificado_el']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'presion_arterial': forms.TextInput(attrs={'placeholder': 'Ej: 120/80'}),
            'pulso': forms.NumberInput(attrs={'placeholder': 'Latidos por minuto'}),
            'temperatura': forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'Ej: 36.5'}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'placeholder': 'Respiraciones por minuto'}),
            
            'atm_ruidos': forms.Select(attrs={'class': 'form-select'}),
            'atm_dolor': forms.Select(attrs={'class': 'form-select'}),
            'atm_movimiento': forms.Select(attrs={'class': 'form-select'}),
            'atm_observaciones': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Observaciones sobre ATM'}),
            
            'ganglios': forms.Select(attrs={'class': 'form-select'}),
            'cicatrices': forms.Select(attrs={'class': 'form-select'}),
            'asimetrias': forms.Select(attrs={'class': 'form-select'}),
            'extra_observaciones': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Observaciones extraorales'}),
            
            'labios': forms.Select(attrs={'class': 'form-select'}),
            'mejillas': forms.Select(attrs={'class': 'form-select'}),
            'paladar': forms.Select(attrs={'class': 'form-select'}),
            'lengua': forms.Select(attrs={'class': 'form-select'}),
            'piso_boca': forms.Select(attrs={'class': 'form-select'}),
            'encias': forms.Select(attrs={'class': 'form-select'}),
            'tejidos_observaciones': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Observaciones sobre tejidos blandos'}),
            
            'sangrado_encias': forms.Select(attrs={'class': 'form-select'}),
            'retraccion_gingival': forms.Select(attrs={'class': 'form-select'}),
            'calculo_dental': forms.Select(attrs={'class': 'form-select'}),
            'movilidad_dental': forms.Select(attrs={'class': 'form-select'}),
            'periodonto_observaciones': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Observaciones sobre periodonto'}),
            
            'tipo_mordida': forms.TextInput(attrs={'placeholder': 'Ej: Clase I, Clase II, etc.'}),
            'malposiciones': forms.Select(attrs={'class': 'form-select'}),
            'dientes_ausentes': forms.TextInput(attrs={'placeholder': 'Ej: 16, 26, 36, 46'}),
            'higiene_oral': forms.Select(attrs={'class': 'form-select'}),
            'caries_dental': forms.Select(attrs={'class': 'form-select'}),
            'oclusion_observaciones': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Observaciones sobre oclusión'}),
            
            'diagnostico_principal': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Diagnóstico principal del paciente', 'required': 'required'}),
            'diagnosticos_secundarios': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Otros diagnósticos relevantes'}),
            'plan_tratamiento': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Plan de tratamiento propuesto'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observaciones adicionales importantes'}),
        }
    
    def clean_diagnostico_principal(self):
        diagnostico = self.cleaned_data.get('diagnostico_principal')
        if not diagnostico:
            raise forms.ValidationError("Este campo es obligatorio.")
        return diagnostico

class OdontogramaForm(forms.ModelForm):
    class Meta:
        model = Odontograma
        exclude = ['paciente', 'doctor', 'datos_odontograma', 'creado_el', 'modificado_el']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'denticion': forms.Select(attrs={'class': 'form-select'}),
            'notas_tratamiento': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Notas sobre tratamientos necesarios'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observaciones adicionales importantes'}),
        }

class DienteEstadoForm(forms.ModelForm):
    class Meta:
        model = DienteEstado
        fields = ['numero_diente', 'estado', 'superficie', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Observaciones específicas sobre este diente'}),
        }
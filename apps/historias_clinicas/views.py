from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
import json  # Agregar esta importación
import os  # Para operaciones con archivos
from apps.pacientes.models import Paciente
from .models import Anamnesis, ExamenClinico, Odontograma, DienteEstado, FotoClinica
from .forms import AnamnesisForm, ExamenClinicoForm, OdontogramaForm, DienteEstadoForm

# Vistas de selección de paciente
@login_required
def lista_pacientes_anamnesis(request):
    """
    Vista que muestra la lista de pacientes para seleccionar uno 
    y gestionar su anamnesis.
    """
    pacientes = Paciente.objects.all().order_by('apellidos', 'nombres')
    
    context = {
        'pacientes': pacientes,
        'seccion': 'anamnesis',
        'titulo': 'Anamnesis - Selección de Paciente',
    }
    return render(request, 'historias_clinicas/lista_pacientes.html', context)

@login_required
def lista_pacientes_examen_clinico(request):
    """
    Vista que muestra la lista de pacientes para seleccionar uno 
    y gestionar su examen clínico.
    """
    pacientes = Paciente.objects.all().order_by('apellidos', 'nombres')
    
    context = {
        'pacientes': pacientes,
        'seccion': 'examen_clinico',
        'titulo': 'Examen Clínico - Selección de Paciente',
    }
    return render(request, 'historias_clinicas/lista_pacientes.html', context)

@login_required
def lista_pacientes_odontograma(request):
    """
    Vista que muestra la lista de pacientes para seleccionar uno 
    y gestionar su odontograma.
    """
    pacientes = Paciente.objects.all().order_by('apellidos', 'nombres')
    
    context = {
        'pacientes': pacientes,
        'seccion': 'odontograma',
        'titulo': 'Odontograma - Selección de Paciente',
    }
    return render(request, 'historias_clinicas/lista_pacientes.html', context)

# Vistas para Anamnesis
@login_required
def historial_anamnesis(request, paciente_id):
    """
    Vista que muestra el historial de anamnesis del paciente con opción
    de crear una nueva o editar las existentes.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id)
    anamnesis_list = Anamnesis.objects.filter(paciente=paciente).order_by('-fecha')
    
    context = {
        'paciente': paciente,
        'anamnesis_list': anamnesis_list,
    }
    return render(request, 'historias_clinicas/historial_anamnesis.html', context)

@login_required
def nueva_anamnesis(request, paciente_id):
    """
    Vista para crear una nueva anamnesis para un paciente.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        form = AnamnesisForm(request.POST)
        if form.is_valid():
            anamnesis = form.save(commit=False)
            anamnesis.paciente = paciente
            anamnesis.doctor = request.user
            anamnesis.save()
            
            # Actualizar la fecha de última visita del paciente
            paciente.ultima_visita = timezone.now().date()
            paciente.save()
            
            messages.success(request, 'Anamnesis registrada correctamente')
            return redirect('historias_clinicas:historial_anamnesis', paciente_id=paciente.id)
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario')
    else:
        # Inicializar con datos del paciente si están disponibles
        initial_data = {}
        form = AnamnesisForm(initial=initial_data)
    
    context = {
        'paciente': paciente,
        'form': form,
        'fecha_actual': timezone.now(),
        'es_nueva': True
    }
    return render(request, 'historias_clinicas/anamnesis.html', context)

@login_required
def editar_anamnesis(request, paciente_id, anamnesis_id):
    """
    Vista para editar una anamnesis existente.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id)
    anamnesis = get_object_or_404(Anamnesis, id=anamnesis_id, paciente=paciente)
    
    if request.method == 'POST':
        form = AnamnesisForm(request.POST, instance=anamnesis)
        if form.is_valid():
            anamnesis = form.save()
            messages.success(request, 'Anamnesis actualizada correctamente')
            return redirect('historias_clinicas:historial_anamnesis', paciente_id=paciente.id)
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario')
    else:
        form = AnamnesisForm(instance=anamnesis)
    
    context = {
        'paciente': paciente,
        'anamnesis': anamnesis,
        'form': form,
        'es_nueva': False
    }
    return render(request, 'historias_clinicas/anamnesis.html', context)

# Vistas para Examen Clínico
@login_required
def historial_examen_clinico(request, paciente_id):
    """
    Vista que muestra el historial de exámenes clínicos del paciente.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id)
    examenes_list = ExamenClinico.objects.filter(paciente=paciente).order_by('-fecha')
    
    context = {
        'paciente': paciente,
        'examenes_list': examenes_list,
    }
    return render(request, 'historias_clinicas/historial_examen_clinico.html', context)

@login_required
def nuevo_examen_clinico(request, paciente_id):
    """
    Vista para crear un nuevo examen clínico para un paciente.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        form = ExamenClinicoForm(request.POST)
        if form.is_valid():
            examen = form.save(commit=False)
            examen.paciente = paciente
            examen.doctor = request.user
            examen.save()
            
            # Procesar fotos clínicas si se han subido
            fotos = request.FILES.getlist('fotos_clinicas')
            for foto in fotos:
                FotoClinica.objects.create(
                    examen=examen,
                    imagen=foto
                )
            
            # Actualizar la fecha de última visita del paciente
            paciente.ultima_visita = timezone.now().date()
            paciente.save()
            
            messages.success(request, 'Examen clínico registrado correctamente')
            
            # Si es guardar borrador, quedarse en la misma página
            if 'guardar_borrador' in request.POST:
                return redirect('historias_clinicas:editar_examen_clinico', paciente_id=paciente.id, examen_id=examen.id)
            else:
                return redirect('historias_clinicas:historial_examen_clinico', paciente_id=paciente.id)
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario')
    else:
        form = ExamenClinicoForm(initial={'fecha': timezone.now()})
    
    context = {
        'paciente': paciente,
        'form': form,
        'fecha_actual': timezone.now(),
        'es_nuevo': True
    }
    return render(request, 'historias_clinicas/examen_clinico.html', context)

@login_required
def editar_examen_clinico(request, paciente_id, examen_id):
    """
    Vista para editar un examen clínico existente.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id)
    examen = get_object_or_404(ExamenClinico, id=examen_id, paciente=paciente)
    
    if request.method == 'POST':
        form = ExamenClinicoForm(request.POST, instance=examen)
        if form.is_valid():
            examen = form.save()
            
            # Procesar fotos clínicas si se han subido
            fotos = request.FILES.getlist('fotos_clinicas')
            for foto in fotos:
                FotoClinica.objects.create(
                    examen=examen,
                    imagen=foto
                )
            
            messages.success(request, 'Examen clínico actualizado correctamente')
            
            # Si es guardar borrador, quedarse en la misma página
            if 'guardar_borrador' in request.POST:
                return redirect('historias_clinicas:editar_examen_clinico', paciente_id=paciente.id, examen_id=examen.id)
            else:
                return redirect('historias_clinicas:historial_examen_clinico', paciente_id=paciente.id)
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario')
    else:
        form = ExamenClinicoForm(instance=examen)
    
    # Obtener las fotos existentes para mostrarlas
    fotos = examen.fotos.all()
    
    context = {
        'paciente': paciente,
        'examen': examen,
        'form': form,
        'es_nuevo': False,
        'fotos': fotos
    }
    return render(request, 'historias_clinicas/examen_clinico.html', context)

# Vistas para Odontograma
@login_required
def historial_odontograma(request, paciente_id):
    """
    Vista que muestra el historial de odontogramas del paciente.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id)
    odontogramas_list = Odontograma.objects.filter(paciente=paciente).order_by('-fecha')
    
    context = {
        'paciente': paciente,
        'odontogramas_list': odontogramas_list,
    }
    return render(request, 'historias_clinicas/historial_odontograma.html', context)

@login_required
def nuevo_odontograma(request, paciente_id):
    """
    Vista para crear un nuevo odontograma para un paciente.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        form = OdontogramaForm(request.POST)
        if form.is_valid():
            odontograma = form.save(commit=False)
            odontograma.paciente = paciente
            odontograma.doctor = request.user
            
            # Procesar datos del odontograma en formato JSON
            datos_odontograma = {}
            
            # Procesar el campo odontogram_data si existe (datos completos)
            if 'odontogram_data' in request.POST:
                try:
                    datos_odontograma = json.loads(request.POST['odontogram_data'])
                except json.JSONDecodeError:
                    messages.error(request, 'Error al procesar los datos del odontograma')
                    return redirect('historias_clinicas:nuevo_odontograma', paciente_id=paciente.id)
            else:
                # Procesar campos individuales como alternativa
                for key, value in request.POST.items():
                    if key.startswith('diente_'):
                        numero_diente = key.split('_')[1]
                        try:
                            estado_data = json.loads(value)
                            datos_odontograma[numero_diente] = estado_data
                        except json.JSONDecodeError:
                            continue
            
            odontograma.datos_odontograma = datos_odontograma
            odontograma.save()
            
            # Guardar estados individuales de dientes
            for diente_num, estado_data in datos_odontograma.items():
                if isinstance(estado_data, dict):  # Si hay datos específicos por superficie
                    for superficie, estado in estado_data.items():
                        DienteEstado.objects.create(
                            odontograma=odontograma,
                            numero_diente=int(diente_num),
                            estado=estado,
                            superficie=superficie
                        )
                else:  # Si es un estado general del diente
                    DienteEstado.objects.create(
                        odontograma=odontograma,
                        numero_diente=int(diente_num),
                        estado=estado_data
                    )
            
            # Actualizar la fecha de última visita del paciente
            paciente.ultima_visita = timezone.now().date()
            paciente.save()
            
            messages.success(request, 'Odontograma registrado correctamente')
            return redirect('historias_clinicas:historial_odontograma', paciente_id=paciente.id)
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario')
    else:
        form = OdontogramaForm(initial={'fecha': timezone.now()})
    
    context = {
        'paciente': paciente,
        'form': form,
        'fecha_actual': timezone.now(),
        'es_nuevo': True
    }
    return render(request, 'historias_clinicas/odontograma.html', context)

@login_required
def editar_odontograma(request, paciente_id, odontograma_id):
    """
    Vista para editar un odontograma existente.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id)
    odontograma = get_object_or_404(Odontograma, id=odontograma_id, paciente=paciente)
    
    if request.method == 'POST':
        form = OdontogramaForm(request.POST, instance=odontograma)
        if form.is_valid():
            odontograma = form.save(commit=False)
            
            # Actualizar los datos del odontograma JSON
            datos_odontograma = {}
            
            # Procesar el campo odontogram_data si existe (datos completos)
            if 'odontogram_data' in request.POST:
                try:
                    datos_odontograma = json.loads(request.POST['odontogram_data'])
                except json.JSONDecodeError:
                    messages.error(request, 'Error al procesar los datos del odontograma')
                    return redirect('historias_clinicas:editar_odontograma', paciente_id=paciente.id, odontograma_id=odontograma.id)
            else:
                # Procesar campos individuales como alternativa
                for key, value in request.POST.items():
                    if key.startswith('diente_'):
                        numero_diente = key.split('_')[1]
                        try:
                            estado_data = json.loads(value)
                            datos_odontograma[numero_diente] = estado_data
                        except json.JSONDecodeError:
                            continue
            
            odontograma.datos_odontograma = datos_odontograma
            odontograma.save()
            
            # Limpiar estados anteriores
            DienteEstado.objects.filter(odontograma=odontograma).delete()
            
            # Guardar estados actualizados de dientes
            for diente_num, estado_data in datos_odontograma.items():
                if isinstance(estado_data, dict):  # Si hay datos específicos por superficie
                    for superficie, estado in estado_data.items():
                        DienteEstado.objects.create(
                            odontograma=odontograma,
                            numero_diente=int(diente_num),
                            estado=estado,
                            superficie=superficie
                        )
                else:  # Si es un estado general del diente
                    DienteEstado.objects.create(
                        odontograma=odontograma,
                        numero_diente=int(diente_num),
                        estado=estado_data
                    )
            
            messages.success(request, 'Odontograma actualizado correctamente')
            
            # Si es guardar borrador, quedarse en la misma página
            if 'guardar_borrador' in request.POST:
                return redirect('historias_clinicas:editar_odontograma', paciente_id=paciente.id, odontograma_id=odontograma.id)
            else:
                return redirect('historias_clinicas:historial_odontograma', paciente_id=paciente.id)
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario')
    else:
        form = OdontogramaForm(instance=odontograma)
    
    # Preparar datos existentes del odontograma para el formulario
    datos_dientes = {}
    
    # Primero intentamos leer los datos desde el campo JSON
    if odontograma.datos_odontograma:
        datos_dientes = odontograma.datos_odontograma
    else:
        # Si no hay datos en el campo JSON, construimos desde los estados individuales
        dientes_estados = DienteEstado.objects.filter(odontograma=odontograma)
        
        for estado in dientes_estados:
            if estado.superficie:
                if str(estado.numero_diente) not in datos_dientes:
                    datos_dientes[str(estado.numero_diente)] = {}
                datos_dientes[str(estado.numero_diente)][estado.superficie] = estado.estado
            else:
                datos_dientes[str(estado.numero_diente)] = estado.estado
    
    context = {
        'paciente': paciente,
        'odontograma': odontograma,
        'form': form,
        'datos_dientes': json.dumps(datos_dientes),
        'es_nuevo': False
    }
    return render(request, 'historias_clinicas/odontograma.html', context)

# Añadir esta vista para eliminar fotos

@login_required
def eliminar_foto_clinica(request, foto_id):
    """Vista para eliminar una foto clínica."""
    foto = get_object_or_404(FotoClinica, id=foto_id)
    paciente_id = foto.examen.paciente.id
    examen_id = foto.examen.id
    
    # Verificar que el usuario tiene permiso (es el doctor o un superusuario)
    if request.user == foto.examen.doctor or request.user.is_superuser:
        # Eliminar el archivo físico
        if foto.imagen and os.path.isfile(foto.imagen.path):
            os.remove(foto.imagen.path)
        
        # Eliminar el registro
        foto.delete()
        messages.success(request, "Foto eliminada correctamente")
    else:
        messages.error(request, "No tiene permiso para eliminar esta foto")
    
    return redirect('historias_clinicas:editar_examen_clinico', paciente_id=paciente_id, examen_id=examen_id)

# Agregar esta nueva vista después de editar_odontograma
@login_required
def detalle_odontograma(request, paciente_id, odontograma_id):
    """
    Vista para ver los detalles de un odontograma existente sin modificarlo.
    """
    import json  # Asegurarnos de que json esté importado
    
    paciente = get_object_or_404(Paciente, id=paciente_id)
    odontograma = get_object_or_404(Odontograma, id=odontograma_id, paciente=paciente)
    
    # Preparar datos existentes del odontograma para la visualización
    datos_dientes = {}
    
    # Primero intentamos leer los datos desde el campo JSON
    if odontograma.datos_odontograma:
        datos_dientes = odontograma.datos_odontograma
    else:
        # Si no hay datos en el campo JSON, construimos desde los estados individuales
        dientes_estados = DienteEstado.objects.filter(odontograma=odontograma)
        
        for estado in dientes_estados:
            if estado.superficie:
                # Si el diente ya tiene entradas, actualizar
                if estado.numero_diente in datos_dientes and isinstance(datos_dientes[estado.numero_diente], dict):
                    datos_dientes[estado.numero_diente][estado.superficie] = estado.estado
                else:
                    # De lo contrario, crear nueva entrada
                    datos_dientes[estado.numero_diente] = {estado.superficie: estado.estado}
            else:
                # Estado general del diente (sin superficie específica)
                datos_dientes[estado.numero_diente] = estado.estado
    
    # Convertir las claves de diente a string para consistencia en JS
    datos_dientes_str = {str(k): v for k, v in datos_dientes.items()}
    
    # Obtener el historial de odontogramas del paciente para navegación
    historial = Odontograma.objects.filter(paciente=paciente).exclude(id=odontograma_id).order_by('-fecha')
    anterior = Odontograma.objects.filter(paciente=paciente, fecha__lt=odontograma.fecha).order_by('-fecha').first()
    siguiente = Odontograma.objects.filter(paciente=paciente, fecha__gt=odontograma.fecha).order_by('fecha').first()
    
    context = {
        'paciente': paciente,
        'odontograma': odontograma,
        'datos_dientes': json.dumps(datos_dientes_str),
        'historial': historial[:5],  # Mostrar solo los 5 más recientes
        'anterior': anterior,
        'siguiente': siguiente,
        'solo_lectura': True  # Indica que es vista de solo lectura
    }
    return render(request, 'historias_clinicas/detalle_odontograma.html', context)

# Agregar esta nueva vista después de editar_examen_clinico
@login_required
def detalle_examen_clinico(request, paciente_id, examen_id):
    """
    Vista para ver los detalles de un examen clínico existente sin modificarlo.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id)
    examen = get_object_or_404(ExamenClinico, id=examen_id, paciente=paciente)
    
    # Obtener las fotos relacionadas
    fotos = examen.fotos.all()
    
    # Obtener el historial de exámenes clínicos del paciente para navegación
    historial = ExamenClinico.objects.filter(paciente=paciente).exclude(id=examen_id).order_by('-fecha')
    anterior = ExamenClinico.objects.filter(paciente=paciente, fecha__lt=examen.fecha).order_by('-fecha').first()
    siguiente = ExamenClinico.objects.filter(paciente=paciente, fecha__gt=examen.fecha).order_by('fecha').first()
    
    context = {
        'paciente': paciente,
        'examen': examen,
        'fotos': fotos,
        'historial': historial[:5],  # Mostrar solo los 5 más recientes
        'anterior': anterior,
        'siguiente': siguiente,
        'solo_lectura': True  # Indica que es vista de solo lectura
    }
    return render(request, 'historias_clinicas/detalle_examen_clinico.html', context)

# Agregar esta nueva vista después de editar_anamnesis
@login_required
def detalle_anamnesis(request, paciente_id, anamnesis_id):
    """
    Vista para ver los detalles de una anamnesis existente sin modificarla.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id)
    anamnesis = get_object_or_404(Anamnesis, id=anamnesis_id, paciente=paciente)
    
    # Obtener el historial de anamnesis del paciente para navegación
    historial = Anamnesis.objects.filter(paciente=paciente).exclude(id=anamnesis_id).order_by('-fecha')
    anterior = Anamnesis.objects.filter(paciente=paciente, fecha__lt=anamnesis.fecha).order_by('-fecha').first()
    siguiente = Anamnesis.objects.filter(paciente=paciente, fecha__gt=anamnesis.fecha).order_by('fecha').first()
    
    context = {
        'paciente': paciente,
        'anamnesis': anamnesis,
        'historial': historial[:5],  # Mostrar solo los 5 más recientes
        'anterior': anterior,
        'siguiente': siguiente,
        'solo_lectura': True  # Indica que es vista de solo lectura
    }
    return render(request, 'historias_clinicas/detalle_anamnesis.html', context)

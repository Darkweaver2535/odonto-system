from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Paciente
from .forms import PacienteForm
from django.utils import timezone

@login_required
def nuevo_paciente(request):
    """Vista para crear un nuevo paciente"""
    if request.method == 'POST':
        form_data = request.POST.copy()  # Hacer una copia mutable
        
        # Asegurar que estado y fecha_registro estén presentes
        if 'estado' not in form_data or not form_data['estado']:
            form_data['estado'] = 'activo'
        if 'fecha_registro' not in form_data or not form_data['fecha_registro']:
            form_data['fecha_registro'] = timezone.now().date().strftime('%Y-%m-%d')
        
        form = PacienteForm(form_data, request.FILES)
        if form.is_valid():
            paciente = form.save()
            messages.success(request, f'Paciente {paciente.get_nombre_completo()} registrado correctamente')
            
            # Según el botón presionado
            if 'guardar_agregar' in request.POST:
                return redirect('pacientes:nuevo_paciente')
            else:
                return redirect('pacientes:lista_pacientes')
        else:
            # Añadir este mensaje para depuración
            print(form.errors)  # Ver errores en consola
            messages.error(request, 'Hay errores en el formulario. Por favor, revise los campos.')
    else:
        form = PacienteForm(initial={
            'estado': 'activo',
            'fecha_registro': timezone.now().date()
        })

    context = {'form': form}
    return render(request, 'nuevo_paciente.html', context)

@login_required
def lista_pacientes(request):
    """Vista para mostrar la lista de pacientes"""
    # Filtros básicos
    estado = request.GET.get('estado', '')
    genero = request.GET.get('genero', '')
    
    pacientes = Paciente.objects.all()
    
    # Aplicar filtros si están presentes
    if estado:
        pacientes = pacientes.filter(estado=estado)
    if genero:
        pacientes = pacientes.filter(genero=genero)
    
    # Paginación
    paginator = Paginator(pacientes, 10)  # 10 pacientes por página
    page_number = request.GET.get('page', 1)
    pacientes_paginados = paginator.get_page(page_number)
    
    context = {
        'pacientes': pacientes_paginados,
        'filtros': {
            'estado': estado,
            'genero': genero
        }
    }
    return render(request, 'lista_pacientes.html', context)

@login_required
def buscar_paciente(request):
    """Vista para buscar pacientes con múltiples criterios"""
    query = request.GET.get('q', '')
    estado = request.GET.get('status', '')
    genero = request.GET.get('gender', '')
    fecha = request.GET.get('date', '')
    ciudad = request.GET.get('city', '')
    seguro = request.GET.get('insurance', '')
    edad_min = request.GET.get('age_min', '')
    edad_max = request.GET.get('age_max', '')
    
    pacientes = Paciente.objects.all()
    
    # Búsqueda por término general
    if query:
        pacientes = pacientes.filter(
            Q(nombres__icontains=query) | 
            Q(apellidos__icontains=query) | 
            Q(ci__icontains=query) | 
            Q(telefono__icontains=query) | 
            Q(email__icontains=query)
        )
    
    # Filtros adicionales
    if estado:
        pacientes = pacientes.filter(estado=estado)
    if genero:
        pacientes = pacientes.filter(genero=genero)
    if ciudad:
        pacientes = pacientes.filter(ciudad__icontains=ciudad)
    
    # Filtro por seguro
    if seguro == 'yes':
        pacientes = pacientes.filter(tiene_seguro=True)
    elif seguro == 'no':
        pacientes = pacientes.filter(tiene_seguro=False)
    
    # Filtro por fecha
    today = timezone.now().date()
    if fecha == 'today':
        pacientes = pacientes.filter(fecha_registro=today)
    elif fecha == 'week':
        # Inicio de semana (lunes)
        start_week = today - timezone.timedelta(days=today.weekday())
        pacientes = pacientes.filter(fecha_registro__gte=start_week)
    elif fecha == 'month':
        # Inicio de mes
        start_month = today.replace(day=1)
        pacientes = pacientes.filter(fecha_registro__gte=start_month)
    elif fecha == 'year':
        # Inicio de año
        start_year = today.replace(month=1, day=1)
        pacientes = pacientes.filter(fecha_registro__gte=start_year)
    
    # Filtro por edad (esto requiere un cálculo más complejo)
    # Para una implementación simple, podríamos filtrar por año de nacimiento
    
    context = {
        'pacientes': pacientes,
        'query': query,
        'filtros': {
            'estado': estado,
            'genero': genero,
            'fecha': fecha,
            'ciudad': ciudad,
            'seguro': seguro,
            'edad_min': edad_min,
            'edad_max': edad_max
        }
    }
    return render(request, 'buscar_paciente.html', context)

@login_required
def detalle_paciente(request, paciente_id):
    """Vista para mostrar los detalles de un paciente"""
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    # Aquí podemos cargar información adicional para el paciente
    # Por ejemplo, próximas citas, historial de visitas, etc.
    # Este código puede expandirse según necesites
    
    proxima_cita = None
    # Si tienes un modelo de Cita, podrías hacer algo como:
    # from apps.citas.models import Cita
    # try:
    #     proxima_cita = Cita.objects.filter(
    #         paciente=paciente, 
    #         fecha__gt=timezone.now()
    #     ).order_by('fecha').first()
    # except:
    #     pass
    
    context = {
        'paciente': paciente,
        'proxima_cita': proxima_cita,
        # Otros datos relacionados que necesites
    }
    
    return render(request, 'detalle_paciente.html', context)

@login_required
def editar_paciente(request, paciente_id):
    """Vista para editar los datos de un paciente"""
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES, instance=paciente)
        if form.is_valid():
            paciente = form.save()
            messages.success(request, f'Datos del paciente {paciente.get_nombre_completo()} actualizados correctamente')
            return redirect('pacientes:detalle_paciente', paciente_id=paciente.id)
    else:
        form = PacienteForm(instance=paciente)
    
    context = {
        'form': form,
        'paciente': paciente
    }
    return render(request, 'editar_paciente.html', context)

@login_required
def historia_clinica(request, paciente_id):
    """Vista para mostrar la historia clínica de un paciente"""
    # Esta vista la implementaremos más adelante cuando desarrollemos la app de historias clínicas
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    messages.info(request, 'Funcionalidad en desarrollo')
    return redirect('pacientes:detalle_paciente', paciente_id=paciente.id)

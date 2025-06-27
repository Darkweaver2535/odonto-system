from django.urls import path
from . import views

app_name = 'historias_clinicas'

urlpatterns = [
    # Vistas para seleccionar paciente
    path('anamnesis/', views.lista_pacientes_anamnesis, name='lista_pacientes_anamnesis'),
    path('examen-clinico/', views.lista_pacientes_examen_clinico, name='lista_pacientes_examen_clinico'),
    path('odontograma/', views.lista_pacientes_odontograma, name='lista_pacientes_odontograma'),
    
    # Vistas de anamnesis
    path('anamnesis/paciente/<int:paciente_id>/', views.historial_anamnesis, name='historial_anamnesis'),
    path('anamnesis/paciente/<int:paciente_id>/nueva/', views.nueva_anamnesis, name='nueva_anamnesis'),
    path('anamnesis/paciente/<int:paciente_id>/editar/<int:anamnesis_id>/', views.editar_anamnesis, name='editar_anamnesis'),
    
    # Vistas de examen clínico
    path('examen-clinico/paciente/<int:paciente_id>/', views.historial_examen_clinico, name='historial_examen_clinico'),
    path('examen-clinico/paciente/<int:paciente_id>/nuevo/', views.nuevo_examen_clinico, name='nuevo_examen_clinico'),
    path('examen-clinico/paciente/<int:paciente_id>/editar/<int:examen_id>/', views.editar_examen_clinico, name='editar_examen_clinico'),
    
    # Vistas de odontograma
    path('odontograma/paciente/<int:paciente_id>/', views.historial_odontograma, name='historial_odontograma'),
    path('odontograma/paciente/<int:paciente_id>/nuevo/', views.nuevo_odontograma, name='nuevo_odontograma'),
    path('odontograma/paciente/<int:paciente_id>/editar/<int:odontograma_id>/', views.editar_odontograma, name='editar_odontograma'),
    
    # Eliminar foto clínica
    path('examen-clinico/foto/<int:foto_id>/eliminar/', views.eliminar_foto_clinica, name='eliminar_foto_clinica'),
    
    # Nuevas URLs para vistas de detalle
    path('anamnesis/<int:paciente_id>/<int:anamnesis_id>/ver/', 
         views.detalle_anamnesis, 
         name='detalle_anamnesis'),
    
    path('examen-clinico/<int:paciente_id>/<int:examen_id>/ver/', 
         views.detalle_examen_clinico, 
         name='detalle_examen_clinico'),
    
    path('odontograma/<int:paciente_id>/<int:odontograma_id>/ver/', 
         views.detalle_odontograma, 
         name='detalle_odontograma'),
]
from django.urls import path
from . import views

app_name = 'pacientes'

urlpatterns = [
    path('nuevo/', views.nuevo_paciente, name='nuevo_paciente'),
    path('lista/', views.lista_pacientes, name='lista_pacientes'),
    path('buscar/', views.buscar_paciente, name='buscar_paciente'),
    path('detalle/<int:paciente_id>/', views.detalle_paciente, name='detalle_paciente'),
    path('editar/<int:paciente_id>/', views.editar_paciente, name='editar_paciente'),
    path('historia-clinica/<int:paciente_id>/', views.historia_clinica, name='historia_clinica'),
]
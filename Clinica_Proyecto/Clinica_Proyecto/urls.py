# Clinica_Proyecto/Clinica_Proyecto/urls.py

from django.contrib import admin
from django.urls import path, include # Importar include
from Clinica.views import (
    crear_paciente, index, paciente_edit, paciente_list, paciente_detail, paciente_delete,
    contacto_salud_create, contacto_salud_details, contacto_salud_edit, contacto_salud_delete, contacto_salud_list,
    register_view, login_view, logout_view, dashboard # Nuevas vistas
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),

    # Rutas de autenticación
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'), # Nueva ruta para el dashboard

    # Rutas existentes, ahora protegidas con @login_required en views.py
    path('pacientes/', paciente_list, name='paciente_list'),
    path('pacientes/<uuid:id>/', paciente_detail, name='paciente_detail'),
    path("pacientes/nuevo/", crear_paciente, name="paciente_create"),
    path("pacientes/<uuid:id>/eliminar/", paciente_delete, name="paciente_delete"),
    path("pacientes/<uuid:id>/editar/", paciente_edit, name="paciente_edit"),
    path('pacientes/<uuid:id_paciente>/contactos/', contacto_salud_list, name='contacto_salud_list'),
    path('pacientes/<uuid:id_paciente>/contactos/nuevo/', contacto_salud_create, name='contacto_salud_create'),
    path('pacientes/<uuid:id_paciente>/contactos/<uuid:id_contacto>/', contacto_salud_details, name='contacto_salud_details'),
    path('pacientes/<uuid:id_paciente>/contactos/<uuid:id_contacto>/editar/',contacto_salud_edit, name='contacto_salud_edit'),
    path('pacientes/<uuid:id_paciente>/contactos/<uuid:id_contacto>/eliminar/', contacto_salud_delete, name='contacto_salud_delete'),
]
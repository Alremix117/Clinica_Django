"""
URL configuration for Clinica_Proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Clinica.views import (
    crear_paciente, index, paciente_edit, paciente_list, paciente_detail, paciente_delete, contacto_salud_create, contacto_salud_details, contacto_salud_edit, contacto_salud_delete, contacto_salud_list
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
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
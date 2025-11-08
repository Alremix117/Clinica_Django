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
    PacienteListView, PacienteDeleteView,
    PacienteCreateView, PacienteUpdateView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("pacientes/", PacienteListView.as_view(), name="paciente_list"),
    path("pacientes/nuevo/", PacienteCreateView.as_view(), name="paciente_create"),
    path("pacientes/<uuid:pk>/editar/", PacienteUpdateView.as_view(), name="paciente_update"),
    path("pacientes/<uuid:pk>/eliminar/", PacienteDeleteView.as_view(), name="paciente_delete"),
]
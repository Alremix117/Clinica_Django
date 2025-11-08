from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Paciente, Paciente_Pais, Paciente_Discapacidad
from .forms import FormPaciente, FormNacionalidad, FormDiscapacidad

def index(request):
    return render(request, "index.html", {"message": "Bienvenido a la Clínica"})  # Puedes personalizar esta vista según tus necesidades

@transaction.atomic
def crear_paciente(request):
    if request.method == "POST":
        form_paciente = FormPaciente(request.POST)
        form_nacionalidad = FormNacionalidad(request.POST)
        form_discapacidad = FormDiscapacidad(request.POST)

        if form_paciente.is_valid() and form_nacionalidad.is_valid() and form_discapacidad.is_valid():
            paciente = form_paciente.save()

            for pais in form_nacionalidad.cleaned_data['paises']:
                Paciente_Pais.objects.create(paciente_UUID=paciente, codigo_pais=pais)

            for disc in form_discapacidad.cleaned_data['discapacidades']:
                Paciente_Discapacidad.objects.create(paciente_UUID=paciente, id_discapacidad=disc)

            return redirect("pacientes/paciente_list.html")  # Cambia a tu URL real
    else:
        form_paciente = FormPaciente()
        form_nacionalidad = FormNacionalidad()
        form_discapacidad = FormDiscapacidad()

    return render(request, "pacientes/paciente_form.html", {
        "form_paciente": form_paciente,
        "form_nacionalidad": form_nacionalidad,
        "form_discapacidad": form_discapacidad,
    })

@transaction.atomic
def paciente_edit(request, id):
    paciente = get_object_or_404(Paciente, paciente_UUID=id)

    if request.method == "POST":
        form_paciente = FormPaciente(request.POST, instance=paciente)
        form_nacionalidad = FormNacionalidad(request.POST)
        form_discapacidad = FormDiscapacidad(request.POST)

        if form_paciente.is_valid() and form_nacionalidad.is_valid() and form_discapacidad.is_valid():
            form_paciente.save()

            # Limpiar relaciones existentes
            Paciente_Pais.objects.filter(paciente_UUID=paciente).delete()
            Paciente_Discapacidad.objects.filter(paciente_UUID=paciente).delete()

            # Volver a guardar relaciones seleccionadas
            for pais in form_nacionalidad.cleaned_data['paises']:
                Paciente_Pais.objects.create(paciente_UUID=paciente, codigo_pais=pais)

            for disc in form_discapacidad.cleaned_data['discapacidades']:
                Paciente_Discapacidad.objects.create(paciente_UUID=paciente, id_discapacidad=disc)

            return redirect("paciente_detail", id=paciente.paciente_UUID)

    else:
        nacionalidades_actuales = paciente.nacionalidad.values_list('codigo_pais', flat=True)
        discapacidades_actuales = paciente.discapacidades.values_list('id_discapacidad', flat=True)

        form_paciente = FormPaciente(instance=paciente)
        form_nacionalidad = FormNacionalidad(initial={'paises': nacionalidades_actuales})
        form_discapacidad = FormDiscapacidad(initial={'discapacidades': discapacidades_actuales})

    return render(request, "pacientes/paciente_edit.html", {
        "form_paciente": form_paciente,
        "form_nacionalidad": form_nacionalidad,
        "form_discapacidad": form_discapacidad,
        "paciente": paciente,
    })

def paciente_delete(request, id):
    paciente = get_object_or_404(Paciente, paciente_UUID=id)

    if request.method == "POST":
        paciente.delete()
        return redirect("paciente_list")

    return render(request, "pacientes/paciente_eliminar_confirmacion.html", {
        "paciente": paciente
    })

def paciente_list(request):
    pacientes = Paciente.objects.all()
    return render(request, "pacientes/paciente_list.html", {"pacientes": pacientes})

def paciente_detail(request, id):
    paciente = get_object_or_404(Paciente, paciente_UUID=id)
    nacionalidades = paciente.nacionalidad.all()
    discapacidades = paciente.discapacidades.all()

    return render(request, "pacientes/paciente_details.html", {
        "paciente": paciente,
        "nacionalidades": nacionalidades,
        "discapacidades": discapacidades,
    })


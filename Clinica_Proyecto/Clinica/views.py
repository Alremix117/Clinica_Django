from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required # Importar para proteger vistas

from .models import Paciente, Paciente_Pais, Paciente_Discapacidad, Voluntad_Anticipada, Oposicion_Donacion , Contacto_Servicio_Salud
from .forms import FormPaciente, FormNacionalidad, FormDiscapacidad, FormVoluntadAnticipada, FormOposicionDonacion, FormContactoSalud, FormPacienteEdit

def index(request):
    return render(request, "index.html", {"message": "Bienvenido a la Clínica"})

@login_required # Protegida
@transaction.atomic
def crear_paciente(request):
    if request.method == "POST":
        form_paciente = FormPaciente(request.POST)
        form_nacionalidad = FormNacionalidad(request.POST)
        form_discapacidad = FormDiscapacidad(request.POST)
        form_voluntad = FormVoluntadAnticipada(request.POST)
        form_oposicion = FormOposicionDonacion(request.POST)

        if form_paciente.is_valid() and form_nacionalidad.is_valid() and form_discapacidad.is_valid() and form_voluntad.is_valid() and form_oposicion.is_valid():
            paciente = form_paciente.save()
            Voluntad_Anticipada_obj = form_voluntad.save(commit=False)
            Voluntad_Anticipada_obj.paciente_UUID = paciente
            Voluntad_Anticipada_obj.save()
            Oposicion_Donacion_obj = form_oposicion.save(commit=False)
            Oposicion_Donacion_obj.paciente_UUID = paciente
            Oposicion_Donacion_obj.save()

            for pais in form_nacionalidad.cleaned_data['paises']:
                Paciente_Pais.objects.create(paciente_UUID=paciente, codigo_pais=pais)

            for disc in form_discapacidad.cleaned_data['discapacidades']:
                Paciente_Discapacidad.objects.create(paciente_UUID=paciente, id_discapacidad=disc)

            return redirect(paciente_list)  # Cambia a tu URL real
    else:
        form_paciente = FormPaciente()
        form_nacionalidad = FormNacionalidad()
        form_discapacidad = FormDiscapacidad()
        form_voluntad = FormVoluntadAnticipada()
        form_oposicion = FormOposicionDonacion()

    return render(request, "pacientes/paciente_form.html", {
        "form_paciente": form_paciente,
        "form_nacionalidad": form_nacionalidad,
        "form_discapacidad": form_discapacidad,
        "form_voluntad": form_voluntad,
        "form_oposicion": form_oposicion,
    })

@login_required # Protegida
@transaction.atomic
def paciente_edit(request, id):
    paciente = get_object_or_404(Paciente, paciente_UUID=id)

    if request.method == "POST":
        form_paciente = FormPacienteEdit(request.POST, instance=paciente)
        form_nacionalidad = FormNacionalidad(request.POST)
        form_discapacidad = FormDiscapacidad(request.POST)
        form_voluntad = FormVoluntadAnticipada(request.POST, instance=paciente)
        form_oposicion = FormOposicionDonacion(request.POST, instance=paciente)

        if form_paciente.is_valid() and form_nacionalidad.is_valid() and form_discapacidad.is_valid():
            form_paciente.save() # Guardamos los datos del paciente

            # Limpiar relaciones existentes
            Paciente_Pais.objects.filter(paciente_UUID=paciente).delete()
            Paciente_Discapacidad.objects.filter(paciente_UUID=paciente).delete()

            # Volver a guardar relaciones seleccionadas
            for pais in form_nacionalidad.cleaned_data['paises']:
                Paciente_Pais.objects.create(paciente_UUID=paciente, codigo_pais=pais)

            for disc in form_discapacidad.cleaned_data['discapacidades']:
                Paciente_Discapacidad.objects.create(paciente_UUID=paciente, id_discapacidad=disc)

            # Actualizar Voluntad Anticipada y Oposición a Donación
            Voluntad_Anticipada_obj, created = Voluntad_Anticipada.objects.get_or_create(paciente_UUID=paciente)
            Oposicion_Donacion_obj, created = Oposicion_Donacion.objects.get_or_create(paciente_UUID=paciente)

            form_voluntad = FormVoluntadAnticipada(request.POST, instance=Voluntad_Anticipada_obj)
            form_oposicion = FormOposicionDonacion(request.POST, instance=Oposicion_Donacion_obj)

            if form_voluntad.is_valid() and form_oposicion.is_valid():
                form_voluntad.save()
                form_oposicion.save()
                return redirect("paciente_detail", id=paciente.paciente_UUID)
            else:
                # Aquí puedes manejar los errores de los formularios de Voluntad y Oposición
                pass # Por ahora, solo pasamos

    else:
        nacionalidades_actuales = paciente.nacionalidad.values_list('codigo_pais', flat=True)
        discapacidades_actuales = paciente.discapacidades.values_list('id_discapacidad', flat=True)

        form_paciente = FormPacienteEdit(instance=paciente)
        form_nacionalidad = FormNacionalidad(initial={'paises': nacionalidades_actuales})
        form_discapacidad = FormDiscapacidad(initial={'discapacidades': discapacidades_actuales})

        # Obtener o crear instancias para Voluntad Anticipada y Oposición Donación
        voluntad_anticipada_instance, created = Voluntad_Anticipada.objects.get_or_create(paciente_UUID=paciente)
        oposicion_donacion_instance, created = Oposicion_Donacion.objects.get_or_create(paciente_UUID=paciente)

        form_voluntad = FormVoluntadAnticipada(instance=voluntad_anticipada_instance)
        form_oposicion = FormOposicionDonacion(instance=oposicion_donacion_instance)

    return render(request, "pacientes/paciente_edit.html", {
        "form_paciente": form_paciente,
        "form_nacionalidad": form_nacionalidad,
        "form_discapacidad": form_discapacidad,
        "paciente": paciente,
        "form_voluntad": form_voluntad,
        "form_oposicion": form_oposicion,
    })

@login_required # Protegida
def paciente_delete(request, id):
    paciente = get_object_or_404(Paciente, paciente_UUID=id)

    if request.method == "POST":
        paciente.delete()
        return redirect("paciente_list")

    return render(request, "pacientes/paciente_eliminar_confirmacion.html", {
        "paciente": paciente
    })

@login_required # Protegida
def paciente_list(request):
    pacientes = Paciente.objects.all()
    return render(request, "pacientes/paciente_list.html", {"pacientes": pacientes})

@login_required # Protegida
def paciente_detail(request, id):
    paciente = get_object_or_404(Paciente, paciente_UUID=id)
    nacionalidades = paciente.nacionalidad.all()
    discapacidades = paciente.discapacidades.all()
    # Asegúrate de que Voluntad_Anticipada y Oposicion_Donacion existen o créalas
    voluntad = Voluntad_Anticipada.objects.filter(paciente_UUID=paciente).first()
    oposicion = Oposicion_Donacion.objects.filter(paciente_UUID=paciente).first()


    return render(request, "pacientes/paciente_details.html", {
        "paciente": paciente,
        "nacionalidades": nacionalidades,
        "discapacidades": discapacidades,
        "voluntad": voluntad,
        "oposicion": oposicion,
    })

#contacto servicio de salud
# 📋 LISTAR CONTACTOS POR PACIENTE
@login_required # Protegida
def contacto_salud_list(request, id_paciente):
    paciente = get_object_or_404(Paciente, paciente_UUID=id_paciente)
    contactos = Contacto_Servicio_Salud.objects.filter(paciente_UUID=paciente).order_by('-fecha_hora_inicio_atencion')

    return render(request, "contacto_salud/contacto_salud_list.html", {
        "paciente": paciente,
        "contactos": contactos,
    })


# ➕ CREAR CONTACTO
@login_required # Protegida
@transaction.atomic
def contacto_salud_create(request, id_paciente):
    paciente = get_object_or_404(Paciente, paciente_UUID=id_paciente)

    if request.method == "POST":
        form = FormContactoSalud(request.POST)
        if form.is_valid():
            contacto = form.save(commit=False)
            contacto.paciente_UUID = paciente  # Relación explícita
            contacto.save()
            return redirect("contacto_salud_list", id_paciente=paciente.paciente_UUID)
    else:
        form = FormContactoSalud()

    return render(request, "contacto_salud/contacto_salud_form.html", {
        "form": form,
        "paciente": paciente,
        "titulo": "Registrar nuevo contacto de salud",
    })


# ✏️ EDITAR CONTACTO
@login_required # Protegida
@transaction.atomic
def contacto_salud_edit(request, id_paciente, id_contacto):
    paciente = get_object_or_404(Paciente, paciente_UUID=id_paciente)
    contacto = get_object_or_404(Contacto_Servicio_Salud, id_contacto_UUID=id_contacto, paciente_UUID=paciente)

    if request.method == "POST":
        form = FormContactoSalud(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect("contacto_salud_list", id_paciente=paciente.paciente_UUID)
    else:
        form = FormContactoSalud(instance=contacto)

    return render(request, "contacto_salud/contacto_salud_edit.html", {
        "form": form,
        "paciente": paciente,
        "contacto": contacto,
        "titulo": "Editar contacto de salud",
    })


# 👁️ DETALLE DE CONTACTO
@login_required # Protegida
def contacto_salud_details(request, id_paciente, id_contacto):
    paciente = get_object_or_404(Paciente, paciente_UUID=id_paciente)
    contacto = get_object_or_404(Contacto_Servicio_Salud, id_contacto_UUID=id_contacto, paciente_UUID=paciente)

    return render(request, "contacto_salud/contacto_salud_details.html", {
        "paciente": paciente,
        "contacto": contacto,
    })


# ❌ ELIMINAR CONTACTO
@login_required # Protegida
@transaction.atomic
def contacto_salud_delete(request, id_paciente, id_contacto):
    paciente = get_object_or_404(Paciente, paciente_UUID=id_paciente)
    contacto = get_object_or_404(Contacto_Servicio_Salud, id_contacto_UUID=id_contacto, paciente_UUID=paciente)

    if request.method == "POST":
        contacto.delete()
        return redirect("contacto_salud_list", id_paciente=paciente.paciente_UUID)

    return render(request, "contacto_salud/contacto_salud_eliminar_confirmacion.html", {
        "paciente": paciente,
        "contacto": contacto,
    })

# Vistas de Autenticación
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Iniciar sesión automáticamente después del registro
            return redirect('dashboard') # Redirigir a una página de bienvenida para usuarios
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form, 'title': 'Registro de Usuario'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard') # Redirigir al dashboard después del login
            else:
                # Opcional: añadir un mensaje de error si la autenticación falla
                pass
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form, 'title': 'Iniciar Sesión'})

@login_required # Protege esta vista, solo accesible para usuarios autenticados
def logout_view(request):
    logout(request)
    return redirect('index') # Redirigir a la página principal

@login_required
def dashboard(request):
    """
    Página de bienvenida para usuarios logeados.
    Desde aquí pueden navegar a Pacientes o Contactos de Salud.
    """
    return render(request, 'dashboard.html', {'user': request.user, 'title': 'Dashboard'})
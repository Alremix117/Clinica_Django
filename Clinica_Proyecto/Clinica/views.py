# views.py
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
# from django.contrib.auth.mixins import LoginRequiredMixin  # opcional

from .models import Paciente
from .forms import (
    PacienteForm,
    PacientePaisFormSet,
    PacienteDiscapacidadFormSet,
)

# ----------------------------------------------------------------------
# Mixin para manejar Inline Formsets con transacciones y validación clara
# ----------------------------------------------------------------------
class PacienteMixinFormsets:
    """
    Mixin para manejar inline formsets en Create/Update del Paciente.
    - Construye formsets con prefijos explícitos (evita colisiones).
    - Valida y guarda todo de forma atómica.
    - Expone los formsets en el contexto como `paises_formset` y `discapacidad_formset`.
    """

    paises_prefix = "paises"
    disc_prefix = "discapacidades"

    def build_formsets(self, post_data=None):
        """
        Construye los formsets con o sin datos POST.
        Usa prefijos explícitos para evitar colisiones.
        """
        kwargs = {"instance": self.object}
        if post_data is not None:
            kwargs["data"] = post_data

        paises_fs = PacientePaisFormSet(prefix=self.paises_prefix, **kwargs)
        disc_fs = PacienteDiscapacidadFormSet(prefix=self.disc_prefix, **kwargs)
        return paises_fs, disc_fs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Reutiliza formsets ya creados en POST; si no, crea nuevos
        paises_fs = kwargs.get("paises_formset")
        disc_fs = kwargs.get("discapacidad_formset")
        if not (paises_fs and disc_fs):
            paises_fs, disc_fs = self.build_formsets()
        ctx["paises_formset"] = paises_fs
        ctx["discapacidad_formset"] = disc_fs
        return ctx

    def validate_formsets(self, paises_fs, disc_fs):
        """
        Punto único para validaciones extra de negocio si las necesitas.
        Retorna (bool, error_message|None).
        """
        # Ejemplo: exigir al menos una nacionalidad
        # count_valid = sum(1 for f in paises_fs.forms
        #                   if f.cleaned_data and not f.cleaned_data.get("DELETE", False) and f.cleaned_data.get("pais"))
        # if count_valid < 1:
        #     return False, "Debe registrar al menos una nacionalidad."
        return True, None

    def save_formsets(self, paises_fs, disc_fs):
        """
        Guarda formsets. Separado para que sea testeable y extensible.
        """
        paises_fs.save()
        disc_fs.save()

    def post(self, request, *args, **kwargs):
        # Prepara self.object según Create/Update
        if isinstance(self, CreateView):
            self.object = None
        else:
            self.object = self.get_object()

        form = self.get_form()
        paises_fs, disc_fs = self.build_formsets(post_data=request.POST)

        # Validación integral: form y formsets
        if not (form.is_valid() and paises_fs.is_valid() and disc_fs.is_valid()):
            messages.error(self.request, "Por favor corrige los errores en el formulario.")
            return self.form_invalid(form=form, paises_formset=paises_fs, discapacidad_formset=disc_fs)

        # Validaciones de negocio adicionales
        ok, err = self.validate_formsets(paises_fs, disc_fs)
        if not ok:
            if err:
                messages.error(self.request, err)
            return self.form_invalid(form=form, paises_formset=paises_fs, discapacidad_formset=disc_fs)

        # Guarda todo de forma atómica
        with transaction.atomic():
            response = self.form_valid(form)   # guarda Paciente
            # Asegura que los formsets apunten al paciente recién guardado
            paises_fs.instance = self.object
            disc_fs.instance = self.object
            self.save_formsets(paises_fs, disc_fs)
        return response

    # Permite pasar formsets a form_invalid y re-renderizar
    def form_invalid(self, form, **kwargs):
        return self.render_to_response(self.get_context_data(form=form, **kwargs))


# ------------------------ READ: listar pacientes ------------------------
class PacienteListView(ListView):
    model = Paciente
    template_name = "pacientes/paciente_list.html"
    context_object_name = "pacientes"
    paginate_by = 20  # opcional

    def get_queryset(self):
        qs = (Paciente.objects
              .select_related(
                  "tipo_documento", "residencia", "ocupacion",
                  "etnia", "comunidad_Etnica", "entidad_prestadora_salud"
              )
              .prefetch_related("nacionalidad", "discapacidades")
              .order_by("primer_apellido", "primer_nombre"))
        q = self.request.GET.get("q")
        if q:
            from django.db.models import Q
            qs = qs.filter(
                Q(numero_documento__icontains=q) |
                Q(primer_nombre__icontains=q) |
                Q(segundo_nombre__icontains=q) |
                Q(primer_apellido__icontains=q) |
                Q(segundo_apellido__icontains=q)
            )
        return qs


# ------------------------ DELETE: eliminar paciente ---------------------
class PacienteDeleteView(SuccessMessageMixin, DeleteView):
    model = Paciente
    template_name = "pacientes/paciente_confirm_delete.html"
    success_url = reverse_lazy("paciente_list")
    success_message = "Paciente eliminado correctamente."

    def get_queryset(self):
        return (super().get_queryset()
                .select_related(
                    "tipo_documento", "residencia", "ocupacion",
                    "etnia", "comunidad_Etnica", "entidad_prestadora_salud")
                .prefetch_related("nacionalidad", "discapacidades"))


# ------------------------ CREATE: crear paciente ------------------------
class PacienteCreateView(SuccessMessageMixin, PacienteMixinFormsets, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "pacientes/paciente_form.html"
    success_url = reverse_lazy("paciente_list")
    success_message = "Paciente creado correctamente."


# ------------------------ UPDATE: actualizar paciente -------------------
class PacienteUpdateView(SuccessMessageMixin, PacienteMixinFormsets, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "pacientes/paciente_form.html"
    success_url = reverse_lazy("paciente_list")
    success_message = "Paciente actualizado correctamente."

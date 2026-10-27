from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PerfilForm, RecetaForm
from .models import Perfil, Receta


def _puede_editar(user, receta):
    return user.is_superuser or receta.autor_id == user.id


# ===== INDEX (listado + búsqueda) =====
@login_required
def index(request):
    q = request.GET.get("q", "").strip()
    recetas = Receta.objects.select_related("autor").prefetch_related("tags")
    if q:
        recetas = recetas.filter(
            Q(nombre__icontains=q)
            | Q(tags__nombre__icontains=q)
            | Q(ingredientes__icontains=q)
        ).distinct()
    return render(request, "recetas/index.html", {"recetas": recetas, "q": q})


# ===== CONSULTA (detalle) =====
@login_required
def detalle(request, pk):
    receta = get_object_or_404(
        Receta.objects.select_related("autor").prefetch_related("tags"), pk=pk
    )
    contexto = {
        "receta": receta,
        "form": RecetaForm(instance=receta),
        "puede_editar": _puede_editar(request.user, receta),
    }
    return render(request, "recetas/detalle.html", contexto)


# ===== ALTA =====
def _contexto_perfil(request, form_nueva=None, tab="mis"):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    u = request.user
    return {
        "perfil": perfil,
        "form_perfil": PerfilForm(
            initial={
                "nombre": u.first_name,
                "usuario": u.username,
                "email": u.email,
                "bio": perfil.bio,
            },
            user=u,
        ),
        "form_nueva": form_nueva or RecetaForm(),
        "mis_recetas": Receta.objects.filter(autor=u)
        .select_related("autor")
        .prefetch_related("tags"),
        "tab": tab,
    }


@login_required
def perfil(request):
    tab = "nueva" if request.GET.get("tab") == "nueva" else "mis"
    return render(request, "recetas/perfil.html", _contexto_perfil(request, tab=tab))


@login_required
@require_POST
def receta_crear(request):
    form = RecetaForm(request.POST)
    if form.is_valid():
        receta = form.save(commit=False)
        receta.autor = request.user
        receta.save()
        form.save_m2m()
        messages.success(request, "🎉 Receta publicada")
        return redirect("perfil")
    messages.error(request, "❌ Completá los campos obligatorios")
    return render(
        request, "recetas/perfil.html", _contexto_perfil(request, form, tab="nueva")
    )


# ===== MODIFICACIÓN =====
@login_required
@require_POST
def receta_editar(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    if not _puede_editar(request.user, receta):
        raise PermissionDenied
    form = RecetaForm(request.POST, instance=receta)
    if form.is_valid():
        form.save()
        messages.success(request, "✅ Receta actualizada")
    else:
        messages.error(request, "❌ No se pudo guardar: revisá nombre, ingredientes y pasos")
    return redirect("detalle", pk=receta.pk)


# ===== BAJA =====
@login_required
@require_POST
def receta_eliminar(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    if not _puede_editar(request.user, receta):
        raise PermissionDenied
    receta.delete()
    messages.success(request, "🗑️ Receta eliminada")
    return redirect("index")


# ===== PERFIL: editar =====
@login_required
@require_POST
def perfil_editar(request):
    form = PerfilForm(request.POST, user=request.user)
    if form.is_valid():
        u = request.user
        u.first_name = form.cleaned_data["nombre"]
        u.username = form.cleaned_data["usuario"]
        u.email = form.cleaned_data["email"]
        u.save()
        perfil, _ = Perfil.objects.get_or_create(user=u)
        perfil.bio = form.cleaned_data["bio"]
        perfil.save()
        messages.success(request, "✅ Perfil actualizado")
    else:
        messages.error(request, "❌ " + " ".join(sum(form.errors.values(), [])))
    return redirect("perfil")

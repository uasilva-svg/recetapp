from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="recetas/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.index, name="index"),
    path("receta/nueva/", views.receta_crear, name="receta_crear"),
    path("receta/<int:pk>/", views.detalle, name="detalle"),
    path("receta/<int:pk>/editar/", views.receta_editar, name="receta_editar"),
    path("receta/<int:pk>/eliminar/", views.receta_eliminar, name="receta_eliminar"),
    path("perfil/", views.perfil, name="perfil"),
    path("perfil/editar/", views.perfil_editar, name="perfil_editar"),
]

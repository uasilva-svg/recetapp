from django import forms
from django.contrib.auth import get_user_model

from .models import Receta, Tag

User = get_user_model()


def _limpiar_lineas(texto):
    return "\n".join(l.strip() for l in texto.splitlines() if l.strip())


class RecetaForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Categorías / hashtags",
    )

    class Meta:
        model = Receta
        fields = ["nombre", "emoji", "ingredientes", "pasos", "nota", "tags"]
        labels = {
            "nombre": "Nombre de la receta *",
            "emoji": "Emoji de portada",
            "ingredientes": "Ingredientes * (uno por línea)",
            "pasos": "Pasos * (uno por línea)",
            "nota": "Nota (opcional)",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Ej: Pasta primavera"}),
            "ingredientes": forms.Textarea(
                attrs={"placeholder": "200g de pasta\n1 tomate\nSal y pimienta"}
            ),
            "pasos": forms.Textarea(
                attrs={"placeholder": "Hervir el agua\nCocinar la pasta 10 min\nMezclar con la salsa"}
            ),
            "nota": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_ingredientes(self):
        valor = _limpiar_lineas(self.cleaned_data["ingredientes"])
        if not valor:
            raise forms.ValidationError("Agregá al menos un ingrediente.")
        return valor

    def clean_pasos(self):
        valor = _limpiar_lineas(self.cleaned_data["pasos"])
        if not valor:
            raise forms.ValidationError("Agregá al menos un paso.")
        return valor


class PerfilForm(forms.Form):
    nombre = forms.CharField(label="Nombre completo", max_length=150, required=False)
    usuario = forms.CharField(label="Usuario", max_length=150)
    email = forms.EmailField(label="Email", required=False)
    bio = forms.CharField(label="Bio", required=False, widget=forms.Textarea)

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_usuario(self):
        usuario = self.cleaned_data["usuario"].strip()
        existe = User.objects.filter(username=usuario).exclude(pk=self.user.pk).exists()
        if existe:
            raise forms.ValidationError("Ese usuario ya está en uso.")
        return usuario

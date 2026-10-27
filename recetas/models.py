from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Tag(models.Model):
    nombre = models.CharField(max_length=30, unique=True)  # ej: "#rápido"
    slug = models.SlugField(max_length=30, unique=True)    # ej: "rapido" (clase CSS)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil"
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"


class Receta(models.Model):
    EMOJIS = [
        ("🍝", "🍝 Pasta"), ("🥗", "🥗 Ensalada"), ("🍕", "🍕 Pizza"),
        ("🍜", "🍜 Sopa"), ("🥘", "🥘 Guiso"), ("🧁", "🧁 Postre"),
        ("🍳", "🍳 Huevos"), ("🥩", "🥩 Carne"), ("🐟", "🐟 Pescado"),
        ("🫔", "🫔 Wrap"), ("🥟", "🥟 Empanadas"), ("🌮", "🌮 Tacos"),
        ("🍮", "🍮 Flan"), ("🍫", "🍫 Chocolate"), ("🍨", "🍨 Helado"),
        ("🥞", "🥞 Panqueques"), ("🍰", "🍰 Torta"), ("🍋", "🍋 Limón"),
        ("🥒", "🥒 Verdura"),
    ]

    nombre = models.CharField(max_length=120)
    emoji = models.CharField(max_length=8, choices=EMOJIS, default="🍝")
    ingredientes = models.TextField(
        help_text="Uno por línea. Una línea que empiece con '## ' es un subtítulo."
    )
    pasos = models.TextField(help_text="Uno por línea.")
    nota = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="recetas")
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recetas"
    )
    fecha = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("detalle", args=[self.pk])

    @property
    def ingredientes_lista(self):
        items = []
        for linea in self.ingredientes.splitlines():
            linea = linea.strip()
            if not linea:
                continue
            if linea.startswith("## "):
                items.append({"texto": linea[3:], "titulo": True})
            else:
                items.append({"texto": linea, "titulo": False})
        return items

    @property
    def pasos_lista(self):
        return [p.strip() for p in self.pasos.splitlines() if p.strip()]

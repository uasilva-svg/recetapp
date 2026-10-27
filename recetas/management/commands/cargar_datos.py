import json
from datetime import date
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from recetas.models import Perfil, Receta, Tag

MESES = {
    "ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
    "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12,
}
TAGS = [
    ("#vegano", "vegano"),
    ("#vegetariano", "vegetariano"),
    ("#sin-gluten", "sin-gluten"),
    ("#rápido", "rapido"),
    ("#dulce", "dulce"),
    ("#salado", "salado"),
]


def parsear_fecha(texto):
    dia, mes, anio = texto.split()
    return date(int(anio), MESES[mes[:3].lower()], int(dia))


class Command(BaseCommand):
    help = "Crea el usuario admin (clave 1234), las categorías y las 21 recetas."

    def handle(self, *args, **options):
        User = get_user_model()

        admin, creado = User.objects.get_or_create(
            username="admin",
            defaults={
                "first_name": "Admin Chef",
                "email": "admin@recetapp.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if creado:
            admin.set_password("1234")
            admin.save()
        Perfil.objects.get_or_create(
            user=admin, defaults={"bio": "Amante de la cocina y las recetas caseras."}
        )

        tags = {}
        for nombre, slug in TAGS:
            tags[nombre], _ = Tag.objects.get_or_create(nombre=nombre, defaults={"slug": slug})

        ruta = Path(__file__).resolve().parents[2] / "data" / "recetas.json"
        datos = json.loads(ruta.read_text(encoding="utf-8"))

        nuevas = 0
        for d in datos:
            receta, creada = Receta.objects.update_or_create(
                nombre=d["nombre"],
                defaults={
                    "emoji": d["emoji"],
                    "ingredientes": "\n".join(d["ingredientes"]),
                    "pasos": "\n".join(d["pasos"]),
                    "nota": d.get("nota", ""),
                    "autor": admin,
                    "fecha": parsear_fecha(d["fecha"]),
                },
            )
            receta.tags.set([tags[t] for t in d["tags"]])
            nuevas += creada

        self.stdout.write(
            self.style.SUCCESS(
                f"Listo: {len(datos)} recetas ({nuevas} nuevas). Usuario: admin / Contraseña: 1234"
            )
        )

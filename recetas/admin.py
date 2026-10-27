from django.contrib import admin

from .models import Perfil, Receta, Tag


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "emoji", "autor", "fecha")
    search_fields = ("nombre", "ingredientes")
    list_filter = ("tags", "autor")


admin.site.register(Tag)
admin.site.register(Perfil)

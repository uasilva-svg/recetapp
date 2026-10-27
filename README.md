# RecetApp (Django)

Recetario con login y ABM completo de recetas (Alta, Baja, Modificación y Consulta).

## Puesta en marcha

```bash
python -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations recetas
python manage.py migrate
python manage.py cargar_datos     # crea admin/1234 y las 21 recetas
python manage.py runserver
```

Abrir http://127.0.0.1:8000/ e ingresar con **admin / 1234**.

## Qué incluye

- **Login / logout** con el sistema de autenticación de Django.
- **Inicio**: listado de recetas con buscador (nombre, ingrediente o categoría).
- **Consulta**: detalle de la receta con ingredientes, pasos y nota.
- **Alta**: pestaña "Nueva receta" en el perfil.
- **Modificación / Baja**: botones Editar y Eliminar en el detalle (solo el autor o un superusuario).
- **Perfil**: ver y editar nombre, usuario, email y bio.
- **Panel /admin/** de Django para administrar recetas, categorías y usuarios.

## Estructura

```
config/            configuración del proyecto
recetas/
  models.py        Receta, Tag, Perfil
  forms.py         RecetaForm, PerfilForm
  views.py         vistas del ABM
  urls.py
  data/recetas.json   las 21 recetas
  management/commands/cargar_datos.py
  templates/recetas/  HTML
  static/recetas/     CSS y JS
```
# recetapp
# recetapp

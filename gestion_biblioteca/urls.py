# urls.py de la aplicación

from django.urls import path
from .admin import admin_site  # Importa la instancia personalizada de admin

urlpatterns = [
    path('', admin_site.urls),  # Usa la instancia personalizada de admin
]

# admin.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count
from .models import Reserva, Prestamo, Reporte, Sancion, Libro
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission, ContentType


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'codename')

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('username', 'nombres', 'telefono', 'email', 'cedula', 'is_staff')
    
    # Definición de los campos en el formulario de edición
    fieldsets = (
        (None, {'fields': ('username', 'nombres', 'telefono', 'email', 'cedula', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'updated')}),
    )
    
    # Agregar todos los campos en el formulario de creación
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 
                'nombres', 
                'telefono', 
                'email', 
                'cedula', 
                'password1', 
                'password2', 
                'is_active', 
                'is_staff', 
                'is_superuser', 
                'groups', 
                'user_permissions',
                'created',  # Si deseas mostrar también el campo creado, asegúrate de que esté bien
                'updated'   # Aunque este campo generalmente no se debería incluir en la creación
            ),
        }),
    )
    
    search_fields = ('username', 'email', 'cedula')
    ordering = ('username',)


class BibliotecaAdminSite(admin.AdminSite):
    site_header = "Administración de la Biblioteca"
    site_title = "Panel de Control"
    index_title = "Bienvenido al Panel de Administración de la Biblioteca"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('estadisticas/', self.admin_view(self.estadisticas_view), name="estadisticas"),
        ]
        return custom_urls + urls

    def estadisticas_view(self, request):
        # Obtener la cantidad de reservas activas
        reservas_activas = Reserva.objects.filter(activa=True).values('libro__titulo').annotate(cantidad=Count('id'))

        # Obtener la cantidad de libros en préstamo
        libros_en_prestamo = Prestamo.objects.filter(devuelto=False).values('libro__titulo').annotate(cantidad=Count('id'))

        return render(request, 'admin/estadisticas.html', {
            'reservas_activas': reservas_activas,
            'libros_en_prestamo': libros_en_prestamo,
        })

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['estadisticas_url'] = f"{request.path}estadisticas/"  # Corrige aquí
        return super().index(request, extra_context=extra_context)

admin_site = BibliotecaAdminSite(name='biblioteca_admin')

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion', 'archivo')


admin_site = BibliotecaAdminSite(name='biblioteca_admin')
admin_site.register(CustomUser, BaseUserAdmin)
admin_site.register(Permission,PermissionAdmin)
admin_site.register(ContentType)
admin_site.register(Reserva)
admin_site.register(Reporte)
admin_site.register(Libro)
admin_site.register(Prestamo)
admin_site.register(Sancion)  # Registrar el modelo de sanciones

# Agrega el botón de estadísticas en la plantilla del índice
admin_site.index_template = 'admin/index.html'

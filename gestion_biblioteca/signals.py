# signals.py

import csv
from io import StringIO
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from .models import Prestamo, Reporte, Sancion
from django.utils import timezone

@receiver(post_save, sender=Prestamo)
def generar_reporte_prestamo(sender, instance, created, **kwargs):
    if created:
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Usuario', 'Libro', 'Fecha de Préstamo', 'Fecha de Devolución', 'Devuelto'])

        writer.writerow([
            instance.usuario.username,
            instance.libro.titulo,
            instance.fecha_prestamo.strftime("%Y-%m-%d %H:%M:%S"),
            instance.fecha_devolucion.strftime("%Y-%m-%d %H:%M:%S") if instance.fecha_devolucion else "N/A",
            "Sí" if instance.devuelto else "No"
        ])

        reporte = Reporte.objects.create(nombre=f"Reporte Préstamo {instance.id}")
        reporte.archivo.save(f"reporte_prestamo_{instance.id}.csv", ContentFile(output.getvalue()))
        output.close()

@receiver(post_save, sender=Prestamo)
def registrar_sancion(sender, instance, created, **kwargs):
    if not created and instance.devuelto:  # Solo para actualizaciones
        if instance.is_late():  # Verifica si el préstamo está atrasado
            sancion = Sancion.objects.create(
                prestamo=instance,
                cantidad=5.00  # Monto de la sanción, puedes ajustarlo según tus necesidades
            )
            # Puedes agregar lógica adicional, como enviar notificaciones, etc.

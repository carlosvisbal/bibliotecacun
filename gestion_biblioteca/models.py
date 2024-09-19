from django.db import models
from django.utils import timezone
from users.models import CustomUser

class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    cantidad = models.IntegerField()
    disponible = models.IntegerField()

    def __str__(self):
        return self.titulo

class Reporte(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='reportes/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Prestamo(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(blank=True, null=True)
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.libro} prestado a {self.usuario}'

    def is_late(self):
        if self.fecha_devolucion and self.devuelto:
            return timezone.now() > self.fecha_devolucion
        return False

class Sancion(models.Model):
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE)
    fecha_sancion = models.DateTimeField(auto_now_add=True)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2)  # Monto de la sanción

    def __str__(self):
        return f"Sanción por préstamo {self.prestamo.id} - ${self.cantidad}"

class Reserva(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.libro} reservado por {self.usuario}'

    
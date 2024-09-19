from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(unique=True, max_length=300, null=False)
    nombres = models.CharField(max_length=300)
    telefono = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    cedula = models.CharField(max_length=15, null=True, blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    # Adding related_name for groups and user_permissions
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Unique related name for this model
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',  # Unique related name for this model
        blank=True,
    )

    class Meta:
        verbose_name = "Usuario"
        db_table = 'user_usuarios'

    def __str__(self):
        return str(self.username)

"""Modelo de usuario con roles del simulador."""

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.accounts.managers import UserManager


class User(AbstractUser):
    """Usuario del sistema con correo único y rol de acceso."""

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        USUARIO = "USUARIO", "Usuario registrado"

    email = models.EmailField("correo electrónico", unique=True)
    role = models.CharField(
        "rol",
        max_length=10,
        choices=Role.choices,
        default=Role.USUARIO,
        help_text="Determina las vistas y acciones permitidas.",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ["email"]

    def __str__(self):
        """Representación legible usada en el admin y las plantillas."""
        return self.email

    def save(self, *args, **kwargs):
        """Sincroniza el acceso al admin cuando el rol es Administrador."""
        self.email = self.email.strip().lower()
        if self.role == self.Role.ADMIN:
            self.is_staff = True
        super().save(*args, **kwargs)

    @property
    def is_administrador(self):
        """Indica si el usuario tiene privilegios de Administrador."""
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def nombre_visible(self):
        """Devuelve el nombre completo o el correo si no hay nombres."""
        return self.get_full_name() or self.email

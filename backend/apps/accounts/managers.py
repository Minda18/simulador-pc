"""Gestor personalizado del modelo de usuario."""

from django.contrib.auth.base_user import BaseUserManager
from django.utils.text import slugify


class UserManager(BaseUserManager):
    """Crea usuarios usando el correo electrónico como identificador."""

    use_in_migrations = True

    @staticmethod
    def _username_base(email):
        """Genera un nombre de usuario base a partir del correo."""
        return (slugify(email.split("@")[0]) or "usuario")[:140]

    def _unique_username(self, base):
        """Añade un sufijo numérico si el nombre de usuario ya existe."""
        candidate = base
        counter = 1
        while self.model._default_manager.filter(username=candidate).exists():
            counter += 1
            suffix = f"-{counter}"
            candidate = f"{base[:150 - len(suffix)]}{suffix}"
        return candidate

    def _create_user(self, email, password, **extra_fields):
        """Valida, normaliza y guarda un usuario con contraseña cifrada."""
        if not email:
            raise ValueError("El correo electrónico es obligatorio.")

        email = self.normalize_email(email).strip().lower()
        username = extra_fields.pop("username", None)
        if not username:
            username = self._unique_username(self._username_base(email))

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Crea un usuario estándar sin privilegios administrativos."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Crea un superusuario con rol de Administrador."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", self.model.Role.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

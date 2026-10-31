"""Backend de autenticación por correo electrónico."""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """Autentica usuarios usando el correo como nombre de usuario."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Busca el usuario por email y comprueba su contraseña."""
        UserModel = get_user_model()
        email = username or kwargs.get("email")

        if not email or password is None:
            return None

        try:
            user = UserModel.objects.get(email__iexact=email.strip())
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

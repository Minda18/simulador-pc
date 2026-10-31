"""Utilidades de redirección según el rol del usuario."""

from django.urls import reverse

from apps.accounts.models import User


def panel_url_for(user):
    """Devuelve la URL del panel adecuado para el usuario indicado."""
    if not user.is_authenticated:
        return reverse("accounts:login")
    if user.is_administrador:
        return reverse("core:panel_admin")
    if user.role == User.Role.USUARIO:
        return reverse("core:panel_usuario")
    return reverse("core:home")

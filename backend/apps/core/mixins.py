"""Control de acceso reutilizable basado en roles."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin):
    """Exige sesión iniciada y uno de los roles permitidos."""

    allowed_roles = ()

    def dispatch(self, request, *args, **kwargs):
        """Valida la sesión y el rol antes de ejecutar la vista."""
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        role_allowed = request.user.role in self.allowed_roles
        if not (request.user.is_administrador or role_allowed):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

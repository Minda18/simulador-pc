"""Vistas públicas y paneles por rol."""

from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, TemplateView

from apps.accounts.models import User
from apps.builds.models import Build
from apps.catalog.models import CompatibilityRule, Component
from apps.core.mixins import RoleRequiredMixin
from apps.core.routing import panel_url_for


class HomeView(TemplateView):
    """Página pública de bienvenida al simulador."""

    template_name = "home.html"


class CatalogView(ListView):
    """Catálogo público de componentes activos."""

    model = Component
    template_name = "catalog/catalog.html"
    context_object_name = "components"
    paginate_by = 24

    def get_queryset(self):
        """Filtra por tipo de componente mediante el parámetro ?tipo."""
        queryset = Component.objects.filter(is_active=True).select_related(
            "brand", "component_type"
        )
        component_type = self.request.GET.get("tipo")
        if component_type:
            queryset = queryset.filter(component_type__slug=component_type)
        return queryset


class PanelRedirectView(View):
    """Envía a cada usuario autenticado a su panel correspondiente."""

    def get(self, request):
        """Redirige según el rol o al login si no hay sesión."""
        return redirect(panel_url_for(request.user))


class PanelAdminView(RoleRequiredMixin, TemplateView):
    """Panel exclusivo del Administrador."""

    template_name = "core/panel_admin.html"
    allowed_roles = (User.Role.ADMIN,)

    def get_context_data(self, **kwargs):
        """Muestra contadores generales del sistema."""
        context = super().get_context_data(**kwargs)
        context["user_count"] = get_user_model().objects.count()
        context["component_count"] = Component.objects.count()
        context["rule_count"] = CompatibilityRule.objects.count()
        context["build_count"] = Build.objects.count()
        return context


class PanelUsuarioView(RoleRequiredMixin, TemplateView):
    """Panel del Usuario registrado con sus builds guardadas."""

    template_name = "core/panel_usuario.html"
    allowed_roles = (User.Role.USUARIO,)

    def get_context_data(self, **kwargs):
        """Carga las builds del usuario autenticado."""
        context = super().get_context_data(**kwargs)
        context["builds"] = Build.objects.filter(user=self.request.user)
        return context


def error_403(request, exception):
    """Renderiza la página personalizada de permisos denegados."""
    return render(request, "errors/403.html", status=403)

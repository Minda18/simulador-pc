"""Vistas de registro, inicio y cierre de sesión."""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from apps.accounts.forms import EmailAuthenticationForm, RegisterForm
from apps.core.routing import panel_url_for


class EmailLoginView(LoginView):
    """Inicia sesión con correo y redirige según el rol del usuario."""

    template_name = "accounts/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        """Envía al panel que corresponde al rol autenticado."""
        return panel_url_for(self.request.user)


class EmailLogoutView(LogoutView):
    """Cierra la sesión y vuelve a la página pública."""

    next_page = reverse_lazy("core:home")


def register(request):
    """Registra un nuevo Usuario y lo autentica automáticamente."""
    if request.user.is_authenticated:
        return redirect(panel_url_for(request.user))

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(
                request,
                user,
                backend="apps.accounts.backends.EmailBackend",
            )
            messages.success(
                request,
                "Tu cuenta fue creada correctamente. ¡Bienvenido!",
            )
            return redirect(panel_url_for(user))
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})

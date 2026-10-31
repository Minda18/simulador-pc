"""Configuración del modelo de usuario en Django Admin."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.forms import AdminUserChangeForm, AdminUserCreationForm
from apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Administra usuarios y su rol dentro del simulador."""

    add_form = AdminUserCreationForm
    form = AdminUserChangeForm
    model = User

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "role",
        "is_staff",
        "is_active",
    )
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Rol en el simulador",
            {"fields": ("role",)},
        ),
    )
    add_fieldsets = (
        (
            "Datos de la cuenta",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "role",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

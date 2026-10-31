"""Rutas principales del proyecto."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("", include("apps.core.urls")),
]

# Vitrina personalizada para errores de permisos.
handler403 = "apps.core.views.error_403"

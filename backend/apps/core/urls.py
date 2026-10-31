"""Rutas públicas y paneles por rol."""

from django.urls import path

from apps.core import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("catalogo/", views.CatalogView.as_view(), name="catalog"),
    path("panel/", views.PanelRedirectView.as_view(), name="panel"),
    path(
        "panel/admin/",
        views.PanelAdminView.as_view(),
        name="panel_admin",
    ),
    path(
        "panel/usuario/",
        views.PanelUsuarioView.as_view(),
        name="panel_usuario",
    ),
]

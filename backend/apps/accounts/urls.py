"""Rutas de autenticación."""

from django.urls import path

from apps.accounts import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.EmailLoginView.as_view(), name="login"),
    path("logout/", views.EmailLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
]

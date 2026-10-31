"""Formularios de registro, login y administración de usuarios."""

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from apps.accounts.models import User


class EmailAuthenticationForm(AuthenticationForm):
    """Formulario de login que solicita correo electrónico y contraseña."""

    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "autocomplete": "email",
                "placeholder": "tu@correo.com",
            }
        ),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "current-password",
            }
        ),
    )


class RegisterForm(forms.Form):
    """Formulario público para crear una cuenta de Usuario registrado."""

    email = forms.EmailField(
        label="Correo electrónico",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "autocomplete": "email",
                "placeholder": "tu@correo.com",
            }
        ),
    )
    first_name = forms.CharField(
        label="Nombres",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Apellidos",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "new-password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "new-password",
            }
        ),
    )

    def clean_email(self):
        """Normaliza el correo y evita duplicados sin distinguir mayúsculas."""
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Ya existe una cuenta con este correo.")
        return email

    def clean(self):
        """Verifica que ambas contraseñas coincidan y cumplan las reglas."""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Las contraseñas no coinciden.")

        if password1:
            user = User(
                email=cleaned_data.get("email", ""),
                first_name=cleaned_data.get("first_name", ""),
                last_name=cleaned_data.get("last_name", ""),
            )
            try:
                validate_password(password1, user=user)
            except ValidationError as error:
                self.add_error("password1", error)

        return cleaned_data

    def save(self):
        """Crea el usuario con rol estándar y contraseña cifrada."""
        return User.objects.create_user(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
            first_name=self.cleaned_data.get("first_name", ""),
            last_name=self.cleaned_data.get("last_name", ""),
        )


class AdminUserCreationForm(UserCreationForm):
    """Formulario del admin adaptado al modelo de usuario propio."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "username", "role", "first_name", "last_name")


class AdminUserChangeForm(UserChangeForm):
    """Formulario de edición del admin adaptado al modelo propio."""

    class Meta:
        model = User
        fields = "__all__"

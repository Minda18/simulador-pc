"""Modelos de configuraciones (builds) e ítems seleccionados."""

from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.catalog.models import Component


class Build(models.Model):
    """Configuración de PC armada por un usuario registrado."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="builds",
        verbose_name="usuario",
        null=True,
        blank=True,
        help_text="Nulo mientras la build es temporal (visitante).",
    )
    name = models.CharField("nombre", max_length=120)
    notes = models.TextField("notas", blank=True)
    is_public = models.BooleanField("compartible", default=False)
    created_at = models.DateTimeField("creada el", auto_now_add=True)
    updated_at = models.DateTimeField("actualizada el", auto_now=True)

    class Meta:
        verbose_name = "build"
        verbose_name_plural = "builds"
        ordering = ["-updated_at"]

    def __str__(self):
        """Nombre de la build junto al correo del propietario."""
        owner = self.user.email if self.user else "temporal"
        return f"{self.name} ({owner})"

    @property
    def total_price(self):
        """Suma el precio de todos los ítems de la build."""
        total = sum(
            (item.subtotal for item in self.items.all()),
            Decimal("0.00"),
        )
        return total


class BuildItem(models.Model):
    """Componente seleccionado dentro de una build."""

    build = models.ForeignKey(
        Build,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="build",
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.PROTECT,
        related_name="build_items",
        verbose_name="componente",
    )
    quantity = models.PositiveIntegerField("cantidad", default=1)
    added_at = models.DateTimeField("agregado el", auto_now_add=True)

    class Meta:
        verbose_name = "ítem de build"
        verbose_name_plural = "ítems de build"
        ordering = ["build", "component__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["build", "component"],
                name="unique_component_per_build",
            )
        ]

    def __str__(self):
        """Resumen del componente y la cantidad seleccionada."""
        return f"{self.component.name} x{self.quantity}"

    @property
    def subtotal(self):
        """Precio del componente multiplicado por la cantidad."""
        return self.component.price * self.quantity

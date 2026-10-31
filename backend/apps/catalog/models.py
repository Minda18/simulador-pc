"""Modelos del catálogo y de las reglas de compatibilidad."""

from django.db import models
from django.utils.text import slugify


class Brand(models.Model):
    """Fabricante de componentes (AMD, Intel, ASUS, etc.)."""

    name = models.CharField("nombre", max_length=100, unique=True)
    website = models.URLField("sitio web", blank=True)
    is_active = models.BooleanField("activa", default=True)
    created_at = models.DateTimeField("creada el", auto_now_add=True)

    class Meta:
        verbose_name = "marca"
        verbose_name_plural = "marcas"
        ordering = ["name"]

    def __str__(self):
        """Nombre de la marca para listados y formularios."""
        return self.name


class ComponentType(models.Model):
    """Tipo de componente: CPU, placa madre, RAM, GPU, fuente, etc."""

    name = models.CharField("nombre", max_length=80, unique=True)
    slug = models.SlugField("identificador", max_length=80, unique=True, blank=True)
    description = models.TextField("descripción", blank=True)

    class Meta:
        verbose_name = "tipo de componente"
        verbose_name_plural = "tipos de componente"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        """Genera el slug automáticamente si no fue indicado."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """Nombre del tipo de componente."""
        return self.name


class Component(models.Model):
    """Pieza concreta del catálogo, con sus especificaciones técnicas."""

    name = models.CharField("nombre", max_length=150)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="components",
        verbose_name="marca",
    )
    component_type = models.ForeignKey(
        ComponentType,
        on_delete=models.PROTECT,
        related_name="components",
        verbose_name="tipo de componente",
    )
    model_code = models.CharField("código de modelo", max_length=80, blank=True)
    price = models.DecimalField(
        "precio", max_digits=10, decimal_places=2, default=0
    )
    stock = models.PositiveIntegerField(
        "disponibilidad referencial",
        default=0,
        help_text=(
            "Cantidad orientativa para el catálogo; no descuenta unidades ni "
            "bloquea la selección."
        ),
    )
    specifications = models.JSONField(
        "especificaciones",
        default=dict,
        blank=True,
        help_text="Datos técnicos usados por el motor de compatibilidad.",
    )
    is_active = models.BooleanField("activo", default=True)
    created_at = models.DateTimeField("creado el", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado el", auto_now=True)

    class Meta:
        verbose_name = "componente"
        verbose_name_plural = "componentes"
        ordering = ["component_type__name", "name"]

    def __str__(self):
        """Nombre y tipo del componente."""
        return f"{self.name} ({self.component_type.name})"

    def spec(self, key, default=None):
        """Devuelve una especificación técnica concreta."""
        return self.specifications.get(key, default)


class CompatibilityRule(models.Model):
    """Regla que relaciona dos tipos de componente."""

    class Severity(models.TextChoices):
        ERROR = "ERROR", "Incompatible"
        WARNING = "WARNING", "Advertencia"

    name = models.CharField("nombre", max_length=150)
    rule_key = models.SlugField(
        "clave de regla",
        max_length=100,
        unique=True,
        help_text="Identificador usado por el motor de reglas.",
    )
    source_type = models.ForeignKey(
        ComponentType,
        on_delete=models.CASCADE,
        related_name="source_rules",
        verbose_name="tipo origen",
    )
    target_type = models.ForeignKey(
        ComponentType,
        on_delete=models.CASCADE,
        related_name="target_rules",
        verbose_name="tipo destino",
    )
    severity = models.CharField(
        "severidad",
        max_length=10,
        choices=Severity.choices,
        default=Severity.ERROR,
    )
    description = models.TextField(
        "descripción",
        help_text="Explicación que se mostrará al usuario.",
    )
    parameters = models.JSONField(
        "parámetros",
        default=dict,
        blank=True,
        help_text="Campos y valores que debe comparar la regla.",
    )
    is_active = models.BooleanField("activa", default=True)
    created_at = models.DateTimeField("creada el", auto_now_add=True)

    class Meta:
        verbose_name = "regla de compatibilidad"
        verbose_name_plural = "reglas de compatibilidad"
        ordering = ["name"]

    def __str__(self):
        """Resumen de la regla y su severidad."""
        return f"{self.name} [{self.get_severity_display()}]"

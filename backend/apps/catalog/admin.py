"""Configuración del catálogo en Django Admin."""

from django.contrib import admin

from apps.catalog.models import Brand, CompatibilityRule, Component, ComponentType


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Administra los fabricantes del catálogo."""

    list_display = ("name", "website", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(ComponentType)
class ComponentTypeAdmin(admin.ModelAdmin):
    """Administra los tipos de componente."""

    list_display = ("name", "slug")
    search_fields = ("name",)
    readonly_fields = ("slug",)


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    """Administra las piezas y sus especificaciones técnicas."""

    list_display = (
        "name",
        "component_type",
        "brand",
        "price",
        "stock",
        "is_active",
    )
    list_filter = ("component_type", "brand", "is_active")
    search_fields = ("name", "brand__name", "model_code")
    list_select_related = ("brand", "component_type")
    autocomplete_fields = ("brand",)
    fieldsets = (
        (
            "Identificación",
            {"fields": ("name", "brand", "component_type", "model_code")},
        ),
        (
            "Comercial y disponibilidad",
            {"fields": ("price", "stock", "is_active")},
        ),
        (
            "Especificaciones técnicas",
            {
                "fields": ("specifications",),
                "description": "Estructura JSON usada por el motor de reglas.",
            },
        ),
    )


@admin.register(CompatibilityRule)
class CompatibilityRuleAdmin(admin.ModelAdmin):
    """Administra las reglas que validará el simulador."""

    list_display = (
        "name",
        "source_type",
        "target_type",
        "severity",
        "is_active",
    )
    list_filter = ("severity", "source_type", "target_type", "is_active")
    search_fields = ("name", "rule_key", "description")
    list_select_related = ("source_type", "target_type")

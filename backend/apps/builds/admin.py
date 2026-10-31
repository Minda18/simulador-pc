"""Configuración de builds en Django Admin."""

from django.contrib import admin

from apps.builds.models import Build, BuildItem


class BuildItemInline(admin.TabularInline):
    """Permite editar los componentes de una build en la misma pantalla."""

    model = BuildItem
    extra = 1
    autocomplete_fields = ("component",)


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    """Administra las configuraciones guardadas."""

    list_display = ("name", "user", "total_price", "items_count", "updated_at")
    list_filter = ("is_public", "created_at")
    search_fields = ("name", "user__email")
    list_select_related = ("user",)
    inlines = [BuildItemInline]

    @admin.display(description="Ítems")
    def items_count(self, obj):
        """Cantidad de componentes agregados a la build."""
        return obj.items.count()


@admin.register(BuildItem)
class BuildItemAdmin(admin.ModelAdmin):
    """Vista independiente para revisar los ítems de todas las builds."""

    list_display = ("build", "component", "quantity", "subtotal")
    list_filter = ("build",)
    search_fields = ("build__name", "component__name")
    list_select_related = ("build", "component")

"""Carga un catálogo de ejemplo y builds de demostración."""

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.accounts.models import User
from apps.builds.models import Build, BuildItem
from apps.catalog.models import Brand, CompatibilityRule, Component, ComponentType

DEMO_EMAIL = "demo@example.com"
DEMO_PASSWORD = "Demo12345!"

COMPONENT_TYPES = [
    {
        "name": "Procesador",
        "slug": "cpu",
        "description": "Unidad central de procesamiento del equipo.",
    },
    {
        "name": "Placa madre",
        "slug": "motherboard",
        "description": "Placa base que conecta y da soporte a los componentes.",
    },
    {
        "name": "Memoria RAM",
        "slug": "ram",
        "description": "Memoria principal para el sistema y las aplicaciones.",
    },
    {
        "name": "Tarjeta gráfica",
        "slug": "gpu",
        "description": "Acelerador gráfico dedicado para juegos y creación.",
    },
    {
        "name": "Fuente de alimentación",
        "slug": "psu",
        "description": "Fuente que entrega energía al resto de los componentes.",
    },
    {
        "name": "Gabinete",
        "slug": "case",
        "description": "Chasis que aloja y organiza los componentes.",
    },
    {
        "name": "Almacenamiento",
        "slug": "storage",
        "description": "Unidades SSD para el sistema y los datos.",
    },
    {
        "name": "Refrigeración de CPU",
        "slug": "cooler",
        "description": "Disipador que mantiene controlada la temperatura del CPU.",
    },
]

BRANDS = [
    ("AMD", "https://www.amd.com"),
    ("Intel", "https://www.intel.com"),
    ("ASUS", "https://www.asus.com"),
    ("MSI", "https://www.msi.com"),
    ("Gigabyte", "https://www.gigabyte.com"),
    ("Kingston", "https://www.kingston.com"),
    ("Corsair", "https://www.corsair.com"),
    ("NVIDIA", "https://www.nvidia.com"),
    ("Seasonic", "https://www.seasonic.com"),
    ("Lian Li", "https://www.lian-li.com"),
    ("Noctua", "https://www.noctua.at"),
    ("Samsung", "https://www.samsung.com"),
]

COMPONENTS = [
    {
        "name": "AMD Ryzen 5 7600",
        "brand": "AMD",
        "type": "cpu",
        "model_code": "100-100001015BOX",
        "price": "229.00",
        "stock": 12,
        "specifications": {
            "socket": "AM5",
            "memory_types": ["DDR5"],
            "tdp_watts": 65,
            "max_boost_watts": 88,
            "cores": 6,
            "threads": 12,
            "tier": 3,
            "integrated_graphics": True,
        },
    },
    {
        "name": "AMD Ryzen 7 7800X3D",
        "brand": "AMD",
        "type": "cpu",
        "model_code": "100-100000910WOF",
        "price": "399.00",
        "stock": 8,
        "specifications": {
            "socket": "AM5",
            "memory_types": ["DDR5"],
            "tdp_watts": 120,
            "max_boost_watts": 162,
            "cores": 8,
            "threads": 16,
            "tier": 5,
            "integrated_graphics": True,
        },
    },
    {
        "name": "AMD Ryzen 5 5600",
        "brand": "AMD",
        "type": "cpu",
        "model_code": "100-100000927BOX",
        "price": "139.00",
        "stock": 15,
        "specifications": {
            "socket": "AM4",
            "memory_types": ["DDR4"],
            "tdp_watts": 65,
            "max_boost_watts": 88,
            "cores": 6,
            "threads": 12,
            "tier": 2,
            "integrated_graphics": False,
        },
    },
    {
        "name": "Intel Core i5-13400F",
        "brand": "Intel",
        "type": "cpu",
        "model_code": "BX8071513400F",
        "price": "189.00",
        "stock": 10,
        "specifications": {
            "socket": "LGA1700",
            "memory_types": ["DDR4", "DDR5"],
            "tdp_watts": 65,
            "max_boost_watts": 148,
            "cores": 10,
            "threads": 16,
            "tier": 3,
            "integrated_graphics": False,
        },
    },
    {
        "name": "Intel Core i5-14600K",
        "brand": "Intel",
        "type": "cpu",
        "model_code": "BX8071514600K",
        "price": "299.00",
        "stock": 7,
        "specifications": {
            "socket": "LGA1700",
            "memory_types": ["DDR4", "DDR5"],
            "tdp_watts": 125,
            "max_boost_watts": 181,
            "cores": 14,
            "threads": 20,
            "tier": 4,
            "integrated_graphics": True,
        },
    },
    {
        "name": "ASUS ROG Strix B650-A Gaming WiFi",
        "brand": "ASUS",
        "type": "motherboard",
        "model_code": "90MB1BP0-M0EAY0",
        "price": "219.00",
        "stock": 9,
        "specifications": {
            "socket": "AM5",
            "memory_type": "DDR5",
            "form_factor": "ATX",
            "ram_slots": 4,
            "max_memory_gb": 128,
            "m2_slots": 3,
            "wifi": True,
        },
    },
    {
        "name": "ASUS TUF Gaming B650M-PLUS WiFi",
        "brand": "ASUS",
        "type": "motherboard",
        "model_code": "90MB1F00-M0EAY0",
        "price": "179.00",
        "stock": 11,
        "specifications": {
            "socket": "AM5",
            "memory_type": "DDR5",
            "form_factor": "micro-ATX",
            "ram_slots": 4,
            "max_memory_gb": 128,
            "m2_slots": 2,
            "wifi": True,
        },
    },
    {
        "name": "MSI PRO B760M-A WiFi",
        "brand": "MSI",
        "type": "motherboard",
        "model_code": "7D99-001R",
        "price": "149.00",
        "stock": 10,
        "specifications": {
            "socket": "LGA1700",
            "memory_type": "DDR5",
            "form_factor": "micro-ATX",
            "ram_slots": 4,
            "max_memory_gb": 128,
            "m2_slots": 2,
            "wifi": True,
        },
    },
    {
        "name": "Gigabyte B550M DS3H",
        "brand": "Gigabyte",
        "type": "motherboard",
        "model_code": "B550M DS3H",
        "price": "99.00",
        "stock": 14,
        "specifications": {
            "socket": "AM4",
            "memory_type": "DDR4",
            "form_factor": "micro-ATX",
            "ram_slots": 4,
            "max_memory_gb": 128,
            "m2_slots": 1,
            "wifi": False,
        },
    },
    {
        "name": "ASUS ROG Strix B650E-I Gaming WiFi",
        "brand": "ASUS",
        "type": "motherboard",
        "model_code": "90MB1F30-M0EAY0",
        "price": "279.00",
        "stock": 5,
        "specifications": {
            "socket": "AM5",
            "memory_type": "DDR5",
            "form_factor": "Mini-ITX",
            "ram_slots": 2,
            "max_memory_gb": 64,
            "m2_slots": 2,
            "wifi": True,
        },
    },
    {
        "name": "Kingston Fury Beast 16 GB DDR5-5600",
        "brand": "Kingston",
        "type": "ram",
        "model_code": "KF556C40BB-16",
        "price": "65.00",
        "stock": 20,
        "specifications": {
            "memory_type": "DDR5",
            "capacity_gb": 16,
            "speed_mhz": 5600,
            "modules": 1,
            "voltage": 1.25,
            "latency_cl": 40,
        },
    },
    {
        "name": "Corsair Vengeance 32 GB DDR5-6000",
        "brand": "Corsair",
        "type": "ram",
        "model_code": "CMK32GX5M2B6000C36",
        "price": "119.00",
        "stock": 13,
        "specifications": {
            "memory_type": "DDR5",
            "capacity_gb": 32,
            "speed_mhz": 6000,
            "modules": 2,
            "voltage": 1.35,
            "latency_cl": 36,
        },
    },
    {
        "name": "Kingston Fury Beast 16 GB DDR4-3200",
        "brand": "Kingston",
        "type": "ram",
        "model_code": "KF432C16BB/16",
        "price": "45.00",
        "stock": 25,
        "specifications": {
            "memory_type": "DDR4",
            "capacity_gb": 16,
            "speed_mhz": 3200,
            "modules": 1,
            "voltage": 1.35,
            "latency_cl": 16,
        },
    },
    {
        "name": "Corsair Vengeance RGB Pro 32 GB DDR4-3600",
        "brand": "Corsair",
        "type": "ram",
        "model_code": "CMW32GX4M2D3600C18",
        "price": "89.00",
        "stock": 8,
        "specifications": {
            "memory_type": "DDR4",
            "capacity_gb": 32,
            "speed_mhz": 3600,
            "modules": 2,
            "voltage": 1.35,
            "latency_cl": 18,
        },
    },
    {
        "name": "NVIDIA GeForce RTX 4060 8 GB",
        "brand": "NVIDIA",
        "type": "gpu",
        "model_code": "RTX 4060 8GB",
        "price": "299.00",
        "stock": 10,
        "specifications": {
            "tdp_watts": 115,
            "recommended_psu_watts": 450,
            "length_mm": 244,
            "memory_gb": 8,
            "tier": 3,
        },
    },
    {
        "name": "NVIDIA GeForce RTX 4070 Super 12 GB",
        "brand": "NVIDIA",
        "type": "gpu",
        "model_code": "RTX 4070 SUPER 12GB",
        "price": "599.00",
        "stock": 6,
        "specifications": {
            "tdp_watts": 220,
            "recommended_psu_watts": 650,
            "length_mm": 285,
            "memory_gb": 12,
            "tier": 4,
        },
    },
    {
        "name": "AMD Radeon RX 7600 8 GB",
        "brand": "AMD",
        "type": "gpu",
        "model_code": "RX 7600 8GB",
        "price": "269.00",
        "stock": 9,
        "specifications": {
            "tdp_watts": 165,
            "recommended_psu_watts": 500,
            "length_mm": 204,
            "memory_gb": 8,
            "tier": 3,
        },
    },
    {
        "name": "NVIDIA GeForce RTX 4090 24 GB",
        "brand": "NVIDIA",
        "type": "gpu",
        "model_code": "RTX 4090 24GB",
        "price": "1599.00",
        "stock": 2,
        "specifications": {
            "tdp_watts": 450,
            "recommended_psu_watts": 850,
            "length_mm": 336,
            "memory_gb": 24,
            "tier": 5,
        },
    },
    {
        "name": "Corsair RM650e 650 W 80+ Gold",
        "brand": "Corsair",
        "type": "psu",
        "model_code": "CP-9020280-NA",
        "price": "99.00",
        "stock": 12,
        "specifications": {
            "wattage": 650,
            "efficiency": "80+ Gold",
            "modular": "Full",
            "atx_standard": "ATX 3.0",
        },
    },
    {
        "name": "Seasonic Focus GX-750 750 W 80+ Gold",
        "brand": "Seasonic",
        "type": "psu",
        "model_code": "FOCUS-GX-750",
        "price": "129.00",
        "stock": 9,
        "specifications": {
            "wattage": 750,
            "efficiency": "80+ Gold",
            "modular": "Full",
            "atx_standard": "ATX 3.0",
        },
    },
    {
        "name": "Corsair CV550 550 W 80+ Bronze",
        "brand": "Corsair",
        "type": "psu",
        "model_code": "CP-9020210-NA",
        "price": "59.00",
        "stock": 18,
        "specifications": {
            "wattage": 550,
            "efficiency": "80+ Bronze",
            "modular": "No",
            "atx_standard": "ATX 2.4",
        },
    },
    {
        "name": "Seasonic Prime TX-1000 1000 W 80+ Titanium",
        "brand": "Seasonic",
        "type": "psu",
        "model_code": "PRIME-TX-1000",
        "price": "259.00",
        "stock": 3,
        "specifications": {
            "wattage": 1000,
            "efficiency": "80+ Titanium",
            "modular": "Full",
            "atx_standard": "ATX 3.0",
        },
    },
    {
        "name": "Lian Li Lancool 216",
        "brand": "Lian Li",
        "type": "case",
        "model_code": "LANCOOL216",
        "price": "99.00",
        "stock": 10,
        "specifications": {
            "form_factors_supported": ["ATX", "micro-ATX", "Mini-ITX"],
            "max_gpu_length_mm": 392,
            "max_cooler_height_mm": 180,
            "color": "Negro",
        },
    },
    {
        "name": "Corsair 4000D Airflow",
        "brand": "Corsair",
        "type": "case",
        "model_code": "CC-9011200-WW",
        "price": "89.00",
        "stock": 12,
        "specifications": {
            "form_factors_supported": ["ATX", "micro-ATX", "Mini-ITX"],
            "max_gpu_length_mm": 360,
            "max_cooler_height_mm": 170,
            "color": "Negro",
        },
    },
    {
        "name": "Lian Li A4-H2O",
        "brand": "Lian Li",
        "type": "case",
        "model_code": "A4-H2O",
        "price": "139.00",
        "stock": 0,
        "specifications": {
            "form_factors_supported": ["Mini-ITX"],
            "max_gpu_length_mm": 322,
            "max_cooler_height_mm": 55,
            "color": "Negro",
        },
    },
    {
        "name": "Samsung 980 NVMe 1 TB",
        "brand": "Samsung",
        "type": "storage",
        "model_code": "MZ-V8V1T0B/AM",
        "price": "79.00",
        "stock": 20,
        "specifications": {
            "interface": "NVMe",
            "form_factor": "M.2 2280",
            "capacity_gb": 1000,
            "read_mbps": 3500,
        },
    },
    {
        "name": "Kingston NV2 NVMe 500 GB",
        "brand": "Kingston",
        "type": "storage",
        "model_code": "SNV2S/500G",
        "price": "39.00",
        "stock": 25,
        "specifications": {
            "interface": "NVMe",
            "form_factor": "M.2 2280",
            "capacity_gb": 500,
            "read_mbps": 3500,
        },
    },
    {
        "name": "Noctua NH-U12S",
        "brand": "Noctua",
        "type": "cooler",
        "model_code": "NH-U12S",
        "price": "69.00",
        "stock": 10,
        "specifications": {
            "supported_sockets": ["AM4", "AM5", "LGA1700", "LGA1200"],
            "height_mm": 158,
            "tdp_capacity_watts": 180,
            "type": "Aire",
        },
    },
    {
        "name": "Noctua NH-L9i-17xx",
        "brand": "Noctua",
        "type": "cooler",
        "model_code": "NH-L9i-17xx",
        "price": "49.00",
        "stock": 8,
        "specifications": {
            "supported_sockets": ["LGA1700", "LGA1200"],
            "height_mm": 37,
            "tdp_capacity_watts": 65,
            "type": "Aire",
        },
    },
]

RULES = [
    {
        "name": "Socket de CPU compatible con la placa",
        "rule_key": "cpu_motherboard_socket",
        "source_type": "cpu",
        "target_type": "motherboard",
        "severity": CompatibilityRule.Severity.ERROR,
        "description": (
            "El socket del procesador debe coincidir con el socket de la placa "
            "madre para que la pieza pueda instalarse."
        ),
        "parameters": {
            "source_field": "socket",
            "target_field": "socket",
            "operator": "equals",
        },
    },
    {
        "name": "Tipo de memoria compatible con la placa",
        "rule_key": "motherboard_ram_type",
        "source_type": "motherboard",
        "target_type": "ram",
        "severity": CompatibilityRule.Severity.ERROR,
        "description": (
            "La placa madre solo admite módulos del tipo de memoria que "
            "especifica su ranura, por ejemplo DDR4 o DDR5."
        ),
        "parameters": {
            "source_field": "memory_type",
            "target_field": "memory_type",
            "operator": "equals",
        },
    },
    {
        "name": "Potencia de la fuente para la GPU",
        "rule_key": "gpu_psu_watts",
        "source_type": "gpu",
        "target_type": "psu",
        "severity": CompatibilityRule.Severity.ERROR,
        "description": (
            "La fuente debe entregar al menos la potencia recomendada por el "
            "fabricante de la tarjeta gráfica."
        ),
        "parameters": {
            "source_field": "recommended_psu_watts",
            "target_field": "wattage",
            "operator": "less_or_equal",
        },
    },
    {
        "name": "Formato de placa compatible con el gabinete",
        "rule_key": "motherboard_case_form_factor",
        "source_type": "motherboard",
        "target_type": "case",
        "severity": CompatibilityRule.Severity.ERROR,
        "description": (
            "El gabinete debe admitir el formato de la placa madre: ATX, "
            "micro-ATX o Mini-ITX."
        ),
        "parameters": {
            "source_field": "form_factor",
            "target_field": "form_factors_supported",
            "operator": "in",
        },
    },
    {
        "name": "Longitud de la GPU compatible con el gabinete",
        "rule_key": "gpu_case_length",
        "source_type": "gpu",
        "target_type": "case",
        "severity": CompatibilityRule.Severity.ERROR,
        "description": (
            "La longitud de la tarjeta gráfica no debe superar el espacio "
            "disponible dentro del gabinete."
        ),
        "parameters": {
            "source_field": "length_mm",
            "target_field": "max_gpu_length_mm",
            "operator": "less_or_equal",
        },
    },
    {
        "name": "Socket compatible con el refrigerador de CPU",
        "rule_key": "cooler_cpu_socket",
        "source_type": "cooler",
        "target_type": "cpu",
        "severity": CompatibilityRule.Severity.ERROR,
        "description": (
            "El sistema de refrigeración debe incluir el soporte para el "
            "socket del procesador seleccionado."
        ),
        "parameters": {
            "source_field": "supported_sockets",
            "target_field": "socket",
            "operator": "contains",
        },
    },
    {
        "name": "Altura del refrigerador compatible con el gabinete",
        "rule_key": "cooler_case_height",
        "source_type": "cooler",
        "target_type": "case",
        "severity": CompatibilityRule.Severity.WARNING,
        "description": (
            "La altura del disipador debe quedar por debajo del máximo que "
            "admite el gabinete."
        ),
        "parameters": {
            "source_field": "height_mm",
            "target_field": "max_cooler_height_mm",
            "operator": "less_or_equal",
        },
    },
    {
        "name": "Posible cuello de botella entre CPU y GPU",
        "rule_key": "cpu_gpu_bottleneck",
        "source_type": "cpu",
        "target_type": "gpu",
        "severity": CompatibilityRule.Severity.WARNING,
        "description": (
            "Una diferencia de más de un nivel entre la gama del procesador y "
            "la de la tarjeta gráfica puede limitar el rendimiento."
        ),
        "parameters": {
            "source_field": "tier",
            "target_field": "tier",
            "operator": "max_gap",
            "max_gap": 1,
        },
    },
]

DEMO_BUILDS = [
    {
        "name": "PC Gamer equilibrada",
        "notes": (
            "Configuración AM5 de gama media-alta para jugar en 1440p con "
            "margen de actualización."
        ),
        "components": [
            "AMD Ryzen 5 7600",
            "ASUS TUF Gaming B650M-PLUS WiFi",
            "Corsair Vengeance 32 GB DDR5-6000",
            "NVIDIA GeForce RTX 4070 Super 12 GB",
            "Corsair RM650e 650 W 80+ Gold",
            "Lian Li Lancool 216",
            "Samsung 980 NVMe 1 TB",
            "Noctua NH-U12S",
        ],
    },
    {
        "name": "PC Oficina Intel",
        "notes": (
            "Equipo equilibrado para productividad, estudio y juegos en 1080p "
            "con consumo contenido."
        ),
        "components": [
            "Intel Core i5-13400F",
            "MSI PRO B760M-A WiFi",
            "Kingston Fury Beast 16 GB DDR5-5600",
            "NVIDIA GeForce RTX 4060 8 GB",
            "Corsair CV550 550 W 80+ Bronze",
            "Corsair 4000D Airflow",
            "Kingston NV2 NVMe 500 GB",
            "Noctua NH-U12S",
        ],
    },
]


class Command(BaseCommand):
    """Crea un catálogo demostrativo y dos builds de ejemplo."""

    help = "Carga marcas, componentes, reglas y builds de demostración."

    @transaction.atomic
    def handle(self, *args, **options):
        """Ejecuta la carga idempotente de los datos de ejemplo."""
        types = self._create_component_types()
        brands = self._create_brands()
        components = self._create_components(types, brands)
        self._create_rules(types)
        user, user_created = self._create_demo_user()
        self._create_builds(user, components)

        self.stdout.write(self.style.SUCCESS("Datos de ejemplo cargados."))
        self.stdout.write(
            "Resumen: "
            f"{ComponentType.objects.count()} tipos, "
            f"{Brand.objects.count()} marcas, "
            f"{Component.objects.count()} componentes, "
            f"{CompatibilityRule.objects.count()} reglas, "
            f"{Build.objects.count()} builds."
        )
        if user_created:
            self.stdout.write(
                f"Usuario demo creado: {DEMO_EMAIL} / {DEMO_PASSWORD}"
            )
        else:
            self.stdout.write(
                f"Usuario demo existente: {DEMO_EMAIL} (contraseña sin cambios)"
            )

    def _create_component_types(self):
        """Crea o actualiza los tipos de componente del catálogo."""
        types = {}
        for data in COMPONENT_TYPES:
            component_type, _ = ComponentType.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "description": data["description"],
                },
            )
            types[data["slug"]] = component_type
        return types

    def _create_brands(self):
        """Crea o actualiza las marcas del catálogo."""
        brands = {}
        for name, website in BRANDS:
            brand, _ = Brand.objects.update_or_create(
                name=name,
                defaults={"website": website, "is_active": True},
            )
            brands[name] = brand
        return brands

    def _create_components(self, types, brands):
        """Crea o actualiza los componentes con sus especificaciones."""
        components = {}
        for data in COMPONENTS:
            component, _ = Component.objects.update_or_create(
                name=data["name"],
                brand=brands[data["brand"]],
                component_type=types[data["type"]],
                defaults={
                    "model_code": data["model_code"],
                    "price": Decimal(data["price"]),
                    "stock": data["stock"],
                    "specifications": data["specifications"],
                    "is_active": True,
                },
            )
            components[data["name"]] = component
        return components

    def _create_rules(self, types):
        """Crea o actualiza las reglas de compatibilidad."""
        for data in RULES:
            CompatibilityRule.objects.update_or_create(
                rule_key=data["rule_key"],
                defaults={
                    "name": data["name"],
                    "source_type": types[data["source_type"]],
                    "target_type": types[data["target_type"]],
                    "severity": data["severity"],
                    "description": data["description"],
                    "parameters": data["parameters"],
                    "is_active": True,
                },
            )

    def _create_demo_user(self):
        """Crea el usuario demo sin sobrescribir una contraseña existente."""
        user = User.objects.filter(email=DEMO_EMAIL).first()
        if user is not None:
            return user, False

        user = User.objects.create_user(
            email=DEMO_EMAIL,
            password=DEMO_PASSWORD,
            first_name="Usuario",
            last_name="Demo",
            role=User.Role.USUARIO,
        )
        return user, True

    def _create_builds(self, user, components):
        """Crea o actualiza las builds de demostración del usuario."""
        for data in DEMO_BUILDS:
            build, _ = Build.objects.update_or_create(
                user=user,
                name=data["name"],
                defaults={"notes": data["notes"], "is_public": True},
            )
            selected = [components[name] for name in data["components"]]
            build.items.exclude(component__in=selected).delete()
            for component in selected:
                BuildItem.objects.update_or_create(
                    build=build,
                    component=component,
                    defaults={"quantity": 1},
                )

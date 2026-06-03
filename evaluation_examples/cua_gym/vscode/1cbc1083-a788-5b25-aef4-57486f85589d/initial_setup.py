"""
Initial Setup: Configure workspace with Django project and single Python formatter
Task ID: vscode_py_077
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_077'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def create_initial():
    # --- Create Django project structure ---

    # Main app files
    create_file(f'{PROJECT_DIR}/manage.py', '''\
#!/usr/bin/env python
"""Django management script for inventory_tracker project."""
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_tracker.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
''')

    # Project settings module
    create_file(f'{PROJECT_DIR}/inventory_tracker/__init__.py', '')

    create_file(f'{PROJECT_DIR}/inventory_tracker/settings.py', '''\
"""
Django settings for inventory_tracker project.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-x7$m2k!p@q3r#s5t&u8v*w0y'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',
    'warehouse',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'inventory_tracker.urls'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True
STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
''')

    create_file(f'{PROJECT_DIR}/inventory_tracker/urls.py', '''\
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('warehouse/', include('warehouse.urls')),
]
''')

    create_file(f'{PROJECT_DIR}/inventory_tracker/wsgi.py', '''\
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_tracker.settings')
application = get_wsgi_application()
''')

    # --- Products app ---
    create_file(f'{PROJECT_DIR}/products/__init__.py', '')

    create_file(f'{PROJECT_DIR}/products/models.py', '''\
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("discontinued", "Discontinued"),
        ("pending", "Pending Review"),
    ]

    sku = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    weight_kg = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def profit_margin(self):
        if self.cost_price == 0:
            return 0
        return ((self.unit_price - self.cost_price) / self.unit_price) * 100

    def __str__(self):
        return f"{self.sku} - {self.name}"
''')

    create_file(f'{PROJECT_DIR}/products/views.py', '''\
from django.http import JsonResponse
from django.views import View


class ProductListView(View):
    """Return a JSON list of active products."""

    def get(self, request):
        from .models import Product
        products = Product.objects.filter(status="active").values(
            "sku", "name", "unit_price", "category__name"
        )
        return JsonResponse({"products": list(products)})


class ProductDetailView(View):
    """Return details for a single product by SKU."""

    def get(self, request, sku):
        from .models import Product
        try:
            product = Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        return JsonResponse({
            "sku": product.sku,
            "name": product.name,
            "unit_price": str(product.unit_price),
            "cost_price": str(product.cost_price),
            "margin": f"{product.profit_margin():.1f}%",
        })
''')

    create_file(f'{PROJECT_DIR}/products/urls.py', '''\
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product-list"),
    path("<str:sku>/", views.ProductDetailView.as_view(), name="product-detail"),
]
''')

    create_file(f'{PROJECT_DIR}/products/admin.py', '''\
from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "category", "unit_price", "status")
    list_filter = ("status", "category")
    search_fields = ("sku", "name")
''')

    # Products migrations
    create_file(f'{PROJECT_DIR}/products/migrations/__init__.py', '')

    create_file(f'{PROJECT_DIR}/products/migrations/0001_initial.py', '''\
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=32, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('active', 'Active'), ('discontinued', 'Discontinued'), ('pending', 'Pending Review')], default='active', max_length=20)),
                ('weight_kg', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category')),
            ],
        ),
    ]
''')

    create_file(f'{PROJECT_DIR}/products/migrations/0002_add_barcode_field.py', '''\
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
''')

    # --- Warehouse app ---
    create_file(f'{PROJECT_DIR}/warehouse/__init__.py', '')

    create_file(f'{PROJECT_DIR}/warehouse/models.py', '''\
from django.db import models


class Location(models.Model):
    code = models.CharField(max_length=16, unique=True)
    aisle = models.CharField(max_length=4)
    shelf = models.IntegerField()
    capacity = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.code} (Aisle {self.aisle}, Shelf {self.shelf})"


class StockEntry(models.Model):
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="stock_entries"
    )
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="stock_entries")
    quantity = models.IntegerField(default=0)
    last_counted = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("product", "location")
        verbose_name_plural = "stock entries"

    def __str__(self):
        return f"{self.product.sku} @ {self.location.code}: {self.quantity}"
''')

    create_file(f'{PROJECT_DIR}/warehouse/views.py', '''\
from django.http import JsonResponse
from django.views import View


class StockLevelView(View):
    """Return current stock levels grouped by location."""

    def get(self, request):
        from .models import StockEntry
        entries = StockEntry.objects.select_related("product", "location").all()
        data = [
            {
                "product_sku": e.product.sku,
                "location": e.location.code,
                "quantity": e.quantity,
                "last_counted": str(e.last_counted) if e.last_counted else None,
            }
            for e in entries
        ]
        return JsonResponse({"stock": data})


class LowStockAlertView(View):
    """Return products with stock below a given threshold."""

    def get(self, request):
        threshold = int(request.GET.get("threshold", 10))
        from .models import StockEntry
        low = StockEntry.objects.filter(quantity__lt=threshold).select_related("product", "location")
        alerts = [
            {"product": e.product.name, "location": e.location.code, "quantity": e.quantity}
            for e in low
        ]
        return JsonResponse({"low_stock_alerts": alerts, "threshold": threshold})
''')

    create_file(f'{PROJECT_DIR}/warehouse/urls.py', '''\
from django.urls import path
from . import views

urlpatterns = [
    path("stock/", views.StockLevelView.as_view(), name="stock-levels"),
    path("alerts/", views.LowStockAlertView.as_view(), name="low-stock-alerts"),
]
''')

    create_file(f'{PROJECT_DIR}/warehouse/admin.py', '''\
from django.contrib import admin
from .models import Location, StockEntry


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("code", "aisle", "shelf", "capacity")


@admin.register(StockEntry)
class StockEntryAdmin(admin.ModelAdmin):
    list_display = ("product", "location", "quantity", "last_counted")
    list_filter = ("location",)
''')

    # Warehouse migrations
    create_file(f'{PROJECT_DIR}/warehouse/migrations/__init__.py', '')

    create_file(f'{PROJECT_DIR}/warehouse/migrations/0001_initial.py', '''\
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True
    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16, unique=True)),
                ('aisle', models.CharField(max_length=4)),
                ('shelf', models.IntegerField()),
                ('capacity', models.IntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='StockEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('last_counted', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_entries', to='warehouse.location')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_entries', to='products.product')),
            ],
            options={
                'verbose_name_plural': 'stock entries',
                'unique_together': {('product', 'location')},
            },
        ),
    ]
''')

    # --- .vscode/settings.json with SINGLE generic formatter (initial state) ---
    # This is the "before" state: one formatter for all Python files
    vscode_settings = {
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "editor.formatOnSave": True,
        "editor.defaultFormatter": "ms-python.autopep8",
        "python.analysis.typeCheckingMode": "basic",
        "files.trimTrailingWhitespace": True,
        "files.insertFinalNewline": True
    }

    create_file(f'{PROJECT_DIR}/.vscode/settings.json', json.dumps(vscode_settings, indent=4))

    # --- requirements.txt ---
    create_file(f'{PROJECT_DIR}/requirements.txt', '''\
Django==4.2.11
djangorestframework==3.15.1
black==24.3.0
autopep8==2.1.0
''')

    # --- .gitignore ---
    create_file(f'{PROJECT_DIR}/.gitignore', '''\
__pycache__/
*.pyc
db.sqlite3
.env
*.egg-info/
dist/
build/
''')

    print(f'Django project created at: {PROJECT_DIR}')

    # --- Launch VSCode with the project folder ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

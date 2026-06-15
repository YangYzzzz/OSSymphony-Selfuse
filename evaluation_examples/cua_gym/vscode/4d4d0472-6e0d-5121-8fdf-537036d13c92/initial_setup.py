"""
Initial Setup: Configure pyrightconfig.json for Django project
Task ID: vscode_fix_057
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_057'
PROJECT_DIR = f'{WORKDIR}/django-project'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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


def create_django_project():
    """Create a realistic Django project structure."""
    # Main project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # manage.py
    with open(os.path.join(PROJECT_DIR, 'manage.py'), 'w') as f:
        f.write('''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
''')

    # mysite package (project config)
    mysite_dir = os.path.join(PROJECT_DIR, 'mysite')
    os.makedirs(mysite_dir, exist_ok=True)

    with open(os.path.join(mysite_dir, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(mysite_dir, 'settings.py'), 'w') as f:
        f.write('''"""
Django settings for mysite project.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-x7&k2m$p!q@r9s^t+u#v%w=y0z1a3b5c8d6e4f'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventory',
    'orders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
''')

    with open(os.path.join(mysite_dir, 'urls.py'), 'w') as f:
        f.write('''from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),
    path('orders/', include('orders.urls')),
]
''')

    with open(os.path.join(mysite_dir, 'wsgi.py'), 'w') as f:
        f.write('''import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
application = get_wsgi_application()
''')

    # --- inventory app ---
    inv_dir = os.path.join(PROJECT_DIR, 'inventory')
    os.makedirs(inv_dir, exist_ok=True)
    inv_migrations = os.path.join(inv_dir, 'migrations')
    os.makedirs(inv_migrations, exist_ok=True)

    with open(os.path.join(inv_dir, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(inv_migrations, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(inv_migrations, '0001_initial.py'), 'w') as f:
        f.write('''from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('sku', models.CharField(max_length=50, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock_quantity', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='inventory.category')),
            ],
        ),
    ]
''')

    with open(os.path.join(inv_dir, 'models.py'), 'w') as f:
        f.write('''from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def product_count(self):
        return self.products.count()

    @property
    def total_inventory_value(self):
        return sum(
            p.price * p.stock_quantity
            for p in self.products.filter(is_active=True)
        )


class Supplier(models.Model):
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    rating = models.FloatField(default=0.0)
    is_preferred = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

    @property
    def active_products(self):
        return self.supplied_products.filter(is_active=True)


class Product(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('refurbished', 'Refurbished'),
        ('used', 'Used'),
    ]

    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    condition = models.CharField(max_length=15, choices=CONDITION_CHOICES, default='new')
    weight = models.FloatField(null=True, blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='supplied_products'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def profit_margin(self):
        if self.cost_price and self.cost_price > 0:
            return ((self.price - self.cost_price) / self.cost_price) * 100
        return None

    @property
    def needs_reorder(self):
        return self.stock_quantity <= self.reorder_level

    @property
    def inventory_value(self):
        return self.price * self.stock_quantity

    def apply_discount(self, percentage):
        """Apply a percentage discount to the product price."""
        discount = self.price * (Decimal(str(percentage)) / Decimal('100'))
        self.price -= discount
        self.save()
        return self.price


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
        ('return', 'Return'),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='movements'
    )
    movement_type = models.CharField(max_length=15, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    performed_by = models.CharField(max_length=100, default='system')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.movement_type}: {self.quantity} x {self.product.name}"
''')

    with open(os.path.join(inv_dir, 'views.py'), 'w') as f:
        f.write('''from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Product, Category, Supplier, StockMovement


def product_list(request):
    """List all active products with optional category filter."""
    products = Product.objects.filter(is_active=True).select_related(
        'category', 'supplier'
    )
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'total_value': sum(p.inventory_value for p in products),
    }
    return render(request, 'inventory/product_list.html', context)


def product_detail(request, pk):
    """Show product detail with stock movement history."""
    product = get_object_or_404(
        Product.objects.select_related('category', 'supplier'), pk=pk
    )
    movements = product.movements.all()[:20]
    context = {
        'product': product,
        'movements': movements,
        'margin': product.profit_margin,
    }
    return render(request, 'inventory/product_detail.html', context)


@require_http_methods(["POST"])
def update_stock(request, pk):
    """Update stock quantity for a product."""
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get('quantity', 0))
    movement_type = request.POST.get('type', 'adjustment')

    StockMovement.objects.create(
        product=product,
        movement_type=movement_type,
        quantity=quantity,
        performed_by=request.user.username if request.user.is_authenticated else 'anonymous',
    )

    if movement_type in ('in', 'return'):
        product.stock_quantity += abs(quantity)
    elif movement_type == 'out':
        product.stock_quantity -= abs(quantity)
    else:
        product.stock_quantity = quantity

    product.save()
    return JsonResponse({
        'status': 'ok',
        'new_quantity': product.stock_quantity,
        'needs_reorder': product.needs_reorder,
    })


def low_stock_report(request):
    """Show products that need reordering."""
    products = Product.objects.filter(
        is_active=True,
        stock_quantity__lte=models.F('reorder_level')
    ).select_related('supplier')

    context = {
        'products': products,
        'count': products.count(),
    }
    return render(request, 'inventory/low_stock.html', context)
''')

    with open(os.path.join(inv_dir, 'urls.py'), 'w') as f:
        f.write('''from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/update-stock/', views.update_stock, name='update_stock'),
    path('low-stock/', views.low_stock_report, name='low_stock'),
]
''')

    with open(os.path.join(inv_dir, 'admin.py'), 'w') as f:
        f.write('''from django.contrib import admin
from .models import Category, Product, Supplier, StockMovement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'contact_person', 'email', 'rating', 'is_preferred']
    list_filter = ['is_preferred']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'stock_quantity', 'category', 'is_active']
    list_filter = ['category', 'is_active', 'condition']
    search_fields = ['name', 'sku']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'timestamp', 'performed_by']
    list_filter = ['movement_type']
''')

    # --- orders app ---
    ord_dir = os.path.join(PROJECT_DIR, 'orders')
    os.makedirs(ord_dir, exist_ok=True)
    ord_migrations = os.path.join(ord_dir, 'migrations')
    os.makedirs(ord_migrations, exist_ok=True)

    with open(os.path.join(ord_dir, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(ord_migrations, '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(ord_migrations, '0001_initial.py'), 'w') as f:
        f.write('''from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('inventory', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20, unique=True)),
                ('customer_name', models.CharField(max_length=200)),
                ('customer_email', models.EmailField()),
                ('status', models.CharField(max_length=20, default='pending')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.product')),
            ],
        ),
    ]
''')

    with open(os.path.join(ord_dir, 'models.py'), 'w') as f:
        f.write('''from django.db import models
from django.utils import timezone
from inventory.models import Product
from decimal import Decimal
import uuid


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    loyalty_points = models.PositiveIntegerField(default=0)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def total_orders(self):
        return self.orders.count()

    @property
    def total_spent(self):
        return sum(o.total_amount for o in self.orders.filter(status='completed'))


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    order_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='orders',
        null=True, blank=True
    )
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    shipping_address = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number} - {self.customer_name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return sum(item.line_total for item in self.items.all())

    @property
    def final_total(self):
        return self.subtotal + self.tax_amount - self.discount_amount

    @property
    def item_count(self):
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0

    def cancel(self):
        if self.status not in ('delivered', 'cancelled', 'refunded'):
            self.status = 'cancelled'
            for item in self.items.all():
                item.product.stock_quantity += item.quantity
                item.product.save()
            self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} @ {self.unit_price}"

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.price
        super().save(*args, **kwargs)
''')

    with open(os.path.join(ord_dir, 'views.py'), 'w') as f:
        f.write('''from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Order, OrderItem, Customer


def order_list(request):
    """List all orders with status filter."""
    orders = Order.objects.all().select_related('customer')
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)

    context = {
        'orders': orders,
        'statuses': Order.STATUS_CHOICES,
        'total_revenue': sum(o.final_total for o in orders.filter(status='completed')),
    }
    return render(request, 'orders/order_list.html', context)


def order_detail(request, pk):
    """Show order detail with items."""
    order = get_object_or_404(
        Order.objects.select_related('customer').prefetch_related('items__product'),
        pk=pk
    )
    context = {'order': order}
    return render(request, 'orders/order_detail.html', context)
''')

    with open(os.path.join(ord_dir, 'urls.py'), 'w') as f:
        f.write('''from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
]
''')

    with open(os.path.join(ord_dir, 'admin.py'), 'w') as f:
        f.write('''from django.contrib import admin
from .models import Order, OrderItem, Customer


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'city', 'loyalty_points', 'total_orders']
    search_fields = ['first_name', 'last_name', 'email']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'status', 'total_amount', 'created_at']
    list_filter = ['status']
    inlines = [OrderItemInline]
''')

    # requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('''Django>=4.2,<5.0
djangorestframework>=3.14
django-cors-headers>=4.0
django-filter>=23.0
Pillow>=10.0
celery>=5.3
redis>=5.0
''')

    # .gitignore
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write('''__pycache__/
*.py[cod]
*.so
db.sqlite3
.env
venv/
.vscode/
*.egg-info/
dist/
build/
''')

    # .vscode directory with workspace settings
    vscode_ws_dir = os.path.join(PROJECT_DIR, '.vscode')
    os.makedirs(vscode_ws_dir, exist_ok=True)

    with open(os.path.join(vscode_ws_dir, 'settings.json'), 'w') as f:
        json.dump({
            "python.defaultInterpreterPath": "/usr/bin/python3",
            "editor.formatOnSave": True,
            "editor.rulers": [88],
            "files.exclude": {
                "**/__pycache__": True,
                "**/*.pyc": True
            }
        }, f, indent=4)

    print(f'Django project created at: {PROJECT_DIR}')


def configure_vscode_strict():
    """Set VSCode global settings to strict type checking mode."""
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Set strict type checking - this is what causes the problem
    settings.update({
        "python.analysis.typeCheckingMode": "strict",
        "python.analysis.autoImportCompletions": True,
        "python.analysis.diagnosticMode": "workspace",
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.wordWrap": "off",
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings configured with strict type checking: {SETTINGS_PATH}')


def ensure_no_pyrightconfig():
    """Make sure no pyrightconfig.json exists in the project."""
    pyright_path = os.path.join(PROJECT_DIR, 'pyrightconfig.json')
    if os.path.exists(pyright_path):
        os.remove(pyright_path)
        print(f'Removed existing pyrightconfig.json')
    else:
        print(f'Confirmed: no pyrightconfig.json exists in {PROJECT_DIR}')


def main():
    create_django_project()
    configure_vscode_strict()
    ensure_no_pyrightconfig()

    # Open VSCode with the django project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with django-project and DISPLAY=:0')


main()

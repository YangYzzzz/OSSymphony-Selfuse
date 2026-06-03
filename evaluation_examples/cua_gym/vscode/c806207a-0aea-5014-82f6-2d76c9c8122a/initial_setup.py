"""
Initial Setup: Create a Django project workspace for VSCode debug configuration task.
Task ID: vscode_py_016
Domain: vscode

Sets up a Django project with manage.py at the root. No .vscode/launch.json exists.
VSCode is opened with the project folder.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_016'
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


def create_initial():
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/mysite', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/catalog', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/catalog/migrations', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/catalog/templates/catalog', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/static/css', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/templates', exist_ok=True)

    # Create manage.py
    with open(f'{PROJECT_DIR}/manage.py', 'w') as f:
        f.write('''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
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
    os.chmod(f'{PROJECT_DIR}/manage.py', 0o755)

    # Create mysite/__init__.py
    with open(f'{PROJECT_DIR}/mysite/__init__.py', 'w') as f:
        f.write('')

    # Create mysite/settings.py
    with open(f'{PROJECT_DIR}/mysite/settings.py', 'w') as f:
        f.write('''"""
Django settings for mysite project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-x7$k3m2p!q9r1t5v8w0y#b4d6f8h0j2l4n6p8r0t2v4x6z'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog.apps.CatalogConfig',
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mysite.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
''')

    # Create mysite/urls.py
    with open(f'{PROJECT_DIR}/mysite/urls.py', 'w') as f:
        f.write('''"""URL configuration for mysite project."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
]
''')

    # Create mysite/wsgi.py
    with open(f'{PROJECT_DIR}/mysite/wsgi.py', 'w') as f:
        f.write('''"""WSGI config for mysite project."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
application = get_wsgi_application()
''')

    # Create catalog app files
    with open(f'{PROJECT_DIR}/catalog/__init__.py', 'w') as f:
        f.write('')

    with open(f'{PROJECT_DIR}/catalog/apps.py', 'w') as f:
        f.write('''from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
''')

    with open(f'{PROJECT_DIR}/catalog/models.py', 'w') as f:
        f.write('''from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=100)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    class Meta:
        ordering = ['name']


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.customer_name}"
''')

    with open(f'{PROJECT_DIR}/catalog/views.py', 'w') as f:
        f.write('''from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Order


def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'catalog/order_list.html', {'orders': orders})
''')

    with open(f'{PROJECT_DIR}/catalog/urls.py', 'w') as f:
        f.write('''from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('orders/', views.order_list, name='order_list'),
]
''')

    with open(f'{PROJECT_DIR}/catalog/admin.py', 'w') as f:
        f.write('''from django.contrib import admin
from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'category', 'in_stock')
    list_filter = ('category', 'in_stock')
    search_fields = ('name', 'sku')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'status', 'total_amount', 'created_at')
    list_filter = ('status',)
''')

    with open(f'{PROJECT_DIR}/catalog/migrations/__init__.py', 'w') as f:
        f.write('')

    # Create a simple template
    with open(f'{PROJECT_DIR}/catalog/templates/catalog/product_list.html', 'w') as f:
        f.write('''{% extends "base.html" %}
{% block content %}
<h1>Product Catalog</h1>
<div class="product-grid">
{% for product in products %}
    <div class="product-card">
        <h2>{{ product.name }}</h2>
        <p class="price">${{ product.price }}</p>
        <p class="category">{{ product.category }}</p>
        <a href="{% url 'catalog:product_detail' product.pk %}">View Details</a>
    </div>
{% empty %}
    <p>No products available.</p>
{% endfor %}
</div>
{% endblock %}
''')

    with open(f'{PROJECT_DIR}/templates/base.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mysite Catalog</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <nav>
        <a href="{% url 'catalog:product_list' %}">Products</a>
        <a href="{% url 'catalog:order_list' %}">Orders</a>
    </nav>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
''')

    with open(f'{PROJECT_DIR}/static/css/style.css', 'w') as f:
        f.write('''body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
}

nav {
    background-color: #2c3e50;
    padding: 10px 20px;
    margin: -20px -20px 20px -20px;
}

nav a {
    color: white;
    text-decoration: none;
    margin-right: 20px;
}

.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
}

.product-card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.price {
    color: #27ae60;
    font-size: 1.2em;
    font-weight: bold;
}
''')

    # Create requirements.txt
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('''Django>=4.2,<5.0
djangorestframework>=3.14
django-cors-headers>=4.0
''')

    # Create .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write('''*.pyc
__pycache__/
db.sqlite3
.env
*.egg-info/
dist/
build/
.venv/
''')

    # IMPORTANT: Do NOT create .vscode/launch.json — that's the task
    print(f'Django project created at: {PROJECT_DIR}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

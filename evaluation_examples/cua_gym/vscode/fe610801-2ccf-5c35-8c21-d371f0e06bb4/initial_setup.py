"""
Initial Setup: Configure a Django project's launch.json for debugging
Task ID: vscode_py_063
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_063'
PROJECT_DIR = f'{WORKDIR}/myproject'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'


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
    # ---- Create Django project structure ----
    os.makedirs(f'{PROJECT_DIR}/myproject/settings', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/myproject/templates', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/blog', exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # manage.py
    with open(f'{PROJECT_DIR}/manage.py', 'w') as f:
        f.write('''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings.base')
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

    # myproject/__init__.py
    with open(f'{PROJECT_DIR}/myproject/__init__.py', 'w') as f:
        f.write('')

    # myproject/settings/__init__.py
    with open(f'{PROJECT_DIR}/myproject/settings/__init__.py', 'w') as f:
        f.write('from .base import *  # noqa\n')

    # myproject/settings/base.py
    with open(f'{PROJECT_DIR}/myproject/settings/base.py', 'w') as f:
        f.write('''"""
Django base settings for myproject.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'django-insecure-x$k3m!7@q9p+wz#cv&8f^uj2ry=5a(tn6b0_he4so1dgl%i'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
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

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'myproject' / 'templates'],
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

WSGI_APPLICATION = 'myproject.wsgi.application'

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
''')

    # myproject/settings/development.py
    with open(f'{PROJECT_DIR}/myproject/settings/development.py', 'w') as f:
        f.write('''"""
Development-specific settings for myproject.
Extends base settings with debug tools and verbose logging.
"""
from .base import *  # noqa

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = ['127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGGING['root']['level'] = 'DEBUG'
LOGGING['loggers'] = {
    'django.db.backends': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False,
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
''')

    # myproject/settings/production.py
    with open(f'{PROJECT_DIR}/myproject/settings/production.py', 'w') as f:
        f.write('''"""
Production settings for myproject.
Security-hardened configuration for deployment.
"""
from .base import *  # noqa
import os

DEBUG = False

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'myproject.example.com').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'myproject_prod'),
        'USER': os.environ.get('DB_USER', 'myproject'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

STATIC_ROOT = '/var/www/myproject/static/'
MEDIA_ROOT = '/var/www/myproject/media/'
''')

    # myproject/urls.py
    with open(f'{PROJECT_DIR}/myproject/urls.py', 'w') as f:
        f.write('''"""myproject URL Configuration"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]
''')

    # myproject/wsgi.py
    with open(f'{PROJECT_DIR}/myproject/wsgi.py', 'w') as f:
        f.write('''"""
WSGI config for myproject project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings.base')
application = get_wsgi_application()
''')

    # blog/__init__.py
    with open(f'{PROJECT_DIR}/blog/__init__.py', 'w') as f:
        f.write('')

    # blog/models.py
    with open(f'{PROJECT_DIR}/blog/models.py', 'w') as f:
        f.write('''from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def publish(self):
        self.status = 'published'
        self.published_at = timezone.now()
        self.save()
''')

    # blog/views.py
    with open(f'{PROJECT_DIR}/blog/views.py', 'w') as f:
        f.write('''from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('category')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published')


class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            status='published',
            category=self.category
        ).select_related('category')
''')

    # blog/urls.py
    with open(f'{PROJECT_DIR}/blog/urls.py', 'w') as f:
        f.write('''from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.CategoryPostListView.as_view(), name='category_posts'),
]
''')

    # blog/admin.py
    with open(f'{PROJECT_DIR}/blog/admin.py', 'w') as f:
        f.write('''from django.contrib import admin
from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created_at', 'published_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
''')

    # requirements.txt
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('''Django>=4.2,<5.0
django-debug-toolbar>=4.2
psycopg2-binary>=2.9
gunicorn>=21.2
''')

    # ---- Create .vscode/launch.json with BASIC Django config ----
    # This is the initial state: basic config WITHOUT the task-required changes
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Django",
                "type": "debugpy",
                "request": "launch",
                "program": "${workspaceFolder}/manage.py",
                "args": [
                    "runserver"
                ],
                "jinja": True,
                "justMyCode": True
            }
        ]
    }

    with open(f'{VSCODE_DIR}/launch.json', 'w') as f:
        json.dump(launch_config, f, indent=4)

    print(f'Initial Django project created at: {PROJECT_DIR}')
    print(f'launch.json created at: {VSCODE_DIR}/launch.json')

    # ---- GUI-ready startup: Open VSCode with the project ----
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

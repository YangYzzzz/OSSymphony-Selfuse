"""
Initial Setup: Create Django CMS project with manage.py, no .vscode/tasks.json
Task ID: vscode_td_034
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_034'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'django-cms')


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
    # Create Django project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'cms'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'cms', 'migrations'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'templates'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'static', 'css'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'static', 'js'), exist_ok=True)

    # Create manage.py
    manage_py = '''\
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_cms.settings')
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
'''
    with open(os.path.join(PROJECT_DIR, 'manage.py'), 'w') as f:
        f.write(manage_py)
    os.chmod(os.path.join(PROJECT_DIR, 'manage.py'), 0o755)

    # Create django_cms package (settings module)
    settings_dir = os.path.join(PROJECT_DIR, 'django_cms')
    os.makedirs(settings_dir, exist_ok=True)

    with open(os.path.join(settings_dir, '__init__.py'), 'w') as f:
        f.write('')

    settings_py = '''\
"""
Django settings for django_cms project.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-x7$k3m!9q2r5t8u1v4w6y0z3b5d7f9h2j4l6n8p0s'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cms',
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

ROOT_URLCONF = 'django_cms.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
'''
    with open(os.path.join(settings_dir, 'settings.py'), 'w') as f:
        f.write(settings_py)

    urls_py = '''\
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cms.urls')),
]
'''
    with open(os.path.join(settings_dir, 'urls.py'), 'w') as f:
        f.write(urls_py)

    # Create cms app files
    cms_dir = os.path.join(PROJECT_DIR, 'cms')

    with open(os.path.join(cms_dir, '__init__.py'), 'w') as f:
        f.write('')

    models_py = '''\
from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    label = models.CharField(max_length=100)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    external_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label
'''
    with open(os.path.join(cms_dir, 'models.py'), 'w') as f:
        f.write(models_py)

    views_py = '''\
from django.shortcuts import render, get_object_or_404
from .models import Page


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'cms/page_detail.html', {'page': page})


def home(request):
    pages = Page.objects.filter(is_published=True)[:5]
    return render(request, 'cms/home.html', {'pages': pages})
'''
    with open(os.path.join(cms_dir, 'views.py'), 'w') as f:
        f.write(views_py)

    urls_cms = '''\
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
]
'''
    with open(os.path.join(cms_dir, 'urls.py'), 'w') as f:
        f.write(urls_cms)

    admin_py = '''\
from django.contrib import admin
from .models import Page, MenuItem


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('label', 'page', 'order')
'''
    with open(os.path.join(cms_dir, 'admin.py'), 'w') as f:
        f.write(admin_py)

    # migrations __init__
    with open(os.path.join(cms_dir, 'migrations', '__init__.py'), 'w') as f:
        f.write('')

    # Ensure NO .vscode/tasks.json exists
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    tasks_path = os.path.join(vscode_dir, 'tasks.json')
    if os.path.exists(tasks_path):
        os.remove(tasks_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'manage.py exists: {os.path.exists(os.path.join(PROJECT_DIR, "manage.py"))}')
    print(f'.vscode/tasks.json exists: {os.path.exists(tasks_path)}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()

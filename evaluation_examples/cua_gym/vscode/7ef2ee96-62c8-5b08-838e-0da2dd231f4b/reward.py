"""
Reward Script: Django REST API project setup in VSCode
Task ID: vscode_gf4_031
Domain: vscode
Scoring:
  C1: venv with django, djangorestframework, django-filter, pytest-django (0.15)
  C2: Django project config/ with rest_framework in INSTALLED_APPS (0.15)
  C3: Product model with 5 fields (name, description, price, stock, category) (0.15)
  C4: ProductSerializer using ModelSerializer (0.10)
  C5: ProductViewSet using ModelViewSet (0.10)
  C6: URL routing for /api/products/ (0.10)
  C7: Test file with 6 test functions (0.15)
  C8: .vscode/launch.json for Django dev server (0.10)
"""

import os
import re
import json
import ast

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'django-rest-api')


def verify_task():
    total_score = 0.0

    # Component 1: venv with required packages (0.15 points)
    try:
        venv_pip = os.path.join(PROJECT, 'venv', 'bin', 'pip')
        if os.path.isfile(venv_pip):
            # Check installed packages by reading site-packages
            site_packages = None
            venv_lib = os.path.join(PROJECT, 'venv', 'lib')
            if os.path.isdir(venv_lib):
                for d in os.listdir(venv_lib):
                    sp = os.path.join(venv_lib, d, 'site-packages')
                    if os.path.isdir(sp):
                        site_packages = sp
                        break

            if site_packages:
                required_packages = {
                    'django': False,
                    'rest_framework': False,
                    'django_filters': False,
                    'pytest_django': False,
                }
                sp_dirs = os.listdir(site_packages)
                for entry in sp_dirs:
                    entry_lower = entry.lower()
                    if entry_lower.startswith('django') and not entry_lower.startswith('django_filter') and not entry_lower.startswith('djangorest'):
                        if 'dist-info' in entry_lower or entry_lower == 'django':
                            required_packages['django'] = True
                    if entry_lower.startswith('rest_framework') or entry_lower.startswith('djangorestframework'):
                        required_packages['rest_framework'] = True
                    if entry_lower.startswith('django_filter'):
                        required_packages['django_filters'] = True
                    if entry_lower.startswith('pytest_django') or entry_lower.startswith('pytest-django'):
                        required_packages['pytest_django'] = True

                found_count = sum(1 for v in required_packages.values() if v)
                if found_count == 4:
                    print(f"PASS: Component 1 - All 4 required packages found in venv (0.15 pts)")
                    total_score += 0.15
                else:
                    missing = [k for k, v in required_packages.items() if not v]
                    print(f"FAIL: Component 1 - Missing packages: {missing} ({found_count}/4 found)")
            else:
                print(f"FAIL: Component 1 - site-packages directory not found in venv")
        else:
            print(f"FAIL: Component 1 - venv/bin/pip not found at {venv_pip}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Django project config/ with rest_framework in INSTALLED_APPS (0.15 points)
    try:
        settings_path = os.path.join(PROJECT, 'config', 'settings.py')
        if os.path.isfile(settings_path):
            with open(settings_path, 'r') as f:
                settings_content = f.read()

            has_rest_framework = 'rest_framework' in settings_content
            has_products_app = "'products'" in settings_content or '"products"' in settings_content

            if has_rest_framework and has_products_app:
                print(f"PASS: Component 2 - config/settings.py has rest_framework and products in INSTALLED_APPS (0.15 pts)")
                total_score += 0.15
            else:
                details = []
                if not has_rest_framework:
                    details.append("rest_framework missing")
                if not has_products_app:
                    details.append("products app missing")
                print(f"FAIL: Component 2 - {', '.join(details)}")
        else:
            print(f"FAIL: Component 2 - config/settings.py not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Product model with 5 fields (0.15 points)
    try:
        models_path = os.path.join(PROJECT, 'products', 'models.py')
        if os.path.isfile(models_path):
            with open(models_path, 'r') as f:
                models_content = f.read()

            # Check for Product class and 5 required fields
            has_product_class = bool(re.search(r'class\s+Product\s*\(', models_content))
            required_fields = ['name', 'description', 'price', 'stock', 'category']
            found_fields = []
            for field in required_fields:
                # Match field definition: field_name = models.SomeField(...)
                if re.search(rf'{field}\s*=\s*models\.\w+Field', models_content):
                    found_fields.append(field)

            if has_product_class and len(found_fields) == 5:
                print(f"PASS: Component 3 - Product model with all 5 fields found (0.15 pts)")
                total_score += 0.15
            else:
                if not has_product_class:
                    print(f"FAIL: Component 3 - Product class not found")
                else:
                    missing = [f for f in required_fields if f not in found_fields]
                    print(f"FAIL: Component 3 - Missing fields: {missing}")
        else:
            print(f"FAIL: Component 3 - products/models.py not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: ProductSerializer with ModelSerializer (0.10 points)
    try:
        serializers_path = os.path.join(PROJECT, 'products', 'serializers.py')
        if os.path.isfile(serializers_path):
            with open(serializers_path, 'r') as f:
                ser_content = f.read()

            has_serializer_class = bool(re.search(r'class\s+ProductSerializer\s*\(', ser_content))
            has_model_serializer = 'ModelSerializer' in ser_content
            has_product_model_ref = 'Product' in ser_content

            if has_serializer_class and has_model_serializer and has_product_model_ref:
                print(f"PASS: Component 4 - ProductSerializer with ModelSerializer found (0.10 pts)")
                total_score += 0.10
            else:
                details = []
                if not has_serializer_class:
                    details.append("ProductSerializer class missing")
                if not has_model_serializer:
                    details.append("ModelSerializer not used")
                if not has_product_model_ref:
                    details.append("Product model not referenced")
                print(f"FAIL: Component 4 - {', '.join(details)}")
        else:
            print(f"FAIL: Component 4 - products/serializers.py not found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: ProductViewSet using ModelViewSet (0.10 points)
    try:
        views_path = os.path.join(PROJECT, 'products', 'views.py')
        if os.path.isfile(views_path):
            with open(views_path, 'r') as f:
                views_content = f.read()

            has_viewset_class = bool(re.search(r'class\s+ProductViewSet\s*\(', views_content))
            has_model_viewset = 'ModelViewSet' in views_content
            has_serializer_ref = 'ProductSerializer' in views_content

            if has_viewset_class and has_model_viewset and has_serializer_ref:
                print(f"PASS: Component 5 - ProductViewSet with ModelViewSet found (0.10 pts)")
                total_score += 0.10
            else:
                details = []
                if not has_viewset_class:
                    details.append("ProductViewSet class missing")
                if not has_model_viewset:
                    details.append("ModelViewSet not used")
                if not has_serializer_ref:
                    details.append("ProductSerializer not referenced")
                print(f"FAIL: Component 5 - {', '.join(details)}")
        else:
            print(f"FAIL: Component 5 - products/views.py not found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: URL routing configured for /api/products/ (0.10 points)
    try:
        config_urls_path = os.path.join(PROJECT, 'config', 'urls.py')
        products_urls_path = os.path.join(PROJECT, 'products', 'urls.py')

        config_urls_ok = False
        products_urls_ok = False

        if os.path.isfile(config_urls_path):
            with open(config_urls_path, 'r') as f:
                config_urls_content = f.read()
            # Check that config/urls.py includes products.urls under api/ path
            if 'products' in config_urls_content and 'include' in config_urls_content:
                config_urls_ok = True

        if os.path.isfile(products_urls_path):
            with open(products_urls_path, 'r') as f:
                products_urls_content = f.read()
            # Check that products/urls.py registers ProductViewSet with a router
            has_router = 'Router' in products_urls_content or 'router' in products_urls_content
            has_viewset_register = 'register' in products_urls_content and 'products' in products_urls_content
            if has_router and has_viewset_register:
                products_urls_ok = True

        if config_urls_ok and products_urls_ok:
            print(f"PASS: Component 6 - URL routing configured for /api/products/ (0.10 pts)")
            total_score += 0.10
        else:
            details = []
            if not config_urls_ok:
                details.append("config/urls.py doesn't include products.urls")
            if not products_urls_ok:
                details.append("products/urls.py doesn't register ProductViewSet with router")
            print(f"FAIL: Component 6 - {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Component 7: Test file with 6 test functions (0.15 points)
    try:
        # Look for test file in tests/ or products/tests.py
        test_path = None
        candidate_paths = [
            os.path.join(PROJECT, 'tests', 'test_products.py'),
            os.path.join(PROJECT, 'products', 'tests.py'),
            os.path.join(PROJECT, 'products', 'test_products.py'),
            os.path.join(PROJECT, 'test_products.py'),
        ]
        for cp in candidate_paths:
            if os.path.isfile(cp):
                test_path = cp
                break

        if test_path:
            with open(test_path, 'r') as f:
                test_content = f.read()

            # Count test functions (def test_*)
            test_functions = re.findall(r'def\s+(test_\w+)\s*\(', test_content)
            has_api_client = 'APIClient' in test_content or 'api_client' in test_content.lower()

            # Check for CRUD coverage
            crud_keywords = {
                'get_list': bool(re.search(r'test_\w*(get|list)\w*', test_content, re.IGNORECASE)),
                'get_detail': bool(re.search(r'test_\w*(detail|retrieve|single)\w*', test_content, re.IGNORECASE)),
                'create': bool(re.search(r'test_\w*(create|post)\w*', test_content, re.IGNORECASE)),
                'update': bool(re.search(r'test_\w*(update|put)\w*', test_content, re.IGNORECASE)),
                'delete': bool(re.search(r'test_\w*(delete|destroy)\w*', test_content, re.IGNORECASE)),
            }

            num_tests = len(test_functions)
            crud_count = sum(1 for v in crud_keywords.values() if v)

            if num_tests >= 6 and has_api_client and crud_count >= 5:
                print(f"PASS: Component 7 - {num_tests} test functions with APIClient and full CRUD coverage (0.15 pts)")
                total_score += 0.15
            else:
                details = []
                if num_tests < 6:
                    details.append(f"only {num_tests}/6 test functions found: {test_functions}")
                if not has_api_client:
                    details.append("APIClient not used")
                if crud_count < 5:
                    missing_crud = [k for k, v in crud_keywords.items() if not v]
                    details.append(f"missing CRUD tests: {missing_crud}")
                print(f"FAIL: Component 7 - {', '.join(details)}")
        else:
            print(f"FAIL: Component 7 - No test file found")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    # Component 8: .vscode/launch.json for Django dev server (0.10 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if os.path.isfile(launch_path):
            with open(launch_path, 'r') as f:
                launch_content = f.read()

            # Strip comments for JSON parsing
            cleaned = re.sub(r'//.*$', '', launch_content, flags=re.MULTILINE)
            launch_data = json.loads(cleaned)

            configurations = launch_data.get('configurations', [])
            has_django_config = False
            for config in configurations:
                # Check for Django runserver configuration
                program = config.get('program', '')
                args = config.get('args', [])
                django_flag = config.get('django', False)

                is_manage_py = 'manage.py' in program
                has_runserver = 'runserver' in args

                if is_manage_py and has_runserver:
                    has_django_config = True
                    break

            if has_django_config:
                print(f"PASS: Component 8 - launch.json has Django runserver configuration (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 8 - launch.json missing Django runserver configuration")
        else:
            print(f"FAIL: Component 8 - .vscode/launch.json not found")
    except Exception as e:
        print(f"ERROR: Component 8 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

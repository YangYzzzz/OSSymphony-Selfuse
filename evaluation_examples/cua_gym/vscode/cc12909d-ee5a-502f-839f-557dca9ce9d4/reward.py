"""
Reward Script: Flask API project setup in VSCode
Task ID: vscode_gf4_023
Domain: vscode
Scoring:
  C1 (0.15) - venv exists with required packages
  C2 (0.15) - app/__init__.py with create_app factory
  C3 (0.15) - app/models.py with User model (id, username, email, created_at)
  C4 (0.10) - app/schemas.py with UserSchema using marshmallow
  C5 (0.20) - app/routes/users.py with Blueprint and 5 CRUD routes
  C6 (0.10) - tests/conftest.py with test_client fixture and in-memory SQLite
  C7 (0.15) - .vscode/launch.json with Flask debug configuration
"""

import os
import json
import ast
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-flask-api')


def verify_task():
    total_score = 0.0

    # Component 1: venv/ exists with required packages installed (0.15 pts)
    try:
        venv_dir = os.path.join(PROJECT, 'venv')
        site_packages = None
        if os.path.isdir(venv_dir):
            # Find site-packages directory
            for root, dirs, files in os.walk(os.path.join(venv_dir, 'lib')):
                if 'site-packages' in dirs:
                    site_packages = os.path.join(root, 'site-packages')
                    break

        if site_packages and os.path.isdir(site_packages):
            required_pkgs = ['flask', 'flask_sqlalchemy', 'flask_migrate', 'marshmallow', 'pytest']
            found_pkgs = []
            pkg_dirs = os.listdir(site_packages)
            pkg_dirs_lower = [d.lower().replace('-', '_') for d in pkg_dirs]

            for pkg in required_pkgs:
                # Check for package directory or dist-info
                pkg_lower = pkg.lower().replace('-', '_')
                found = False
                for d in pkg_dirs:
                    d_norm = d.lower().replace('-', '_')
                    if d_norm == pkg_lower or d_norm.startswith(pkg_lower + '-') or d_norm.startswith(pkg_lower + '.'):
                        found = True
                        break
                    # Check dist-info entries
                    if '.dist-info' in d_norm and d_norm.startswith(pkg_lower):
                        found = True
                        break
                if found:
                    found_pkgs.append(pkg)

            if len(found_pkgs) == len(required_pkgs):
                print(f"PASS: Component 1 - venv with all 5 required packages ({found_pkgs}) (0.15 pts)")
                total_score += 0.15
            else:
                missing = set(required_pkgs) - set(found_pkgs)
                print(f"FAIL: Component 1 - missing packages: {missing} (found: {found_pkgs})")
        else:
            print(f"FAIL: Component 1 - venv directory or site-packages not found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: app/__init__.py with create_app factory (0.15 pts)
    try:
        init_path = os.path.join(PROJECT, 'app', '__init__.py')
        if os.path.exists(init_path):
            with open(init_path, 'r') as f:
                content = f.read()

            has_create_app = False
            has_flask_import = False
            has_sqlalchemy = False

            # Parse the AST to find create_app function
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == 'create_app':
                    has_create_app = True
                if isinstance(node, ast.ImportFrom):
                    if node.module == 'flask':
                        for alias in node.names:
                            if alias.name == 'Flask':
                                has_flask_import = True
                    if node.module == 'flask_sqlalchemy':
                        has_sqlalchemy = True

            if has_create_app and has_flask_import:
                print(f"PASS: Component 2 - app/__init__.py has create_app factory with Flask import (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 - create_app={has_create_app}, Flask import={has_flask_import}")
        else:
            print(f"FAIL: Component 2 - app/__init__.py not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: app/models.py with User model (id, username, email, created_at) (0.15 pts)
    try:
        models_path = os.path.join(PROJECT, 'app', 'models.py')
        if os.path.exists(models_path):
            with open(models_path, 'r') as f:
                content = f.read()

            has_user_class = False
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == 'User':
                    has_user_class = True

            # Check for required fields via text search (Column definitions)
            required_fields = ['id', 'username', 'email', 'created_at']
            found_fields = []
            for field in required_fields:
                # Look for field = db.Column(...) or similar pattern
                if re.search(rf'{field}\s*=\s*.*Column', content, re.IGNORECASE):
                    found_fields.append(field)

            if has_user_class and len(found_fields) == 4:
                print(f"PASS: Component 3 - User model with fields {found_fields} (0.15 pts)")
                total_score += 0.15
            else:
                missing = set(required_fields) - set(found_fields)
                print(f"FAIL: Component 3 - User class={has_user_class}, missing fields: {missing}")
        else:
            print(f"FAIL: Component 3 - app/models.py not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: app/schemas.py with UserSchema using marshmallow (0.10 pts)
    try:
        schemas_path = os.path.join(PROJECT, 'app', 'schemas.py')
        if os.path.exists(schemas_path):
            with open(schemas_path, 'r') as f:
                content = f.read()

            has_user_schema = False
            has_marshmallow = False

            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and 'UserSchema' in node.name:
                    has_user_schema = True
                if isinstance(node, ast.ImportFrom) and node.module and 'marshmallow' in node.module:
                    has_marshmallow = True

            if has_user_schema and has_marshmallow:
                print(f"PASS: Component 4 - UserSchema with marshmallow import (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 - UserSchema={has_user_schema}, marshmallow={has_marshmallow}")
        else:
            print(f"FAIL: Component 4 - app/schemas.py not found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: app/routes/users.py with Blueprint and 5 CRUD routes (0.20 pts)
    try:
        routes_path = os.path.join(PROJECT, 'app', 'routes', 'users.py')
        if os.path.exists(routes_path):
            with open(routes_path, 'r') as f:
                content = f.read()

            has_blueprint = 'Blueprint' in content

            # Check for the 5 required route methods
            # GET /users, GET /users/<id>, POST /users, PUT /users/<id>, DELETE /users/<id>
            route_patterns = {
                'GET_list': r"@\w+\.route\(['\"]\/users['\"].*methods\s*=\s*\[['\"]GET['\"]",
                'GET_single': r"@\w+\.route\(['\"]\/users\/<",
                'POST': r"methods\s*=\s*\[.*['\"]POST['\"]",
                'PUT': r"methods\s*=\s*\[.*['\"]PUT['\"]",
                'DELETE': r"methods\s*=\s*\[.*['\"]DELETE['\"]",
            }

            found_routes = []
            for name, pattern in route_patterns.items():
                if re.search(pattern, content):
                    found_routes.append(name)

            sub_score = 0.0
            if has_blueprint:
                sub_score += 0.04  # Blueprint exists
            route_credit = min(len(found_routes), 5) * 0.032  # ~0.16 for all 5
            sub_score += route_credit

            if sub_score > 0:
                sub_score = min(sub_score, 0.20)
                print(f"PASS: Component 5 - Blueprint={has_blueprint}, routes found: {found_routes} ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 5 - Blueprint={has_blueprint}, routes={found_routes}")
        else:
            print(f"FAIL: Component 5 - app/routes/users.py not found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: tests/conftest.py with test_client fixture and in-memory SQLite (0.10 pts)
    try:
        conftest_path = os.path.join(PROJECT, 'tests', 'conftest.py')
        if os.path.exists(conftest_path):
            with open(conftest_path, 'r') as f:
                content = f.read()

            has_fixture = '@pytest.fixture' in content or 'fixture' in content
            has_test_client = 'test_client' in content
            has_memory_sqlite = 'sqlite:///:memory:' in content or 'testing' in content.lower()

            if has_fixture and has_test_client:
                print(f"PASS: Component 6 - conftest.py with test_client fixture (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 - fixture={has_fixture}, test_client={has_test_client}, memory_sqlite={has_memory_sqlite}")
        else:
            print(f"FAIL: Component 6 - tests/conftest.py not found")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Component 7: .vscode/launch.json with Flask debug configuration (0.15 pts)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if os.path.exists(launch_path):
            with open(launch_path, 'r') as f:
                content = f.read()

            # Strip comments for JSON parsing
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            launch_config = json.loads(cleaned)

            configs = launch_config.get('configurations', [])
            has_flask_config = False
            for cfg in configs:
                # Check for flask module or flask-related settings
                module = cfg.get('module', '')
                env = cfg.get('env', {})
                flask_app = env.get('FLASK_APP', '')
                if 'flask' in module.lower() or 'flask' in flask_app.lower():
                    has_flask_config = True
                    break

            if has_flask_config:
                print(f"PASS: Component 7 - launch.json with Flask debug configuration (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 7 - No Flask configuration found in launch.json")
        else:
            print(f"FAIL: Component 7 - .vscode/launch.json not found")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

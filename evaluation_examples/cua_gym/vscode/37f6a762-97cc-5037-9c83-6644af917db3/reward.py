"""
Reward Script: JWT Authentication Service for FastAPI
Task ID: vscode_gf4_038
Domain: vscode
Scoring:
  C1 (0.15) - venv with required packages
  C2 (0.15) - app/models.py with User model including hashed_password
  C3 (0.15) - app/auth.py with hash_password, verify_password, create_access_token, decode_token
  C4 (0.15) - app/routes/auth.py with /register, /login, /me endpoints
  C5 (0.10) - alembic/ directory with migration
  C6 (0.10) - tests/ with >=5 tests
  C7 (0.10) - .vscode/launch.json with FastAPI debug config
  C8 (0.10) - .env file with SECRET_KEY
"""

import os
import json
import ast
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-auth-service')


def verify_task():
    total_score = 0.0

    # Component 1: Virtual environment with required packages (0.15 points)
    try:
        venv_pip = os.path.join(PROJECT, 'venv', 'bin', 'pip')
        site_packages = None
        venv_lib = os.path.join(PROJECT, 'venv', 'lib')
        if os.path.isdir(venv_lib):
            for d in os.listdir(venv_lib):
                sp = os.path.join(venv_lib, d, 'site-packages')
                if os.path.isdir(sp):
                    site_packages = sp
                    break

        if site_packages is None:
            print("FAIL: Component 1 — venv/lib/*/site-packages not found")
        else:
            # Check required packages by looking for dist-info or package dirs
            required = {
                'fastapi': False,
                'pyjwt': False,
                'passlib': False,
                'sqlalchemy': False,
                'aiosqlite': False,
                'alembic': False,
                'pytest-asyncio': False,
            }
            pkg_dirs = os.listdir(site_packages)
            pkg_dirs_lower = [d.lower() for d in pkg_dirs]

            for pkg in required:
                pkg_lower = pkg.lower().replace('-', '_')
                for d in pkg_dirs_lower:
                    # Match dist-info directories or package directories
                    d_norm = d.replace('-', '_')
                    if d_norm.startswith(pkg_lower):
                        required[pkg] = True
                        break
                # Special cases
                if pkg == 'pyjwt':
                    for d in pkg_dirs_lower:
                        if d.startswith('pyjwt') or d == 'jwt':
                            required[pkg] = True
                            break

            found = sum(1 for v in required.values() if v)
            if found == len(required):
                print(f"PASS: Component 1 — All {len(required)} required packages found in venv (0.15 pts)")
                total_score += 0.15
            else:
                missing = [k for k, v in required.items() if not v]
                print(f"FAIL: Component 1 — Missing packages: {missing} ({found}/{len(required)} found)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: app/models.py with User model including hashed_password (0.15 points)
    try:
        models_path = os.path.join(PROJECT, 'app', 'models.py')
        if not os.path.isfile(models_path):
            print("FAIL: Component 2 — app/models.py does not exist")
        else:
            with open(models_path, 'r') as f:
                models_content = f.read()
            has_user_class = 'class User' in models_content
            has_hashed_password = 'hashed_password' in models_content
            has_sqlalchemy = 'sqlalchemy' in models_content or 'Column' in models_content

            if has_user_class and has_hashed_password and has_sqlalchemy:
                print(f"PASS: Component 2 — User model with hashed_password field found (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — User class: {has_user_class}, hashed_password: {has_hashed_password}, SQLAlchemy: {has_sqlalchemy}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: app/auth.py with required functions (0.15 points)
    try:
        auth_path = os.path.join(PROJECT, 'app', 'auth.py')
        if not os.path.isfile(auth_path):
            print("FAIL: Component 3 — app/auth.py does not exist")
        else:
            with open(auth_path, 'r') as f:
                auth_content = f.read()

            required_funcs = ['hash_password', 'verify_password', 'create_access_token', 'decode_token']
            # Parse AST to find function definitions
            try:
                tree = ast.parse(auth_content)
                defined_funcs = [node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
            except SyntaxError:
                # Fallback to regex
                defined_funcs = re.findall(r'def\s+(\w+)\s*\(', auth_content)

            found_funcs = [f for f in required_funcs if f in defined_funcs]

            if len(found_funcs) == len(required_funcs):
                print(f"PASS: Component 3 — All 4 auth functions found: {found_funcs} (0.15 pts)")
                total_score += 0.15
            else:
                missing = [f for f in required_funcs if f not in defined_funcs]
                print(f"FAIL: Component 3 — Missing functions: {missing}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: app/routes/auth.py with /register, /login, /me endpoints (0.15 points)
    try:
        routes_path = os.path.join(PROJECT, 'app', 'routes', 'auth.py')
        if not os.path.isfile(routes_path):
            print("FAIL: Component 4 — app/routes/auth.py does not exist")
        else:
            with open(routes_path, 'r') as f:
                routes_content = f.read()

            # Check for endpoint decorators/definitions
            has_register = bool(re.search(r'["\'/]register["\']', routes_content) or 'register' in routes_content)
            has_login = bool(re.search(r'["\'/]login["\']', routes_content) or 'login' in routes_content)
            has_me = bool(re.search(r'["\'/]me["\']', routes_content))
            has_post = '.post(' in routes_content
            has_get = '.get(' in routes_content

            # Check for POST /register, POST /login, GET /me
            has_post_register = bool(re.search(r'\.post\(["\']\/register["\']', routes_content))
            has_post_login = bool(re.search(r'\.post\(["\']\/login["\']', routes_content))
            has_get_me = bool(re.search(r'\.get\(["\']\/me["\']', routes_content))

            # Also accept decorator-style route definitions
            if not has_post_register:
                has_post_register = bool(re.search(r'post.*register|register.*post', routes_content, re.IGNORECASE))
            if not has_post_login:
                has_post_login = bool(re.search(r'post.*login|login.*post', routes_content, re.IGNORECASE))
            if not has_get_me:
                has_get_me = bool(re.search(r'get.*["\'/]me["\']', routes_content, re.IGNORECASE))

            # Check for Bearer token requirement on /me
            has_bearer = 'Bearer' in routes_content or 'HTTPBearer' in routes_content or 'Depends' in routes_content

            if has_post_register and has_post_login and has_get_me and has_bearer:
                print(f"PASS: Component 4 — All 3 endpoints found with auth (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — POST /register: {has_post_register}, POST /login: {has_post_login}, GET /me: {has_get_me}, Bearer: {has_bearer}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: alembic/ directory with migration (0.10 points)
    try:
        alembic_dir = os.path.join(PROJECT, 'alembic')
        alembic_ini = os.path.join(PROJECT, 'alembic.ini')
        versions_dir = os.path.join(alembic_dir, 'versions')

        has_alembic_dir = os.path.isdir(alembic_dir)
        has_alembic_ini = os.path.isfile(alembic_ini)
        has_env_py = os.path.isfile(os.path.join(alembic_dir, 'env.py'))

        has_migration = False
        if os.path.isdir(versions_dir):
            migration_files = [f for f in os.listdir(versions_dir) if f.endswith('.py')]
            if migration_files:
                # Check that at least one migration references users table
                for mf in migration_files:
                    with open(os.path.join(versions_dir, mf), 'r') as f:
                        content = f.read()
                    if 'users' in content or 'user' in content.lower():
                        has_migration = True
                        break

        if has_alembic_dir and has_env_py and has_migration:
            print(f"PASS: Component 5 — Alembic setup with User migration found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — alembic dir: {has_alembic_dir}, env.py: {has_env_py}, migration: {has_migration}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: tests/ with at least 5 tests (0.10 points)
    try:
        tests_dir = os.path.join(PROJECT, 'tests')
        if not os.path.isdir(tests_dir):
            print("FAIL: Component 6 — tests/ directory does not exist")
        else:
            # Find test files
            test_files = [f for f in os.listdir(tests_dir) if f.startswith('test_') and f.endswith('.py')]
            if not test_files:
                print("FAIL: Component 6 — No test files found in tests/")
            else:
                total_tests = 0
                for tf in test_files:
                    with open(os.path.join(tests_dir, tf), 'r') as f:
                        content = f.read()
                    # Count test functions
                    test_funcs = re.findall(r'(?:async\s+)?def\s+(test_\w+)\s*\(', content)
                    total_tests += len(test_funcs)

                if total_tests >= 5:
                    print(f"PASS: Component 6 — {total_tests} tests found (>= 5 required) (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 6 — Only {total_tests} tests found (need >= 5)")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: .vscode/launch.json with FastAPI debug config (0.10 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if not os.path.isfile(launch_path):
            print("FAIL: Component 7 — .vscode/launch.json does not exist")
        else:
            with open(launch_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            try:
                launch_config = json.loads(content_clean)
            except json.JSONDecodeError:
                # Try stripping trailing commas
                content_clean = re.sub(r',\s*([}\]])', r'\1', content_clean)
                launch_config = json.loads(content_clean)

            configs = launch_config.get('configurations', [])
            has_fastapi = False
            for cfg in configs:
                # Check for uvicorn/fastapi related config
                module = cfg.get('module', '')
                program = cfg.get('program', '')
                args = cfg.get('args', [])
                name = cfg.get('name', '').lower()
                args_str = ' '.join(args) if isinstance(args, list) else str(args)

                if ('uvicorn' in module or 'uvicorn' in args_str or
                    'fastapi' in name or 'fastapi' in module or
                    'app.main:app' in args_str or 'app.main' in args_str):
                    has_fastapi = True
                    break

            if has_fastapi:
                print(f"PASS: Component 7 — FastAPI/uvicorn debug config found (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — No FastAPI/uvicorn config in launch.json")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: .env file with SECRET_KEY (0.10 points)
    try:
        env_path = os.path.join(PROJECT, '.env')
        if not os.path.isfile(env_path):
            print("FAIL: Component 8 — .env file does not exist")
        else:
            with open(env_path, 'r') as f:
                env_content = f.read()

            has_secret_key = bool(re.search(r'^SECRET_KEY\s*=\s*.+', env_content, re.MULTILINE))

            if has_secret_key:
                print(f"PASS: Component 8 — .env contains SECRET_KEY (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 8 — SECRET_KEY not found in .env")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    final_score = min(total_score, 1.0)
    # Round to avoid float precision issues
    final_score = round(final_score, 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

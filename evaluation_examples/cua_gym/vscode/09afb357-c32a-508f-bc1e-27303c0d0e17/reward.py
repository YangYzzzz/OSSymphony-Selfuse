"""
Reward Script: FastAPI OpenAPI spec generation and validation in VSCode project
Task ID: vscode_gf6_062
Domain: vscode
Scoring:
  Component 1 (0.15): Required packages installed in venv
  Component 2 (0.25): src/main.py with 5 CRUD endpoints
  Component 3 (0.15): Pydantic models (UserCreate, UserResponse, UserUpdate)
  Component 4 (0.10): FastAPI app metadata (title, version, description)
  Component 5 (0.20): openapi.json exists and is valid OpenAPI spec
  Component 6 (0.15): .vscode/tasks.json with 'Generate OpenAPI Spec' task
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'python-openapi')
TASK_ID = 'vscode_gf6_062'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================================
    # Component 1: Required packages installed in venv (0.15 points)
    # Checks: fastapi, uvicorn, pydantic (v2), openapi-spec-validator
    # =========================================================================
    try:
        venv_site = None
        venv_lib = os.path.join(PROJECT_DIR, 'venv', 'lib')
        if os.path.isdir(venv_lib):
            for d in os.listdir(venv_lib):
                sp = os.path.join(venv_lib, d, 'site-packages')
                if os.path.isdir(sp):
                    venv_site = sp
                    break

        if venv_site is None:
            print("FAIL: Component 1 -- venv site-packages not found")
        else:
            required_pkgs = {
                'fastapi': False,
                'uvicorn': False,
                'pydantic': False,
                'openapi_spec_validator': False,
            }
            entries = os.listdir(venv_site)
            for entry in entries:
                entry_lower = entry.lower()
                if entry_lower.startswith('fastapi'):
                    required_pkgs['fastapi'] = True
                elif entry_lower.startswith('uvicorn'):
                    required_pkgs['uvicorn'] = True
                elif entry_lower.startswith('pydantic') and 'core' not in entry_lower and 'settings' not in entry_lower:
                    required_pkgs['pydantic'] = True
                elif entry_lower.startswith('openapi_spec_validator'):
                    required_pkgs['openapi_spec_validator'] = True

            # Check pydantic is v2 by looking for pydantic_core (v2 dependency)
            pydantic_v2 = any(e.lower().startswith('pydantic_core') for e in entries)

            installed = sum(1 for v in required_pkgs.values() if v)
            if installed == 4 and pydantic_v2:
                print(f"PASS: Component 1 -- All 4 packages installed, pydantic v2 confirmed (0.15 pts)")
                total_score += 0.15
            else:
                missing = [k for k, v in required_pkgs.items() if not v]
                print(f"FAIL: Component 1 -- installed={installed}/4, missing={missing}, pydantic_v2={pydantic_v2}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # =========================================================================
    # Component 2: src/main.py exists with 5 CRUD endpoints (0.25 points)
    # GET /users, POST /users, GET /users/{{user_id}}, PUT /users/{{user_id}}, DELETE /users/{{user_id}}
    # =========================================================================
    main_py_path = os.path.join(PROJECT_DIR, 'src', 'main.py')
    main_py_content = None
    try:
        if not os.path.isfile(main_py_path):
            print(f"FAIL: Component 2 -- src/main.py does not exist")
        else:
            with open(main_py_path, 'r') as f:
                main_py_content = f.read()

            # Check for the 5 endpoint decorators
            endpoints_found = 0
            endpoint_patterns = [
                (r'@app\.get\s*\(\s*["\']\/users["\']', 'GET /users'),
                (r'@app\.post\s*\(\s*["\']\/users["\']', 'POST /users'),
                (r'@app\.get\s*\(\s*["\']\/users\/\{', 'GET /users/{user_id}'),
                (r'@app\.put\s*\(\s*["\']\/users\/\{', 'PUT /users/{user_id}'),
                (r'@app\.delete\s*\(\s*["\']\/users\/\{', 'DELETE /users/{user_id}'),
            ]
            for pattern, name in endpoint_patterns:
                if re.search(pattern, main_py_content):
                    endpoints_found += 1
                else:
                    print(f"  DETAIL: Missing endpoint {name}")

            if endpoints_found == 5:
                print(f"PASS: Component 2 -- All 5 CRUD endpoints found in src/main.py (0.25 pts)")
                total_score += 0.25
            elif endpoints_found >= 3:
                partial = round(0.25 * (endpoints_found / 5), 2)
                print(f"PARTIAL: Component 2 -- {endpoints_found}/5 endpoints found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 -- Only {endpoints_found}/5 endpoints found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # =========================================================================
    # Component 3: Pydantic models defined (0.15 points)
    # UserCreate (name, email, role), UserResponse (id, name, email, role, created_at),
    # UserUpdate (optional name, email, role)
    # =========================================================================
    try:
        if main_py_content is None:
            print("FAIL: Component 3 -- src/main.py not available")
        else:
            models_found = 0

            # Check UserCreate
            if re.search(r'class\s+UserCreate\b', main_py_content):
                # Verify it has name, email, role fields
                uc_match = re.search(r'class\s+UserCreate\b.*?(?=\nclass\s|\Z)', main_py_content, re.DOTALL)
                if uc_match:
                    uc_body = uc_match.group()
                    if all(f in uc_body for f in ['name', 'email', 'role']):
                        models_found += 1
                    else:
                        print("  DETAIL: UserCreate missing fields")
                else:
                    models_found += 1  # class exists at least

            # Check UserResponse
            if re.search(r'class\s+UserResponse\b', main_py_content):
                ur_match = re.search(r'class\s+UserResponse\b.*?(?=\nclass\s|\Z)', main_py_content, re.DOTALL)
                if ur_match:
                    ur_body = ur_match.group()
                    if all(f in ur_body for f in ['id', 'name', 'email', 'role', 'created_at']):
                        models_found += 1
                    else:
                        print("  DETAIL: UserResponse missing fields")
                else:
                    models_found += 1

            # Check UserUpdate
            if re.search(r'class\s+UserUpdate\b', main_py_content):
                uu_match = re.search(r'class\s+UserUpdate\b.*?(?=\nclass\s|\Z)', main_py_content, re.DOTALL)
                if uu_match:
                    uu_body = uu_match.group()
                    if 'Optional' in uu_body or 'None' in uu_body:
                        if all(f in uu_body for f in ['name', 'email', 'role']):
                            models_found += 1
                        else:
                            print("  DETAIL: UserUpdate missing fields")
                    else:
                        print("  DETAIL: UserUpdate fields not Optional")
                else:
                    models_found += 1

            if models_found == 3:
                print(f"PASS: Component 3 -- All 3 Pydantic models correctly defined (0.15 pts)")
                total_score += 0.15
            elif models_found >= 1:
                partial = round(0.15 * (models_found / 3), 2)
                print(f"PARTIAL: Component 3 -- {models_found}/3 models found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- No Pydantic models found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # =========================================================================
    # Component 4: FastAPI app metadata (0.10 points)
    # title, version, description set on the app
    # =========================================================================
    try:
        if main_py_content is None:
            print("FAIL: Component 4 -- src/main.py not available")
        else:
            # Check for FastAPI(...) with title, version, description
            has_title = bool(re.search(r'FastAPI\s*\(.*title\s*=', main_py_content, re.DOTALL))
            has_version = bool(re.search(r'FastAPI\s*\(.*version\s*=', main_py_content, re.DOTALL))
            has_description = bool(re.search(r'FastAPI\s*\(.*description\s*=', main_py_content, re.DOTALL))

            meta_count = sum([has_title, has_version, has_description])
            if meta_count == 3:
                print(f"PASS: Component 4 -- FastAPI app has title, version, description (0.10 pts)")
                total_score += 0.10
            else:
                missing = []
                if not has_title:
                    missing.append('title')
                if not has_version:
                    missing.append('version')
                if not has_description:
                    missing.append('description')
                print(f"FAIL: Component 4 -- Missing metadata: {missing}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # =========================================================================
    # Component 5: openapi.json exists and is a valid OpenAPI spec (0.20 points)
    # Must have 'openapi' version key, 'info' with title/version, 'paths' with user endpoints
    # =========================================================================
    try:
        openapi_path = os.path.join(PROJECT_DIR, 'openapi.json')
        if not os.path.isfile(openapi_path):
            print("FAIL: Component 5 -- openapi.json does not exist")
        else:
            with open(openapi_path, 'r') as f:
                spec = json.load(f)

            checks_passed = 0
            total_checks = 4

            # Check 'openapi' version field
            if 'openapi' in spec and isinstance(spec['openapi'], str):
                checks_passed += 1
            else:
                print("  DETAIL: Missing 'openapi' version field")

            # Check 'info' with title and version
            info = spec.get('info', {})
            if isinstance(info, dict) and 'title' in info and 'version' in info:
                checks_passed += 1
            else:
                print("  DETAIL: Missing or incomplete 'info' section")

            # Check 'paths' has /users endpoints
            paths = spec.get('paths', {})
            if '/users' in paths and '/users/{user_id}' in paths:
                checks_passed += 1
            else:
                print(f"  DETAIL: Missing user paths, found: {list(paths.keys())}")

            # Check schemas include UserCreate, UserResponse, UserUpdate
            schemas = spec.get('components', {}).get('schemas', {})
            required_schemas = ['UserCreate', 'UserResponse', 'UserUpdate']
            if all(s in schemas for s in required_schemas):
                checks_passed += 1
            else:
                found = [s for s in required_schemas if s in schemas]
                print(f"  DETAIL: Found schemas {found}, need {required_schemas}")

            if checks_passed == total_checks:
                print(f"PASS: Component 5 -- openapi.json is valid with all required sections (0.20 pts)")
                total_score += 0.20
            elif checks_passed >= 2:
                partial = round(0.20 * (checks_passed / total_checks), 2)
                print(f"PARTIAL: Component 5 -- {checks_passed}/{total_checks} checks passed ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 -- Only {checks_passed}/{total_checks} checks passed")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 5 -- openapi.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # =========================================================================
    # Component 6: .vscode/tasks.json with 'Generate OpenAPI Spec' task (0.15 points)
    # =========================================================================
    try:
        tasks_path = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
        if not os.path.isfile(tasks_path):
            print("FAIL: Component 6 -- .vscode/tasks.json does not exist")
        else:
            with open(tasks_path, 'r') as f:
                tasks_config = json.load(f)

            tasks_list = tasks_config.get('tasks', [])
            matching = [t for t in tasks_list if 'generate openapi spec' in t.get('label', '').lower()]

            if len(matching) > 0:
                print(f"PASS: Component 6 -- 'Generate OpenAPI Spec' task found in tasks.json (0.15 pts)")
                total_score += 0.15
            else:
                labels = [t.get('label', '') for t in tasks_list]
                print(f"FAIL: Component 6 -- 'Generate OpenAPI Spec' task not found, labels: {labels}")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 6 -- tasks.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

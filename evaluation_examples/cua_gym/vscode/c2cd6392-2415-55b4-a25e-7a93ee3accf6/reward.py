"""
Reward Script: API testing workflow setup in VSCode
Task ID: vscode_wf_060
Domain: vs_code
Scoring:
  - Component 1: REST Client extension installed (0.15)
  - Component 2: api_tests/users.http exists with GET, POST, PUT, DELETE requests (0.30)
  - Component 3: users.http uses {{baseUrl}} variable syntax (0.10)
  - Component 4: settings.json has rest-client.environmentVariables with local/staging/production (0.25)
  - Component 5: tasks.json has start-server and api-test tasks (0.20)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_060'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: REST Client extension installed (0.15 points)
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        if os.path.isdir(ext_dir):
            ext_folders = os.listdir(ext_dir)
            # Extension directories are named like "humao.rest-client-0.25.1"
            rest_client_found = any(
                entry.lower().startswith('humao.rest-client')
                for entry in ext_folders
                if not entry.endswith('.json')
            )
            if rest_client_found:
                print(f"PASS: Component 1 — REST Client extension installed (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — REST Client extension not found. Extensions: {ext_folders}")
        else:
            print(f"FAIL: Component 1 — Extensions directory not found at {ext_dir}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: api_tests/users.http exists with GET, POST, PUT, DELETE (0.30 points)
    try:
        http_file = os.path.join(PROJECT, 'api_tests', 'users.http')
        if not os.path.exists(http_file):
            print(f"FAIL: Component 2 — {http_file} does not exist")
        else:
            with open(http_file, 'r') as f:
                content = f.read()

            methods_found = []
            required_methods = ['GET', 'POST', 'PUT', 'DELETE']
            for method in required_methods:
                # Match HTTP method at beginning of line followed by space and URL pattern
                if re.search(rf'^{method}\s+', content, re.MULTILINE):
                    methods_found.append(method)

            if len(methods_found) == 4:
                print(f"PASS: Component 2 — users.http has all 4 methods: {methods_found} (0.30 pts)")
                total_score += 0.30
            elif len(methods_found) >= 2:
                partial = round(0.30 * len(methods_found) / 4, 2)
                print(f"PARTIAL: Component 2 — users.http has {len(methods_found)}/4 methods: {methods_found} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — users.http has {len(methods_found)}/4 methods: {methods_found}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: users.http uses {{baseUrl}} variable syntax (0.10 points)
    try:
        http_file = os.path.join(PROJECT, 'api_tests', 'users.http')
        if not os.path.exists(http_file):
            print(f"FAIL: Component 3 — users.http does not exist")
        else:
            with open(http_file, 'r') as f:
                content = f.read()
            # Check for {{baseUrl}} or {{base_url}} or similar variable syntax
            if '{{baseUrl}}' in content or '{{base_url}}' in content:
                print(f"PASS: Component 3 — users.http uses {{{{baseUrl}}}} variable syntax (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — users.http does not use {{{{baseUrl}}}} variable syntax")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: settings.json has rest-client.environmentVariables with local/staging/production (0.25 points)
    try:
        settings_path = os.path.join(PROJECT, '.vscode', 'settings.json')
        if not os.path.exists(settings_path):
            print(f"FAIL: Component 4 — {settings_path} does not exist")
        else:
            with open(settings_path, 'r') as f:
                raw = f.read()
            # Strip JSONC comments (only // at start of line or after whitespace, not in URLs)
            cleaned = re.sub(r'(?<![:\"\'])//.*$', '', raw, flags=re.MULTILINE)
            try:
                settings = json.loads(cleaned)
            except json.JSONDecodeError:
                # Fallback: try parsing raw (no comments)
                settings = json.loads(raw)

            env_vars = settings.get('rest-client.environmentVariables', {})
            required_envs = ['local', 'staging', 'production']
            envs_found = []
            envs_with_baseurl = []

            for env_name in required_envs:
                if env_name in env_vars:
                    envs_found.append(env_name)
                    env_data = env_vars[env_name]
                    if isinstance(env_data, dict) and 'baseUrl' in env_data:
                        envs_with_baseurl.append(env_name)

            # Check that each environment has a DIFFERENT baseUrl
            base_urls = set()
            for env_name in envs_with_baseurl:
                base_urls.add(env_vars[env_name]['baseUrl'])

            if len(envs_with_baseurl) == 3 and len(base_urls) >= 3:
                print(f"PASS: Component 4 — settings.json has all 3 environments with distinct baseUrls (0.25 pts)")
                total_score += 0.25
            elif len(envs_found) >= 2:
                partial = round(0.25 * len(envs_with_baseurl) / 3, 2)
                print(f"PARTIAL: Component 4 — {len(envs_with_baseurl)}/3 envs with baseUrl ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — environments found: {envs_found}, with baseUrl: {envs_with_baseurl}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: tasks.json has start-server and api-test tasks (0.20 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if not os.path.exists(tasks_path):
            print(f"FAIL: Component 5 — {tasks_path} does not exist")
        else:
            with open(tasks_path, 'r') as f:
                raw = f.read()
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            tasks_config = json.loads(cleaned)

            task_labels = []
            if 'tasks' in tasks_config:
                task_labels = [t.get('label', '') for t in tasks_config['tasks']]

            has_start_server = any('start' in l.lower() and 'server' in l.lower() for l in task_labels)
            has_api_test = any('api' in l.lower() and 'test' in l.lower() for l in task_labels)

            if has_start_server and has_api_test:
                print(f"PASS: Component 5 — tasks.json has start-server and api-test tasks (0.20 pts)")
                total_score += 0.20
            elif has_start_server or has_api_test:
                print(f"PARTIAL: Component 5 — tasks.json has only one of the two tasks (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — tasks.json missing required tasks. Found labels: {task_labels}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

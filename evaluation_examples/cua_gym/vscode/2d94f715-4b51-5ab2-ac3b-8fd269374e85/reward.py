"""
Reward Script: Full-stack Todo App Initialization in VSCode
Task ID: vscode_gf4_028
Domain: vscode
Scoring:
  1. client/package.json with React + TypeScript deps (0.15)
  2. client/src/components/TodoList.tsx with add/toggle/delete (0.20)
  3. server/package.json with express + TypeScript deps (0.15)
  4. server/src/routes/todos.ts with 4 REST endpoints (0.20)
  5. todo.code-workspace referencing both folders (0.10)
  6. client/.vscode/launch.json exists (0.10)
  7. server/.vscode/launch.json exists (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_028'
BASE = os.path.join(WORKDIR, 'projects', 'full-stack-todo')


def verify_task():
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    # Component 1: client/package.json with React + TypeScript dependencies (0.15 points)
    try:
        client_pkg_path = os.path.join(BASE, 'client', 'package.json')
        with open(client_pkg_path, 'r') as f:
            client_pkg = json.load(f)

        deps = {}
        deps.update(client_pkg.get('dependencies', {}))
        deps.update(client_pkg.get('devDependencies', {}))

        has_react = 'react' in deps
        has_typescript = 'typescript' in deps or '@types/react' in deps
        has_react_dom = 'react-dom' in deps

        if has_react and has_typescript and has_react_dom:
            print(f"PASS: Component 1 — client/package.json has react, react-dom, typescript deps (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Missing deps: react={has_react}, react-dom={has_react_dom}, typescript={has_typescript}")
    except FileNotFoundError:
        print(f"FAIL: Component 1 — client/package.json not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: client/src/components/TodoList.tsx with add/toggle/delete functionality (0.20 points)
    try:
        todolist_path = os.path.join(BASE, 'client', 'src', 'components', 'TodoList.tsx')
        with open(todolist_path, 'r') as f:
            todolist_content = f.read()

        # Check for key functionality markers
        has_add = bool(re.search(r'(addTodo|add\s*Todo|POST|method.*POST)', todolist_content))
        has_toggle = bool(re.search(r'(toggleTodo|toggle\s*Todo|PUT|method.*PUT|completed)', todolist_content, re.IGNORECASE))
        has_delete = bool(re.search(r'(deleteTodo|delete\s*Todo|DELETE|method.*DELETE)', todolist_content))
        has_fetch = bool(re.search(r'(fetch|axios|GET|useEffect)', todolist_content))

        component_score = 0.0
        if has_add:
            component_score += 0.05
        if has_toggle:
            component_score += 0.05
        if has_delete:
            component_score += 0.05
        if has_fetch:
            component_score += 0.05

        if component_score > 0:
            print(f"PASS: Component 2 — TodoList.tsx: add={has_add}, toggle={has_toggle}, delete={has_delete}, fetch={has_fetch} ({component_score} pts)")
            total_score += component_score
        else:
            print(f"FAIL: Component 2 — TodoList.tsx missing key functionality")
    except FileNotFoundError:
        print(f"FAIL: Component 2 — client/src/components/TodoList.tsx not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: server/package.json with express + TypeScript dependencies (0.15 points)
    try:
        server_pkg_path = os.path.join(BASE, 'server', 'package.json')
        with open(server_pkg_path, 'r') as f:
            server_pkg = json.load(f)

        all_deps = {}
        all_deps.update(server_pkg.get('dependencies', {}))
        all_deps.update(server_pkg.get('devDependencies', {}))

        has_express = 'express' in all_deps
        has_types_express = '@types/express' in all_deps
        has_ts = 'typescript' in all_deps

        if has_express and has_types_express and has_ts:
            print(f"PASS: Component 3 — server/package.json has express, @types/express, typescript (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Missing: express={has_express}, @types/express={has_types_express}, typescript={has_ts}")
    except FileNotFoundError:
        print(f"FAIL: Component 3 — server/package.json not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: server/src/routes/todos.ts with 4 REST endpoints (0.20 points)
    try:
        todos_route_path = os.path.join(BASE, 'server', 'src', 'routes', 'todos.ts')
        with open(todos_route_path, 'r') as f:
            route_content = f.read()

        # Check for each REST endpoint pattern
        has_get = bool(re.search(r'\.(get)\s*\(', route_content))
        has_post = bool(re.search(r'\.(post)\s*\(', route_content))
        has_put = bool(re.search(r'\.(put)\s*\(', route_content))
        has_delete = bool(re.search(r'\.(delete)\s*\(', route_content))

        endpoint_score = 0.0
        if has_get:
            endpoint_score += 0.05
        if has_post:
            endpoint_score += 0.05
        if has_put:
            endpoint_score += 0.05
        if has_delete:
            endpoint_score += 0.05

        if endpoint_score > 0:
            print(f"PASS: Component 4 — todos.ts endpoints: GET={has_get}, POST={has_post}, PUT={has_put}, DELETE={has_delete} ({endpoint_score} pts)")
            total_score += endpoint_score
        else:
            print(f"FAIL: Component 4 — No REST endpoints found in todos.ts")
    except FileNotFoundError:
        print(f"FAIL: Component 4 — server/src/routes/todos.ts not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: todo.code-workspace references both client/ and server/ (0.10 points)
    try:
        ws_path = os.path.join(BASE, 'todo.code-workspace')
        with open(ws_path, 'r') as f:
            ws = json.load(f)

        folders = ws.get('folders', [])
        folder_paths = [f.get('path', '') for f in folders]

        # Accept both relative and absolute paths
        has_client = any('client' in p for p in folder_paths)
        has_server = any('server' in p for p in folder_paths)

        if has_client and has_server:
            print(f"PASS: Component 5 — todo.code-workspace has client and server folders (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Workspace folders: {folder_paths}, need client and server")
    except FileNotFoundError:
        print(f"FAIL: Component 5 — todo.code-workspace not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: client/.vscode/launch.json exists with at least one configuration (0.10 points)
    try:
        client_launch_path = os.path.join(BASE, 'client', '.vscode', 'launch.json')
        with open(client_launch_path, 'r') as f:
            content = f.read()
        # Strip JSONC comments (lines starting with //, not inside strings)
        cleaned = re.sub(r'^\s*//.*$', '', content, flags=re.MULTILINE)
        try:
            client_launch = json.loads(cleaned)
        except json.JSONDecodeError:
            # Fallback: try raw content
            client_launch = json.loads(content)

        configs = client_launch.get('configurations', [])
        if len(configs) > 0:
            print(f"PASS: Component 6 — client/.vscode/launch.json has {len(configs)} configuration(s) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — client/.vscode/launch.json has no configurations")
    except FileNotFoundError:
        print(f"FAIL: Component 6 — client/.vscode/launch.json not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: server/.vscode/launch.json exists with at least one configuration (0.10 points)
    try:
        server_launch_path = os.path.join(BASE, 'server', '.vscode', 'launch.json')
        with open(server_launch_path, 'r') as f:
            content = f.read()
        cleaned = re.sub(r'^\s*//.*$', '', content, flags=re.MULTILINE)
        try:
            server_launch = json.loads(cleaned)
        except json.JSONDecodeError:
            server_launch = json.loads(content)

        configs = server_launch.get('configurations', [])
        if len(configs) > 0:
            print(f"PASS: Component 7 — server/.vscode/launch.json has {len(configs)} configuration(s) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 — server/.vscode/launch.json has no configurations")
    except FileNotFoundError:
        print(f"FAIL: Component 7 — server/.vscode/launch.json not found")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

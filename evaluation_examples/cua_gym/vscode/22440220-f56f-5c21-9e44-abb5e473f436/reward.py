"""
Reward Script: TypeScript monorepo setup with npm workspaces
Task ID: vscode_gf6_061
Domain: vscode
Scoring:
  C1 (0.15) - Root package.json has workspaces: ['packages/*']
  C2 (0.15) - packages/shared/src/types.ts has User, Product, ApiResponse<T> interfaces
  C3 (0.10) - packages/shared/package.json has name @myapp/shared and types entry
  C4 (0.10) - packages/api/package.json has name @myapp/api and depends on @myapp/shared
  C5 (0.10) - packages/web/package.json has name @myapp/web and depends on @myapp/shared + @myapp/api
  C6 (0.10) - packages/api/tsconfig.json has references to ../shared
  C7 (0.10) - Root tsconfig.json has composite:true and references to all 3 packages
  C8 (0.05) - node_modules/@myapp/shared symlink exists (npm workspaces linking)
  C9 (0.10) - .vscode/tasks.json has Build All, Test All, Typecheck tasks
  C10 (0.05) - fullstack.code-workspace references all 3 package folders
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_061'
PROJECT = os.path.join(WORKDIR, 'projects', 'ts-monorepo')


def load_json(path):
    """Load a JSON file, returning None on failure."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"  Could not load {path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Root package.json has workspaces: ['packages/*'] (0.15 points)
    try:
        root_pkg = load_json(os.path.join(PROJECT, 'package.json'))
        if root_pkg and 'workspaces' in root_pkg:
            ws = root_pkg['workspaces']
            if isinstance(ws, list) and 'packages/*' in ws:
                print(f"PASS: C1 — Root package.json has workspaces: {ws} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: C1 — workspaces field present but missing 'packages/*': {ws}")
        else:
            print(f"FAIL: C1 — Root package.json missing 'workspaces' field")
    except Exception as e:
        print(f"ERROR: C1 — {e}")

    # Component 2: packages/shared/src/types.ts has User, Product, ApiResponse<T> interfaces (0.15 points)
    try:
        types_path = os.path.join(PROJECT, 'packages', 'shared', 'src', 'types.ts')
        if os.path.exists(types_path):
            with open(types_path, 'r') as f:
                content = f.read()
            found_interfaces = []
            for iface in ['User', 'Product', 'ApiResponse']:
                # Check for "interface User" or "interface ApiResponse<T>"
                if f'interface {iface}' in content:
                    found_interfaces.append(iface)
            if len(found_interfaces) == 3:
                # Also verify ApiResponse is generic (has <T> or similar generic parameter)
                if 'ApiResponse<' in content:
                    print(f"PASS: C2 — types.ts has all 3 interfaces (User, Product, ApiResponse<T>) (0.15 pts)")
                    total_score += 0.15
                elif len(found_interfaces) == 3:
                    print(f"FAIL: C2 — ApiResponse interface found but not generic (no <T>)")
                    total_score += 0.10  # partial: interfaces exist but generic missing
            else:
                missing = [i for i in ['User', 'Product', 'ApiResponse'] if i not in found_interfaces]
                print(f"FAIL: C2 — Missing interfaces: {missing}")
                # Partial credit: give proportional score
                partial = len(found_interfaces) / 3.0 * 0.15
                if partial > 0:
                    total_score += round(partial, 3)
                    print(f"  Partial credit: {round(partial, 3)} pts for {found_interfaces}")
        else:
            print(f"FAIL: C2 — types.ts not found at {types_path}")
    except Exception as e:
        print(f"ERROR: C2 — {e}")

    # Component 3: packages/shared/package.json has name @myapp/shared and types entry (0.10 points)
    try:
        shared_pkg = load_json(os.path.join(PROJECT, 'packages', 'shared', 'package.json'))
        if shared_pkg:
            name_ok = shared_pkg.get('name') == '@myapp/shared'
            types_ok = 'types' in shared_pkg or 'typings' in shared_pkg
            if name_ok and types_ok:
                print(f"PASS: C3 — shared/package.json name=@myapp/shared, types entry present (0.10 pts)")
                total_score += 0.10
            elif name_ok:
                print(f"FAIL: C3 — name correct but no 'types' entry in shared/package.json")
                total_score += 0.05
            else:
                print(f"FAIL: C3 — shared/package.json name={shared_pkg.get('name')}, expected @myapp/shared")
        else:
            print(f"FAIL: C3 — packages/shared/package.json not found or invalid")
    except Exception as e:
        print(f"ERROR: C3 — {e}")

    # Component 4: packages/api/package.json has name @myapp/api and depends on @myapp/shared (0.10 points)
    try:
        api_pkg = load_json(os.path.join(PROJECT, 'packages', 'api', 'package.json'))
        if api_pkg:
            name_ok = api_pkg.get('name') == '@myapp/api'
            deps = api_pkg.get('dependencies', {})
            dep_ok = '@myapp/shared' in deps
            if name_ok and dep_ok:
                print(f"PASS: C4 — api/package.json name=@myapp/api, depends on @myapp/shared (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: C4 — name_ok={name_ok}, dep_on_shared={dep_ok}")
                if name_ok or dep_ok:
                    total_score += 0.05
        else:
            print(f"FAIL: C4 — packages/api/package.json not found or invalid")
    except Exception as e:
        print(f"ERROR: C4 — {e}")

    # Component 5: packages/web/package.json has name @myapp/web and depends on @myapp/shared + @myapp/api (0.10 points)
    try:
        web_pkg = load_json(os.path.join(PROJECT, 'packages', 'web', 'package.json'))
        if web_pkg:
            name_ok = web_pkg.get('name') == '@myapp/web'
            deps = web_pkg.get('dependencies', {})
            dep_shared = '@myapp/shared' in deps
            dep_api = '@myapp/api' in deps
            if name_ok and dep_shared and dep_api:
                print(f"PASS: C5 — web/package.json name=@myapp/web, depends on shared+api (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: C5 — name_ok={name_ok}, dep_shared={dep_shared}, dep_api={dep_api}")
                if name_ok:
                    total_score += 0.03
                if dep_shared:
                    total_score += 0.03
        else:
            print(f"FAIL: C5 — packages/web/package.json not found or invalid")
    except Exception as e:
        print(f"ERROR: C5 — {e}")

    # Component 6: packages/api/tsconfig.json has references to ../shared (0.10 points)
    try:
        api_tsconfig = load_json(os.path.join(PROJECT, 'packages', 'api', 'tsconfig.json'))
        if api_tsconfig:
            refs = api_tsconfig.get('references', [])
            ref_paths = [r.get('path', '') for r in refs if isinstance(r, dict)]
            if any('../shared' in p for p in ref_paths):
                print(f"PASS: C6 — api/tsconfig.json references ../shared (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: C6 — api/tsconfig.json references={ref_paths}, expected ../shared")
        else:
            print(f"FAIL: C6 — packages/api/tsconfig.json not found or invalid")
    except Exception as e:
        print(f"ERROR: C6 — {e}")

    # Component 7: Root tsconfig.json has composite:true and references to all 3 packages (0.10 points)
    try:
        root_tsconfig = load_json(os.path.join(PROJECT, 'tsconfig.json'))
        if root_tsconfig:
            compiler_opts = root_tsconfig.get('compilerOptions', {})
            composite_ok = compiler_opts.get('composite') is True
            refs = root_tsconfig.get('references', [])
            ref_paths = [r.get('path', '') for r in refs if isinstance(r, dict)]
            has_shared = any('shared' in p for p in ref_paths)
            has_api = any('api' in p for p in ref_paths)
            has_web = any('web' in p for p in ref_paths)
            all_refs = has_shared and has_api and has_web
            if composite_ok and all_refs:
                print(f"PASS: C7 — Root tsconfig.json composite=true, refs to all 3 packages (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: C7 — composite={composite_ok}, shared={has_shared}, api={has_api}, web={has_web}")
                if composite_ok:
                    total_score += 0.03
                if all_refs:
                    total_score += 0.05
        else:
            print(f"FAIL: C7 — Root tsconfig.json not found or invalid")
    except Exception as e:
        print(f"ERROR: C7 — {e}")

    # Component 8: node_modules/@myapp/shared symlink exists (npm workspaces linking) (0.05 points)
    try:
        symlink_path = os.path.join(PROJECT, 'node_modules', '@myapp', 'shared')
        if os.path.exists(symlink_path) and os.path.islink(symlink_path):
            print(f"PASS: C8 — node_modules/@myapp/shared is a symlink (0.05 pts)")
            total_score += 0.05
        elif os.path.exists(symlink_path):
            # exists but not a symlink - could be npm installed differently
            print(f"PASS: C8 — node_modules/@myapp/shared exists (not symlink but linked) (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: C8 — node_modules/@myapp/shared not found")
    except Exception as e:
        print(f"ERROR: C8 — {e}")

    # Component 9: .vscode/tasks.json has Build All, Test All, Typecheck tasks (0.10 points)
    try:
        tasks_config = load_json(os.path.join(PROJECT, '.vscode', 'tasks.json'))
        if tasks_config:
            tasks = tasks_config.get('tasks', [])
            task_labels = [t.get('label', '').lower() for t in tasks]
            has_build = any('build all' in lbl for lbl in task_labels)
            has_test = any('test all' in lbl for lbl in task_labels)
            has_typecheck = any('typecheck' in lbl for lbl in task_labels)
            found = sum([has_build, has_test, has_typecheck])
            if found == 3:
                print(f"PASS: C9 — tasks.json has Build All, Test All, Typecheck (0.10 pts)")
                total_score += 0.10
            else:
                partial = round(found / 3.0 * 0.10, 3)
                print(f"FAIL: C9 — build_all={has_build}, test_all={has_test}, typecheck={has_typecheck}")
                if partial > 0:
                    total_score += partial
                    print(f"  Partial credit: {partial} pts")
        else:
            print(f"FAIL: C9 — .vscode/tasks.json not found or invalid")
    except Exception as e:
        print(f"ERROR: C9 — {e}")

    # Component 10: fullstack.code-workspace references all 3 package folders (0.05 points)
    try:
        ws_path = os.path.join(PROJECT, 'fullstack.code-workspace')
        ws_config = load_json(ws_path)
        if ws_config:
            folders = ws_config.get('folders', [])
            folder_paths = [f.get('path', '') for f in folders if isinstance(f, dict)]
            has_shared = any('shared' in p for p in folder_paths)
            has_api = any('api' in p for p in folder_paths)
            has_web = any('web' in p for p in folder_paths)
            if has_shared and has_api and has_web:
                print(f"PASS: C10 — fullstack.code-workspace references shared, api, web (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: C10 — folders={folder_paths}, shared={has_shared}, api={has_api}, web={has_web}")
        else:
            print(f"FAIL: C10 — fullstack.code-workspace not found or invalid")
    except Exception as e:
        print(f"ERROR: C10 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

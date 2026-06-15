"""
Reward Script: React Dashboard with TypeScript, recharts, axios, custom hook, and VSCode config
Task ID: vscode_gf4_020
Domain: vscode
Scoring:
  Component 1: package.json has recharts + axios dependencies (0.2)
  Component 2: Dashboard.tsx exists with BarChart + useFetch + jsonplaceholder URL (0.3)
  Component 3: useFetch.ts exists returning {data, loading, error} (0.2)
  Component 4: .vscode/settings.json has formatOnSave + Prettier (0.2)
  Component 5: tsconfig.json has strict: true (0.1)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-dashboard')
TASK_ID = 'vscode_gf4_020'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory must exist
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory {PROJECT_DIR} does not exist")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: package.json has recharts and axios as dependencies (0.2 points)
    try:
        pkg_path = os.path.join(PROJECT_DIR, 'package.json')
        if os.path.exists(pkg_path):
            with open(pkg_path, 'r') as f:
                pkg = json.load(f)
            deps = pkg.get('dependencies', {})
            has_recharts = any('recharts' in k for k in deps.keys())
            has_axios = any('axios' in k for k in deps.keys())
            has_typescript = any('typescript' in k for k in deps.keys())
            has_react = any(k == 'react' for k in deps.keys())
            if has_recharts and has_axios:
                print(f"PASS: Component 1 — package.json has recharts ({deps.get('recharts','?')}) and axios ({deps.get('axios','?')}) (0.2 pts)")
                total_score += 0.2
            else:
                missing = []
                if not has_recharts:
                    missing.append('recharts')
                if not has_axios:
                    missing.append('axios')
                print(f"FAIL: Component 1 — package.json missing dependencies: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 1 — package.json not found at {pkg_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Dashboard.tsx exists with BarChart, useFetch hook usage, and jsonplaceholder URL (0.3 points)
    try:
        dashboard_path = os.path.join(PROJECT_DIR, 'src', 'components', 'Dashboard.tsx')
        if os.path.exists(dashboard_path):
            with open(dashboard_path, 'r') as f:
                content = f.read()

            sub_score = 0.0

            # 2a: Imports from recharts (BarChart specifically)
            if 'BarChart' in content and 'recharts' in content:
                sub_score += 0.1
                print("  PASS: Component 2a — Dashboard.tsx imports BarChart from recharts")
            else:
                print(f"  FAIL: Component 2a — Dashboard.tsx missing BarChart/recharts import")

            # 2b: Uses useFetch hook
            if 'useFetch' in content:
                sub_score += 0.1
                print("  PASS: Component 2b — Dashboard.tsx uses useFetch hook")
            else:
                print(f"  FAIL: Component 2b — Dashboard.tsx does not use useFetch hook")

            # 2c: References jsonplaceholder API URL
            if 'jsonplaceholder.typicode.com/posts' in content:
                sub_score += 0.1
                print("  PASS: Component 2c — Dashboard.tsx fetches from jsonplaceholder API")
            else:
                print(f"  FAIL: Component 2c — Dashboard.tsx missing jsonplaceholder URL")

            if sub_score > 0:
                print(f"PASS: Component 2 — Dashboard.tsx ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 — Dashboard.tsx has none of the required elements")
        else:
            print(f"FAIL: Component 2 — Dashboard.tsx not found at {dashboard_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: useFetch.ts exists and returns {data, loading, error} (0.2 points)
    try:
        hook_path = os.path.join(PROJECT_DIR, 'src', 'hooks', 'useFetch.ts')
        if os.path.exists(hook_path):
            with open(hook_path, 'r') as f:
                content = f.read()

            # Check that it exports a function and has data, loading, error state
            has_data = bool(re.search(r'\bdata\b', content))
            has_loading = bool(re.search(r'\bloading\b', content))
            has_error = bool(re.search(r'\berror\b', content))
            has_export = bool(re.search(r'export\s+(function|const|default)', content))
            has_return = bool(re.search(r'return\s*\{.*data.*loading.*error', content, re.DOTALL))

            if has_data and has_loading and has_error and has_export:
                print(f"PASS: Component 3 — useFetch.ts exports hook with data/loading/error state (0.2 pts)")
                total_score += 0.2
            else:
                missing = []
                if not has_data:
                    missing.append('data')
                if not has_loading:
                    missing.append('loading')
                if not has_error:
                    missing.append('error')
                if not has_export:
                    missing.append('export')
                print(f"FAIL: Component 3 — useFetch.ts missing: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 3 — useFetch.ts not found at {hook_path}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: .vscode/settings.json has formatOnSave and Prettier formatter (0.2 points)
    try:
        vscode_settings_path = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
        if os.path.exists(vscode_settings_path):
            with open(vscode_settings_path, 'r') as f:
                raw = f.read()
            # Strip JSONC comments before parsing
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            settings = json.loads(cleaned)

            sub_score = 0.0

            # 4a: formatOnSave is true
            if settings.get('editor.formatOnSave') is True:
                sub_score += 0.1
                print("  PASS: Component 4a — editor.formatOnSave is true")
            else:
                print(f"  FAIL: Component 4a — editor.formatOnSave is {settings.get('editor.formatOnSave', 'not set')}")

            # 4b: Prettier is referenced as formatter
            settings_str = json.dumps(settings).lower()
            if 'prettier' in settings_str:
                sub_score += 0.1
                print("  PASS: Component 4b — Prettier is referenced as formatter")
            else:
                print(f"  FAIL: Component 4b — No Prettier reference found in .vscode/settings.json")

            if sub_score > 0:
                print(f"PASS: Component 4 — .vscode/settings.json ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 4 — .vscode/settings.json missing formatOnSave and Prettier")
        else:
            print(f"FAIL: Component 4 — .vscode/settings.json not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: tsconfig.json has strict: true (0.1 points)
    try:
        tsconfig_path = os.path.join(PROJECT_DIR, 'tsconfig.json')
        if os.path.exists(tsconfig_path):
            with open(tsconfig_path, 'r') as f:
                raw = f.read()
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            tsconfig = json.loads(cleaned)
            compiler_opts = tsconfig.get('compilerOptions', {})
            if compiler_opts.get('strict') is True:
                print(f"PASS: Component 5 — tsconfig.json has strict: true (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 5 — tsconfig.json strict is {compiler_opts.get('strict', 'not set')}")
        else:
            print(f"FAIL: Component 5 — tsconfig.json not found at {tsconfig_path}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

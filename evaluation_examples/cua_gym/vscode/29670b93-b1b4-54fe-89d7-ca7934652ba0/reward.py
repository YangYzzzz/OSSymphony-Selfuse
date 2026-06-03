"""
Reward Script: VSCode React TypeScript Project Setup
Task ID: vscode_gf4_011
Domain: vscode
Scoring:
  Component 1 (0.25): package.json with react, react-dom, typescript deps
  Component 2 (0.25): src/App.tsx exists (TypeScript React component)
  Component 3 (0.25): .vscode/settings.json with tabSize=2, insertSpaces=true
  Component 4 (0.25): .vscode/settings.json with importModuleSpecifier=relative, *.tsx association
"""

import os
import json
import re

WORKDIR = '/home/user/projects/react-app'
TASK_ID = 'vscode_gf4_011'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: package.json exists with react, react-dom, typescript dependencies (0.25 points)
    try:
        pkg_path = os.path.join(WORKDIR, 'package.json')
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)

        deps = pkg.get('dependencies', {})
        has_react = any(k == 'react' for k in deps)
        has_react_dom = any(k == 'react-dom' for k in deps)
        has_typescript = any(k == 'typescript' for k in deps)

        if has_react and has_react_dom and has_typescript:
            print(f"PASS: Component 1 -- package.json has react, react-dom, typescript (0.25 pts)")
            total_score += 0.25
        else:
            missing = []
            if not has_react:
                missing.append('react')
            if not has_react_dom:
                missing.append('react-dom')
            if not has_typescript:
                missing.append('typescript')
            print(f"FAIL: Component 1 -- package.json missing deps: {missing}")
    except FileNotFoundError:
        print(f"FAIL: Component 1 -- package.json not found at {pkg_path}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: src/App.tsx exists (TypeScript React component) (0.25 points)
    try:
        app_tsx_path = os.path.join(WORKDIR, 'src', 'App.tsx')
        if os.path.isfile(app_tsx_path):
            with open(app_tsx_path, 'r') as f:
                content = f.read()
            # Verify it has some React content (import or JSX-like patterns)
            if len(content) > 10:
                print(f"PASS: Component 2 -- src/App.tsx exists with content ({len(content)} bytes) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- src/App.tsx exists but is nearly empty ({len(content)} bytes)")
        else:
            print(f"FAIL: Component 2 -- src/App.tsx not found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: .vscode/settings.json with tabSize=2 and insertSpaces=true (0.25 points)
    try:
        settings_path = os.path.join(WORKDIR, '.vscode', 'settings.json')
        with open(settings_path, 'r') as f:
            raw = f.read()
        # Strip JSONC comments before parsing
        cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
        settings = json.loads(cleaned)

        tab_size_ok = settings.get('editor.tabSize') == 2
        insert_spaces_ok = settings.get('editor.insertSpaces') is True

        if tab_size_ok and insert_spaces_ok:
            print(f"PASS: Component 3 -- editor.tabSize=2, editor.insertSpaces=true (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- tabSize={settings.get('editor.tabSize')}, insertSpaces={settings.get('editor.insertSpaces')}")
    except FileNotFoundError:
        print(f"FAIL: Component 3 -- .vscode/settings.json not found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: .vscode/settings.json with importModuleSpecifier=relative and *.tsx=typescriptreact (0.25 points)
    try:
        settings_path = os.path.join(WORKDIR, '.vscode', 'settings.json')
        with open(settings_path, 'r') as f:
            raw = f.read()
        cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
        settings = json.loads(cleaned)

        import_spec_ok = settings.get('typescript.preferences.importModuleSpecifier') == 'relative'
        file_assoc = settings.get('files.associations', {})
        tsx_assoc_ok = file_assoc.get('*.tsx') == 'typescriptreact'

        if import_spec_ok and tsx_assoc_ok:
            print(f"PASS: Component 4 -- importModuleSpecifier=relative, *.tsx=typescriptreact (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 -- importModuleSpecifier={settings.get('typescript.preferences.importModuleSpecifier')}, *.tsx={file_assoc.get('*.tsx')}")
    except FileNotFoundError:
        print(f"FAIL: Component 4 -- .vscode/settings.json not found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

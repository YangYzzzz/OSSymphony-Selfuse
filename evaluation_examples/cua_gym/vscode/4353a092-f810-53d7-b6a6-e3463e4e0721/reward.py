"""
Reward Script: Full-stack workspace configuration for VSCode
Task ID: vscode_wf_035
Domain: vscode
Scoring:
  C1 (0.20) - Workspace file exists with both folders
  C2 (0.20) - Frontend folder settings: ESLint + Prettier + tabSize 2
  C3 (0.20) - Backend folder settings: pylint + Black + tabSize 4
  C4 (0.20) - Launch configurations for backend (debugpy) and frontend (chrome)
  C5 (0.20) - Compound launch configuration combining both
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_035'

WORKSPACE_PATH = os.path.join(WORKDIR, 'fullstack.code-workspace')

# Possible locations for launch config
LAUNCH_PATHS = [
    os.path.join(WORKDIR, '.vscode', 'launch.json'),
]


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) safely."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip JSONC comments carefully (avoid stripping // inside strings)
    # Strategy: try parsing directly first, fall back to comment stripping
    try:
        return json.loads(content, strict=False)
    except json.JSONDecodeError:
        pass
    # Remove single-line comments only outside of strings
    # Simple approach: remove lines that are only comments
    lines = content.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('//'):
            continue  # Skip comment-only lines
        cleaned.append(line)
    content = '\n'.join(cleaned)
    # Strip block comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content, strict=False)


def _is_subset(expected, actual):
    """Check if expected is a subset of actual (recursive dict matching)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def find_launch_config():
    """Find launch config either in workspace file or .vscode/launch.json."""
    # First check workspace file for embedded launch config
    if os.path.exists(WORKSPACE_PATH):
        try:
            ws = load_jsonc(WORKSPACE_PATH)
            if 'launch' in ws and 'configurations' in ws['launch']:
                return ws['launch']
        except Exception:
            pass

    # Then check standalone launch.json
    for path in LAUNCH_PATHS:
        if os.path.exists(path):
            try:
                return load_jsonc(path)
            except Exception:
                continue
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Workspace file exists with both folders (0.20 points)
    try:
        if not os.path.exists(WORKSPACE_PATH):
            print("FAIL: Component 1 - fullstack.code-workspace does not exist")
        else:
            ws = load_jsonc(WORKSPACE_PATH)
            folders = ws.get('folders', [])
            folder_paths = [f.get('path', '') for f in folders]

            has_frontend = any('/home/user/frontend' in p or 'frontend' in p for p in folder_paths)
            has_backend = any('/home/user/backend' in p or 'backend' in p for p in folder_paths)

            if has_frontend and has_backend:
                print(f"PASS: Component 1 - Workspace has both folders: {folder_paths} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 - Missing folders. frontend={has_frontend}, backend={has_backend}. Found: {folder_paths}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Frontend folder settings (ESLint + Prettier + tabSize 2) (0.20 points)
    try:
        frontend_settings_path = os.path.join(WORKDIR, 'frontend', '.vscode', 'settings.json')

        # Also check workspace-level per-folder settings
        frontend_settings = None

        if os.path.exists(frontend_settings_path):
            frontend_settings = load_jsonc(frontend_settings_path)
        elif os.path.exists(WORKSPACE_PATH):
            # Check workspace file for folder-level settings
            ws = load_jsonc(WORKSPACE_PATH)
            for folder in ws.get('folders', []):
                fp = folder.get('path', '')
                if 'frontend' in fp:
                    frontend_settings = folder.get('settings', {})
                    break

        if frontend_settings is None:
            print("FAIL: Component 2 - No frontend settings found")
        else:
            sub_score = 0.0
            # Check tabSize == 2
            if frontend_settings.get('editor.tabSize') == 2:
                sub_score += 0.07
            else:
                print(f"  DETAIL: Frontend tabSize expected 2, found {frontend_settings.get('editor.tabSize')}")

            # Check Prettier configured as formatter
            prettier_found = False
            default_fmt = frontend_settings.get('editor.defaultFormatter', '')
            if 'prettier' in str(default_fmt).lower():
                prettier_found = True
            # Also check language-specific formatters
            for key in ['[typescript]', '[typescriptreact]', '[javascript]', '[javascriptreact]']:
                lang_settings = frontend_settings.get(key, {})
                if 'prettier' in str(lang_settings.get('editor.defaultFormatter', '')).lower():
                    prettier_found = True
                    break
            if prettier_found:
                sub_score += 0.07
            else:
                print(f"  DETAIL: Prettier not configured for frontend")

            # Check ESLint enabled
            eslint_found = False
            if frontend_settings.get('eslint.enable') is True:
                eslint_found = True
            if frontend_settings.get('eslint.validate'):
                eslint_found = True
            if eslint_found:
                sub_score += 0.06
            else:
                print(f"  DETAIL: ESLint not configured for frontend")

            if sub_score > 0:
                print(f"PASS: Component 2 - Frontend settings verified ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print("FAIL: Component 2 - Frontend settings missing all required configs")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Backend folder settings (pylint + Black + tabSize 4) (0.20 points)
    try:
        backend_settings_path = os.path.join(WORKDIR, 'backend', '.vscode', 'settings.json')

        backend_settings = None

        if os.path.exists(backend_settings_path):
            backend_settings = load_jsonc(backend_settings_path)
        elif os.path.exists(WORKSPACE_PATH):
            ws = load_jsonc(WORKSPACE_PATH)
            for folder in ws.get('folders', []):
                fp = folder.get('path', '')
                if 'backend' in fp:
                    backend_settings = folder.get('settings', {})
                    break

        if backend_settings is None:
            print("FAIL: Component 3 - No backend settings found")
        else:
            sub_score = 0.0
            # Check tabSize == 4
            if backend_settings.get('editor.tabSize') == 4:
                sub_score += 0.07
            else:
                print(f"  DETAIL: Backend tabSize expected 4, found {backend_settings.get('editor.tabSize')}")

            # Check Black configured as formatter
            black_found = False
            default_fmt = str(backend_settings.get('editor.defaultFormatter', '')).lower()
            if 'black' in default_fmt:
                black_found = True
            formatting_provider = str(backend_settings.get('python.formatting.provider', '')).lower()
            if 'black' in formatting_provider:
                black_found = True
            python_settings = backend_settings.get('[python]', {})
            if 'black' in str(python_settings.get('editor.defaultFormatter', '')).lower():
                black_found = True
            if black_found:
                sub_score += 0.07
            else:
                print(f"  DETAIL: Black not configured for backend")

            # Check pylint enabled
            pylint_found = False
            if backend_settings.get('python.linting.pylintEnabled') is True:
                pylint_found = True
            if backend_settings.get('python.linting.enabled') is True:
                pylint_found = True
            pylint_args = backend_settings.get('python.linting.pylintArgs')
            if pylint_args is not None:
                pylint_found = True
            if pylint_found:
                sub_score += 0.06
            else:
                print(f"  DETAIL: pylint not configured for backend")

            if sub_score > 0:
                print(f"PASS: Component 3 - Backend settings verified ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print("FAIL: Component 3 - Backend settings missing all required configs")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Launch configurations for backend (debugpy) and frontend (chrome) (0.20 points)
    try:
        launch = find_launch_config()
        if launch is None:
            print("FAIL: Component 4 - No launch configuration found")
        else:
            configs = launch.get('configurations', [])
            sub_score = 0.0

            # Check for backend debugpy launch config
            backend_launch_found = False
            for cfg in configs:
                cfg_type = str(cfg.get('type', '')).lower()
                cfg_name = str(cfg.get('name', '')).lower()
                cfg_module = str(cfg.get('module', '')).lower()
                # debugpy type or python type with uvicorn/main.py
                if cfg_type in ('debugpy', 'python') or 'backend' in cfg_name or 'fastapi' in cfg_name:
                    if cfg_type in ('debugpy', 'python') or 'uvicorn' in cfg_module:
                        backend_launch_found = True
                        break
            if backend_launch_found:
                sub_score += 0.10
                print(f"  DETAIL: Backend launch config found (debugpy/python)")
            else:
                print(f"  DETAIL: No backend debugpy/python launch config found")

            # Check for frontend chrome launch config
            frontend_launch_found = False
            for cfg in configs:
                cfg_type = str(cfg.get('type', '')).lower()
                cfg_name = str(cfg.get('name', '')).lower()
                if 'chrome' in cfg_type or ('chrome' in cfg_name and cfg.get('request') in ('launch', 'attach')):
                    frontend_launch_found = True
                    break
            if frontend_launch_found:
                sub_score += 0.10
                print(f"  DETAIL: Frontend chrome launch config found")
            else:
                print(f"  DETAIL: No frontend chrome launch config found")

            if sub_score > 0:
                print(f"PASS: Component 4 - Launch configs verified ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print("FAIL: Component 4 - No valid launch configurations found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Compound launch configuration (0.20 points)
    try:
        launch = find_launch_config()
        if launch is None:
            print("FAIL: Component 5 - No launch configuration found")
        else:
            compounds = launch.get('compounds', [])
            if not compounds:
                print("FAIL: Component 5 - No compound launch configurations found")
            else:
                compound_valid = False
                for compound in compounds:
                    compound_configs = compound.get('configurations', [])
                    # Normalize to strings (could be dicts with name key)
                    config_names = []
                    for c in compound_configs:
                        if isinstance(c, str):
                            config_names.append(c.lower())
                        elif isinstance(c, dict):
                            config_names.append(str(c.get('name', '')).lower())

                    # Check it references at least 2 configs (backend + frontend)
                    has_backend_ref = any('backend' in n or 'fastapi' in n or 'python' in n for n in config_names)
                    has_frontend_ref = any('frontend' in n or 'react' in n or 'chrome' in n for n in config_names)

                    if has_backend_ref and has_frontend_ref and len(compound_configs) >= 2:
                        compound_valid = True
                        print(f"  DETAIL: Compound '{compound.get('name', '')}' references both backend and frontend")
                        break

                if compound_valid:
                    print(f"PASS: Component 5 - Compound launch config verified (0.20 pts)")
                    total_score += 0.20
                else:
                    print("FAIL: Component 5 - Compound config does not reference both backend and frontend")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

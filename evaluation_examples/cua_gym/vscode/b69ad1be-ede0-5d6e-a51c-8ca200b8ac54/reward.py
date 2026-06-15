"""
Reward Script: Vite + React + TypeScript project with path aliases
Task ID: vscode_web_093
Domain: vscode
Scoring:
  - Component 1 (0.20): package.json exists with React+TS Vite template deps
  - Component 2 (0.20): node_modules directory exists (deps installed)
  - Component 3 (0.30): vite.config.ts has resolve.alias '@' -> './src'
  - Component 4 (0.30): tsconfig.json has paths '@/*' -> ['./src/*'] with baseUrl '.'
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'new-app')
TASK_ID = 'vscode_web_093'


def strip_jsonc_comments(text):
    """Strip // and /* */ comments from JSONC text for parsing."""
    # Remove single-line comments
    text = re.sub(r'//.*?$', '', text, flags=re.MULTILINE)
    # Remove multi-line comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    return text


def load_json_or_jsonc(path):
    """Load a JSON or JSONC file, stripping comments if needed."""
    with open(path, 'r') as f:
        content = f.read()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        cleaned = strip_jsonc_comments(content)
        return json.loads(cleaned)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: package.json with React+TypeScript Vite template (0.20 points)
    # Checks that Vite scaffolded a React+TS project with correct dependencies
    try:
        pkg_path = os.path.join(PROJECT_DIR, 'package.json')
        if not os.path.exists(pkg_path):
            print(f"FAIL: Component 1 -- package.json not found at {pkg_path}")
        else:
            pkg = load_json_or_jsonc(pkg_path)
            deps = pkg.get('dependencies', {})
            dev_deps = pkg.get('devDependencies', {})
            has_react = 'react' in deps
            has_react_dom = 'react-dom' in deps
            has_vite = 'vite' in dev_deps
            has_typescript = 'typescript' in dev_deps

            if has_react and has_react_dom and has_vite and has_typescript:
                print(f"PASS: Component 1 -- package.json has react, react-dom, vite, typescript (0.20 pts)")
                total_score += 0.20
            else:
                missing = []
                if not has_react: missing.append('react')
                if not has_react_dom: missing.append('react-dom')
                if not has_vite: missing.append('vite')
                if not has_typescript: missing.append('typescript')
                print(f"FAIL: Component 1 -- package.json missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: node_modules exists (dependencies installed) (0.20 points)
    # The task requires running npm install; node_modules must be present and non-empty
    try:
        nm_path = os.path.join(PROJECT_DIR, 'node_modules')
        if os.path.isdir(nm_path):
            entries = os.listdir(nm_path)
            # Must have a reasonable number of packages (Vite+React template has 100+)
            if len(entries) >= 10:
                print(f"PASS: Component 2 -- node_modules exists with {len(entries)} entries (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 -- node_modules has only {len(entries)} entries, expected 10+")
        else:
            print(f"FAIL: Component 2 -- node_modules directory not found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: vite.config.ts has resolve.alias '@' -> './src' (0.30 points)
    # The task requires configuring path aliases in Vite's config
    try:
        vite_config_path = os.path.join(PROJECT_DIR, 'vite.config.ts')
        if not os.path.exists(vite_config_path):
            print(f"FAIL: Component 3 -- vite.config.ts not found")
        else:
            with open(vite_config_path, 'r') as f:
                vite_content = f.read()

            # Check for resolve.alias with '@' mapping
            # The config should contain resolve: { alias: { '@': ... } }
            has_resolve_alias = 'resolve' in vite_content and 'alias' in vite_content
            has_at_alias = bool(re.search(r"""['"]@['"]""", vite_content))
            has_src_ref = bool(re.search(r"""['"]\.?/?src['"]""", vite_content)) or 'src' in vite_content

            if has_resolve_alias and has_at_alias and has_src_ref:
                print(f"PASS: Component 3 -- vite.config.ts has resolve.alias '@' -> src (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 -- vite.config.ts missing alias config "
                      f"(resolve/alias={has_resolve_alias}, @={has_at_alias}, src={has_src_ref})")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: tsconfig.json has paths '@/*' -> ['./src/*'] with baseUrl '.' (0.30 points)
    # The task requires configuring TS path aliases to match Vite's alias
    try:
        # Check both tsconfig.json and tsconfig.app.json since paths can be in either
        tsconfig_path = os.path.join(PROJECT_DIR, 'tsconfig.json')
        tsconfig_app_path = os.path.join(PROJECT_DIR, 'tsconfig.app.json')

        baseurl_match = False
        paths_match = False

        for cfg_path in [tsconfig_path, tsconfig_app_path]:
            if not os.path.exists(cfg_path):
                continue
            try:
                cfg = load_json_or_jsonc(cfg_path)
                compiler_opts = cfg.get('compilerOptions', {})

                # Check baseUrl
                baseurl_match = baseurl_match or (compiler_opts.get('baseUrl') == '.')

                # Check paths
                paths = compiler_opts.get('paths', {})
                at_paths = paths.get('@/*', [])
                paths_match = paths_match or (isinstance(at_paths, list) and './src/*' in at_paths)
            except Exception:
                continue

        if baseurl_match and paths_match:
            print(f"PASS: Component 4 -- tsconfig has baseUrl='.' and paths '@/*' -> ['./src/*'] (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 4 -- tsconfig missing config "
                  f"(baseUrl={baseurl_match}, paths={paths_match})")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(PROJECT_DIR):
    print(f"Project directory not found: {PROJECT_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()

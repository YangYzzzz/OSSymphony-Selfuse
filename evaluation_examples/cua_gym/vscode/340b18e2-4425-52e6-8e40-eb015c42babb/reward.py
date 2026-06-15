"""
Reward Script: TypeScript monorepo with workspaces setup
Task ID: vscode_gf3_092
Domain: vscode
Scoring:
  C1 (0.15) - Root package.json with workspaces: ["packages/*"]
  C2 (0.15) - packages/core/package.json with @myorg/core, main, types
  C3 (0.15) - packages/api/package.json with @myorg/core dependency
  C4 (0.20) - Root tsconfig.json with project references to core and api
  C5 (0.20) - .vscode/settings.json with TS SDK path setting
  C6 (0.15) - Package tsconfigs: composite + api references core
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_092'
BASE = os.path.join(WORKDIR, 'projects', 'ts-monorepo')


def load_json(path):
    """Load a JSON file, stripping // comments (JSONC support)."""
    import re
    with open(path, 'r') as f:
        content = f.read()
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: base directory must exist
    if not os.path.isdir(BASE):
        print(f"CRITICAL: Base directory {BASE} does not exist")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Root package.json with workspaces (0.15 points)
    try:
        root_pkg_path = os.path.join(BASE, 'package.json')
        root_pkg = load_json(root_pkg_path)
        workspaces = root_pkg.get('workspaces', [])
        if isinstance(workspaces, list) and 'packages/*' in workspaces:
            print(f"PASS: Component 1 — Root package.json has workspaces: {workspaces} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected workspaces containing 'packages/*', found: {workspaces}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: packages/core/package.json (0.15 points)
    try:
        core_pkg_path = os.path.join(BASE, 'packages', 'core', 'package.json')
        core_pkg = load_json(core_pkg_path)
        checks = 0
        total_checks = 3

        name = core_pkg.get('name', '')
        if name == '@myorg/core':
            checks += 1
        else:
            print(f"  DETAIL: core name is '{name}', expected '@myorg/core'")

        main = core_pkg.get('main', '')
        if './dist/index.js' in main or 'dist/index.js' in main:
            checks += 1
        else:
            print(f"  DETAIL: core main is '{main}', expected './dist/index.js'")

        types = core_pkg.get('types', core_pkg.get('typings', ''))
        if './dist/index.d.ts' in types or 'dist/index.d.ts' in types:
            checks += 1
        else:
            print(f"  DETAIL: core types is '{types}', expected './dist/index.d.ts'")

        if checks == total_checks:
            print(f"PASS: Component 2 — core/package.json correct: name={name}, main={main}, types={types} (0.15 pts)")
            total_score += 0.15
        elif checks > 0:
            partial = round(0.15 * checks / total_checks, 3)
            print(f"PARTIAL: Component 2 — {checks}/{total_checks} checks passed ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — core/package.json missing all required fields")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: packages/api/package.json with @myorg/core dependency (0.15 points)
    try:
        api_pkg_path = os.path.join(BASE, 'packages', 'api', 'package.json')
        api_pkg = load_json(api_pkg_path)
        deps = api_pkg.get('dependencies', {})
        dev_deps = api_pkg.get('devDependencies', {})
        all_deps = {**deps, **dev_deps}

        if '@myorg/core' in all_deps:
            print(f"PASS: Component 3 — api/package.json has @myorg/core dependency: {all_deps.get('@myorg/core', '')} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — api/package.json missing @myorg/core dependency. deps={deps}, devDeps={dev_deps}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Root tsconfig.json with project references (0.20 points)
    try:
        root_tsconfig_path = os.path.join(BASE, 'tsconfig.json')
        root_tsconfig = load_json(root_tsconfig_path)
        refs = root_tsconfig.get('references', [])
        ref_paths = [r.get('path', '') for r in refs]

        has_core_ref = any('core' in p for p in ref_paths)
        has_api_ref = any('api' in p for p in ref_paths)

        if has_core_ref and has_api_ref:
            print(f"PASS: Component 4 — Root tsconfig.json references both packages: {ref_paths} (0.20 pts)")
            total_score += 0.20
        elif has_core_ref or has_api_ref:
            print(f"PARTIAL: Component 4 — Only one reference found: {ref_paths} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — Root tsconfig.json missing project references. Found: {refs}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: .vscode/settings.json with TS SDK path (0.20 points)
    try:
        vscode_settings_path = os.path.join(BASE, '.vscode', 'settings.json')
        vscode_settings = load_json(vscode_settings_path)

        sub_score = 0.0
        # Check typescript.tsdk is set to workspace node_modules
        tsdk = vscode_settings.get('typescript.tsdk', '')
        if tsdk and 'node_modules' in tsdk and 'typescript' in tsdk:
            print(f"  DETAIL: typescript.tsdk = '{tsdk}' — correct")
            sub_score += 0.12
        else:
            print(f"  DETAIL: typescript.tsdk = '{tsdk}' — expected path containing node_modules/typescript")

        # Check for project references enablement (enablePromptUseWorkspaceTsdk or similar)
        prompt_tsdk = vscode_settings.get('typescript.enablePromptUseWorkspaceTsdk', None)
        refs_lens = vscode_settings.get('typescript.referencesCodeLens.enabled', None)
        impl_lens = vscode_settings.get('typescript.implementationsCodeLens.enabled', None)
        # Any of these being set counts as "enables project references" support
        if prompt_tsdk is True or refs_lens is True or impl_lens is True:
            print(f"  DETAIL: Project reference settings found — correct")
            sub_score += 0.08
        else:
            print(f"  DETAIL: No project reference enabling settings found")

        if sub_score > 0:
            print(f"PASS: Component 5 — .vscode/settings.json ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 5 — .vscode/settings.json missing TS SDK and project reference settings")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Package tsconfigs with composite + api references core (0.15 points)
    try:
        sub_score = 0.0

        # Core tsconfig must have composite: true
        core_tsconfig_path = os.path.join(BASE, 'packages', 'core', 'tsconfig.json')
        core_tsconfig = load_json(core_tsconfig_path)
        core_compiler = core_tsconfig.get('compilerOptions', {})
        if core_compiler.get('composite') is True:
            print(f"  DETAIL: core/tsconfig.json has composite: true")
            sub_score += 0.05
        else:
            print(f"  DETAIL: core/tsconfig.json missing composite: true")

        # Api tsconfig must have composite: true
        api_tsconfig_path = os.path.join(BASE, 'packages', 'api', 'tsconfig.json')
        api_tsconfig = load_json(api_tsconfig_path)
        api_compiler = api_tsconfig.get('compilerOptions', {})
        if api_compiler.get('composite') is True:
            print(f"  DETAIL: api/tsconfig.json has composite: true")
            sub_score += 0.05
        else:
            print(f"  DETAIL: api/tsconfig.json missing composite: true")

        # Api tsconfig must reference core
        api_refs = api_tsconfig.get('references', [])
        api_ref_paths = [r.get('path', '') for r in api_refs]
        if any('core' in p for p in api_ref_paths):
            print(f"  DETAIL: api/tsconfig.json references core: {api_ref_paths}")
            sub_score += 0.05
        else:
            print(f"  DETAIL: api/tsconfig.json missing reference to core. refs={api_refs}")

        if sub_score > 0:
            print(f"PASS: Component 6 — Package tsconfigs ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 6 — Package tsconfigs missing required settings")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

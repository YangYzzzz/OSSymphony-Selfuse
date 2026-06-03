"""
Reward Script: Configure advanced TypeScript settings and project references in VSCode
Task ID: vscode_gf2_044
Domain: vscode
Scoring:
  Component 1 (0.4): .vscode/settings.json has all 4 TypeScript settings
  Component 2 (0.3): tsconfig.base.json exists with strict settings
  Component 3 (0.3): tsconfig.json extends base with composite and references
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'ts-compiler')


def load_jsonc(path):
    """Load a JSON or JSONC file, stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---------------------------------------------------------------
    # Component 1: .vscode/settings.json has all 4 TypeScript settings (0.4 points)
    # These settings do NOT exist in initial_env (no .vscode dir at all)
    # ---------------------------------------------------------------
    settings_path = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
    try:
        if not os.path.exists(settings_path):
            print(f"FAIL: Component 1 — {settings_path} does not exist")
        else:
            settings = load_jsonc(settings_path)
            checks_passed = 0
            total_checks = 4

            # Check 1a: typescript.tsserver.maxTsServerMemory == 4096
            val = settings.get('typescript.tsserver.maxTsServerMemory')
            if val == 4096:
                checks_passed += 1
                print(f"PASS: 1a — maxTsServerMemory = {val}")
            else:
                print(f"FAIL: 1a — maxTsServerMemory expected 4096, found {val}")

            # Check 1b: typescript.preferences.includePackageJsonAutoImports == "on"
            val = settings.get('typescript.preferences.includePackageJsonAutoImports')
            if val == 'on':
                checks_passed += 1
                print(f"PASS: 1b — includePackageJsonAutoImports = '{val}'")
            else:
                print(f"FAIL: 1b — includePackageJsonAutoImports expected 'on', found '{val}'")

            # Check 1c: typescript.suggest.autoImports == true
            val = settings.get('typescript.suggest.autoImports')
            if val is True:
                checks_passed += 1
                print(f"PASS: 1c — suggest.autoImports = {val}")
            else:
                print(f"FAIL: 1c — suggest.autoImports expected True, found {val}")

            # Check 1d: typescript.inlayHints.parameterNames.enabled == "literals"
            val = settings.get('typescript.inlayHints.parameterNames.enabled')
            if val == 'literals':
                checks_passed += 1
                print(f"PASS: 1d — parameterNames.enabled = '{val}'")
            else:
                print(f"FAIL: 1d — parameterNames.enabled expected 'literals', found '{val}'")

            if checks_passed == total_checks:
                total_score += 0.4
                print(f"PASS: Component 1 — all 4 settings correct (0.4 pts)")
            elif checks_passed > 0:
                partial = 0.4 * (checks_passed / total_checks)
                total_score += partial
                print(f"PARTIAL: Component 1 — {checks_passed}/{total_checks} settings correct ({partial:.2f} pts)")
            else:
                print(f"FAIL: Component 1 — no settings correct")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Component 2: tsconfig.base.json exists with strict settings (0.3 points)
    # This file does NOT exist in initial_env
    # ---------------------------------------------------------------
    base_config_path = os.path.join(PROJECT_DIR, 'tsconfig.base.json')
    try:
        if not os.path.exists(base_config_path):
            print(f"FAIL: Component 2 — tsconfig.base.json does not exist")
        else:
            base_config = load_jsonc(base_config_path)
            compiler_opts = base_config.get('compilerOptions', {})

            checks_passed = 0
            total_checks = 3

            # Check 2a: strict mode is enabled
            if compiler_opts.get('strict') is True:
                checks_passed += 1
                print(f"PASS: 2a — strict = true")
            else:
                print(f"FAIL: 2a — strict expected true, found {compiler_opts.get('strict')}")

            # Check 2b: has additional strict sub-options (at least 2 of the common ones)
            strict_keys = [
                'strictNullChecks', 'strictFunctionTypes', 'strictBindCallApply',
                'strictPropertyInitialization', 'noImplicitAny', 'noImplicitReturns',
                'noImplicitThis'
            ]
            strict_count = sum(1 for k in strict_keys if compiler_opts.get(k) is True)
            if strict_count >= 2:
                checks_passed += 1
                print(f"PASS: 2b — {strict_count} additional strict options enabled")
            else:
                print(f"FAIL: 2b — expected >= 2 strict sub-options, found {strict_count}")

            # Check 2c: has declaration/sourceMap support (build infrastructure)
            has_declaration = compiler_opts.get('declaration') is True
            has_sourcemap = compiler_opts.get('sourceMap') is True
            if has_declaration or has_sourcemap:
                checks_passed += 1
                print(f"PASS: 2c — declaration={has_declaration}, sourceMap={has_sourcemap}")
            else:
                print(f"FAIL: 2c — expected declaration or sourceMap to be true")

            if checks_passed == total_checks:
                total_score += 0.3
                print(f"PASS: Component 2 — tsconfig.base.json correctly configured (0.3 pts)")
            elif checks_passed > 0:
                partial = 0.3 * (checks_passed / total_checks)
                total_score += partial
                print(f"PARTIAL: Component 2 — {checks_passed}/{total_checks} checks ({partial:.2f} pts)")
            else:
                print(f"FAIL: Component 2 — tsconfig.base.json missing required settings")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: tsconfig.json extends base with composite and references (0.3 points)
    # In initial_env, tsconfig.json exists but does NOT have extends, composite, or references
    # ---------------------------------------------------------------
    tsconfig_path = os.path.join(PROJECT_DIR, 'tsconfig.json')
    try:
        if not os.path.exists(tsconfig_path):
            print(f"FAIL: Component 3 — tsconfig.json does not exist")
        else:
            tsconfig = load_jsonc(tsconfig_path)
            compiler_opts = tsconfig.get('compilerOptions', {})

            checks_passed = 0
            total_checks = 3

            # Check 3a: extends tsconfig.base.json
            extends_val = tsconfig.get('extends', '')
            if 'tsconfig.base' in str(extends_val):
                checks_passed += 1
                print(f"PASS: 3a — extends = '{extends_val}'")
            else:
                print(f"FAIL: 3a — extends expected to reference tsconfig.base.json, found '{extends_val}'")

            # Check 3b: composite is true (for project references)
            if compiler_opts.get('composite') is True:
                checks_passed += 1
                print(f"PASS: 3b — composite = true")
            else:
                print(f"FAIL: 3b — composite expected true, found {compiler_opts.get('composite')}")

            # Check 3c: references key exists (array)
            if 'references' in tsconfig and isinstance(tsconfig['references'], list):
                checks_passed += 1
                print(f"PASS: 3c — references array present (length={len(tsconfig['references'])})")
            else:
                print(f"FAIL: 3c — references array expected, found {tsconfig.get('references', 'MISSING')}")

            if checks_passed == total_checks:
                total_score += 0.3
                print(f"PASS: Component 3 — tsconfig.json correctly configured (0.3 pts)")
            elif checks_passed > 0:
                partial = 0.3 * (checks_passed / total_checks)
                total_score += partial
                print(f"PARTIAL: Component 3 — {checks_passed}/{total_checks} checks ({partial:.2f} pts)")
            else:
                print(f"FAIL: Component 3 — tsconfig.json missing task-required settings")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Configure absolute imports with '@/' alias in Next.js project
Task ID: vscode_gf5_021
Domain: vscode
Scoring:
  - Component 1 (0.30): jsconfig.json has baseUrl='.' and paths={'@/*': ['./src/*']}
  - Component 2 (0.25): dashboard/analytics/index.js uses @/ imports, no deep relative imports
  - Component 3 (0.25): settings/profile/edit.js uses @/ imports, no deep relative imports
  - Component 4 (0.20): products/inventory/overview.js uses @/ imports, no deep relative imports
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_021'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'next-app')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: jsconfig.json has baseUrl and paths configured (0.30 points)
    try:
        jsconfig_path = os.path.join(PROJECT_DIR, 'jsconfig.json')
        with open(jsconfig_path, 'r') as f:
            content = f.read()
        # Try direct JSON parse first; fall back to JSONC stripping only if needed
        try:
            jsconfig = json.loads(content)
        except json.JSONDecodeError:
            # Strip single-line comments outside strings (best effort)
            lines = content.split('\n')
            stripped_lines = []
            for line in lines:
                # Remove trailing // comments (naive, but works for simple JSONC)
                idx = line.find('//')
                if idx >= 0:
                    # Only strip if not inside a string (count preceding quotes)
                    before = line[:idx]
                    if before.count('"') % 2 == 0:
                        line = before
                stripped_lines.append(line)
            jsconfig = json.loads('\n'.join(stripped_lines))

        compiler_opts = jsconfig.get('compilerOptions', {})
        base_url = compiler_opts.get('baseUrl', None)
        paths = compiler_opts.get('paths', {})

        has_base_url = base_url == '.'
        # Check that @/* maps to ./src/* (allow minor variations)
        has_alias = False
        alias_value = paths.get('@/*', None)
        if alias_value is not None:
            # Could be a list like ['./src/*'] or a string
            if isinstance(alias_value, list):
                for v in alias_value:
                    if v in ('./src/*', 'src/*'):
                        has_alias = True
                        break
            elif isinstance(alias_value, str) and alias_value in ('./src/*', 'src/*'):
                has_alias = True

        if has_base_url and has_alias:
            print(f"PASS: Component 1 — jsconfig.json has baseUrl='.' and paths @/*->./src/* (0.30 pts)")
            total_score += 0.30
        elif has_base_url or has_alias:
            # Partial: one of the two is correct
            print(f"PARTIAL: Component 1 — baseUrl={base_url}, paths={paths} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — baseUrl={base_url}, paths={paths}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Helper to check a JS file for @/ imports and absence of deep relative imports
    def check_file_imports(file_rel_path, component_name, points):
        """
        Check that a file uses @/ imports and has no deep relative imports (../../).
        Returns points earned.
        """
        nonlocal total_score
        try:
            file_path = os.path.join(PROJECT_DIR, file_rel_path)
            with open(file_path, 'r') as f:
                content = f.read()

            # Check for @/ imports (at least one must exist)
            at_imports = re.findall(r"from\s+['\"]@/", content)
            has_at_imports = len(at_imports) > 0

            # Check for deep relative imports (../../ or deeper)
            deep_relative = re.findall(r"from\s+['\"]\.\.\/\.\.\/(components|utils)", content)
            has_deep_relative = len(deep_relative) > 0

            if has_at_imports and not has_deep_relative:
                print(f"PASS: {component_name} — {len(at_imports)} @/ imports, no deep relative imports ({points} pts)")
                total_score += points
            elif has_at_imports and has_deep_relative:
                # Partial: has some @/ imports but still has relative ones
                partial = points * 0.5
                print(f"PARTIAL: {component_name} — has @/ imports but also {len(deep_relative)} deep relative imports ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: {component_name} — @/ imports: {len(at_imports)}, deep relative: {len(deep_relative)}")
        except Exception as e:
            print(f"ERROR: {component_name} — {e}")

    # Component 2: dashboard/analytics/index.js (0.25 points)
    check_file_imports(
        'src/pages/dashboard/analytics/index.js',
        'Component 2 (analytics/index.js)',
        0.25
    )

    # Component 3: settings/profile/edit.js (0.25 points)
    check_file_imports(
        'src/pages/settings/profile/edit.js',
        'Component 3 (settings/profile/edit.js)',
        0.25
    )

    # Component 4: products/inventory/overview.js (0.20 points)
    check_file_imports(
        'src/pages/products/inventory/overview.js',
        'Component 4 (products/inventory/overview.js)',
        0.20
    )

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

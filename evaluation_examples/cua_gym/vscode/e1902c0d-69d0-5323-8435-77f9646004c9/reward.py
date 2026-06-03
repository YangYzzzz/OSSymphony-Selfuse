"""
Reward Script: Multi-cursor editing workflow — rename fetchData to fetchDataLegacy and add JSDoc @deprecated tag
Task ID: vscode_code_100
Domain: vs_code
Scoring:
  Component 1 (0.4): legacy.ts — function renamed to fetchDataLegacy AND @deprecated JSDoc comment added
  Component 2 (0.3): api.ts — import and all calls updated to fetchDataLegacy
  Component 3 (0.3): dashboard.ts — import and all calls updated to fetchDataLegacy
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user/project'
TASK_ID = 'vscode_code_100'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    legacy_path = os.path.join(WORKDIR, 'legacy.ts')
    api_path = os.path.join(WORKDIR, 'api.ts')
    dashboard_path = os.path.join(WORKDIR, 'dashboard.ts')

    # Pre-condition: all files must exist
    for path in [legacy_path, api_path, dashboard_path]:
        if not os.path.exists(path):
            print(f"CRITICAL: Required file not found: {path}")
            print("REWARD: 0.0")
            return 0.0

    # Component 1: legacy.ts — function renamed to fetchDataLegacy AND @deprecated JSDoc comment added (0.4 points)
    # Task requires:
    #   - 'fetchData' renamed to 'fetchDataLegacy' (the export function definition)
    #   - JSDoc @deprecated tag added above the function
    try:
        with open(legacy_path, 'r') as f:
            legacy_content = f.read()

        # Check 1a: function definition uses fetchDataLegacy (renamed from fetchData)
        has_renamed_function = bool(re.search(r'export function fetchDataLegacy\s*\(', legacy_content))

        # Check 1b: @deprecated JSDoc comment exists above the function
        has_deprecated_jsdoc = '@deprecated' in legacy_content

        # Check 1c: old name 'fetchData(' should NOT be the export function definition
        # (It's OK if 'fetchData' still appears in comments or the fetchDataV2 name, but the
        # standalone function export should not exist with the old name)
        has_old_export = bool(re.search(r'export function fetchData\b(?!V2|Legacy)', legacy_content))

        if has_renamed_function and has_deprecated_jsdoc and not has_old_export:
            print(f"PASS: Component 1 — legacy.ts: function renamed to fetchDataLegacy and @deprecated JSDoc added (0.4 pts)")
            total_score += 0.4
        elif has_renamed_function and not has_deprecated_jsdoc:
            print(f"FAIL: Component 1 — legacy.ts: function renamed to fetchDataLegacy but @deprecated JSDoc missing")
        elif not has_renamed_function and has_deprecated_jsdoc:
            print(f"FAIL: Component 1 — legacy.ts: @deprecated JSDoc present but function not renamed (has_renamed={has_renamed_function}, has_old_export={has_old_export})")
        elif has_old_export:
            print(f"FAIL: Component 1 — legacy.ts: original 'export function fetchData' still exists (not renamed)")
        else:
            print(f"FAIL: Component 1 — legacy.ts: function not renamed (has_renamed={has_renamed_function}) and @deprecated missing ({has_deprecated_jsdoc})")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not read legacy.ts: {e}")

    # Component 2: api.ts — import and all function calls updated to fetchDataLegacy (0.3 points)
    # Task requires:
    #   - import statement uses { fetchDataLegacy } instead of { fetchData }
    #   - All 2 function call sites use fetchDataLegacy (getUsers, getProducts)
    try:
        with open(api_path, 'r') as f:
            api_content = f.read()

        # Check 2a: import uses fetchDataLegacy
        has_import_legacy = bool(re.search(r"import\s*\{\s*fetchDataLegacy\s*\}\s*from\s*['\"]\.\/legacy['\"]", api_content))

        # Check 2b: no remaining import of fetchData (old name)
        has_import_old = bool(re.search(r"import\s*\{[^}]*\bfetchData\b(?!Legacy|V2)[^}]*\}\s*from\s*['\"]\.\/legacy['\"]", api_content))

        # Check 2c: all calls use fetchDataLegacy
        # Count calls: getUsers and getProducts each call fetchDataLegacy once
        legacy_calls_in_api = len(re.findall(r'\bfetchDataLegacy\s*\(', api_content))
        old_calls_in_api = len(re.findall(r'\bfetchData\s*\((?!.*Legacy)', api_content))
        # Use a simpler check: no bare 'fetchData(' (not followed by Legacy or V2)
        old_bare_calls = len(re.findall(r'\bfetchData(?!Legacy|V2)\s*\(', api_content))

        if has_import_legacy and not has_import_old and legacy_calls_in_api >= 2 and old_bare_calls == 0:
            print(f"PASS: Component 2 — api.ts: import updated to fetchDataLegacy, {legacy_calls_in_api} calls use fetchDataLegacy (0.3 pts)")
            total_score += 0.3
        else:
            details = []
            if not has_import_legacy:
                details.append("import not updated to fetchDataLegacy")
            if has_import_old:
                details.append("old import { fetchData } still present")
            if legacy_calls_in_api < 2:
                details.append(f"only {legacy_calls_in_api} fetchDataLegacy calls (expected 2)")
            if old_bare_calls > 0:
                details.append(f"{old_bare_calls} old fetchData( calls still present")
            print(f"FAIL: Component 2 — api.ts: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not read api.ts: {e}")

    # Component 3: dashboard.ts — import and all function calls updated to fetchDataLegacy (0.3 points)
    # Task requires:
    #   - import statement uses { fetchDataLegacy } instead of { fetchData }
    #   - All 2 function call sites use fetchDataLegacy (loadDashboard makes 2 calls)
    try:
        with open(dashboard_path, 'r') as f:
            dashboard_content = f.read()

        # Check 3a: import uses fetchDataLegacy
        has_import_legacy = bool(re.search(r"import\s*\{\s*fetchDataLegacy\s*\}\s*from\s*['\"]\.\/legacy['\"]", dashboard_content))

        # Check 3b: no remaining import of fetchData (old name)
        has_import_old = bool(re.search(r"import\s*\{[^}]*\bfetchData\b(?!Legacy|V2)[^}]*\}\s*from\s*['\"]\.\/legacy['\"]", dashboard_content))

        # Check 3c: all calls use fetchDataLegacy (2 calls expected in loadDashboard)
        legacy_calls_in_dashboard = len(re.findall(r'\bfetchDataLegacy\s*\(', dashboard_content))
        old_bare_calls = len(re.findall(r'\bfetchData(?!Legacy|V2)\s*\(', dashboard_content))

        if has_import_legacy and not has_import_old and legacy_calls_in_dashboard >= 2 and old_bare_calls == 0:
            print(f"PASS: Component 3 — dashboard.ts: import updated to fetchDataLegacy, {legacy_calls_in_dashboard} calls use fetchDataLegacy (0.3 pts)")
            total_score += 0.3
        else:
            details = []
            if not has_import_legacy:
                details.append("import not updated to fetchDataLegacy")
            if has_import_old:
                details.append("old import { fetchData } still present")
            if legacy_calls_in_dashboard < 2:
                details.append(f"only {legacy_calls_in_dashboard} fetchDataLegacy calls (expected 2)")
            if old_bare_calls > 0:
                details.append(f"{old_bare_calls} old fetchData( calls still present")
            print(f"FAIL: Component 3 — dashboard.ts: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not read dashboard.ts: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

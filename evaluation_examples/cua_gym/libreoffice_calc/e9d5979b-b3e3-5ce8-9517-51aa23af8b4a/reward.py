"""
Reward Script: VSCode Rename Symbol - App to MainApplication
Task ID: vscode_wf_033
Domain: vscode (file-based verification)
Scoring:
  Component 1 (0.30): App.jsx function declaration renamed to MainApplication
  Component 2 (0.20): App.jsx export default renamed to MainApplication
  Component 3 (0.25): index.jsx import and JSX usage updated to MainApplication
  Component 4 (0.25): routes.jsx import and JSX usage updated to MainApplication
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_033'

APP_JSX = os.path.join(WORKDIR, 'project', 'src', 'components', 'App.jsx')
INDEX_JSX = os.path.join(WORKDIR, 'project', 'src', 'index.jsx')
ROUTES_JSX = os.path.join(WORKDIR, 'project', 'src', 'routes.jsx')


def read_file(path):
    """Read file content, return None on failure."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"ERROR: Cannot read {path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Component 1: App.jsx function declaration renamed (0.30 points) ---
    try:
        content = read_file(APP_JSX)
        if content is None:
            print("FAIL: Component 1 -- App.jsx not found")
        else:
            # Check that 'function MainApplication()' exists
            has_new_decl = bool(re.search(r'function\s+MainApplication\s*\(', content))
            # Check that 'function App()' does NOT exist
            has_old_decl = bool(re.search(r'function\s+App\s*\(', content))

            if has_new_decl and not has_old_decl:
                print(f"PASS: Component 1 -- function MainApplication() found in App.jsx (0.30 pts)")
                total_score += 0.30
            elif has_new_decl and has_old_decl:
                print(f"PARTIAL: Component 1 -- MainApplication found but old App declaration still present")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 -- Expected 'function MainApplication()', found old declaration or missing")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # --- Component 2: App.jsx export default renamed (0.20 points) ---
    try:
        content = read_file(APP_JSX)
        if content is None:
            print("FAIL: Component 2 -- App.jsx not found")
        else:
            # Check 'export default MainApplication'
            has_new_export = bool(re.search(r'export\s+default\s+MainApplication\b', content))
            # Check old export is gone
            # Be careful: 'export default App' but NOT 'export default AppRoutes' etc.
            has_old_export = bool(re.search(r'export\s+default\s+App\b(?!lication|Routes)', content))

            if has_new_export and not has_old_export:
                print(f"PASS: Component 2 -- export default MainApplication in App.jsx (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 -- Expected 'export default MainApplication', "
                      f"new_export={has_new_export}, old_export={has_old_export}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # --- Component 3: index.jsx import and usage updated (0.25 points) ---
    try:
        content = read_file(INDEX_JSX)
        if content is None:
            print("FAIL: Component 3 -- index.jsx not found")
        else:
            # Check import statement uses MainApplication
            has_new_import = bool(re.search(r'import\s+MainApplication\b', content))
            # Check JSX usage <MainApplication />
            has_new_jsx = bool(re.search(r'<MainApplication\s*/?\s*>', content))
            # Check old references are gone (identifiers only, not file paths in strings)
            # Remove string literals (import paths like './components/App') before checking
            content_no_strings = re.sub(r"['\"][^'\"]*['\"]", '""', content)
            has_old_ref = bool(re.search(r'(?<![A-Za-z])App(?!lication|Routes)(?![A-Za-z])', content_no_strings))

            if has_new_import and has_new_jsx and not has_old_ref:
                print(f"PASS: Component 3 -- index.jsx fully updated to MainApplication (0.25 pts)")
                total_score += 0.25
            elif has_new_import or has_new_jsx:
                print(f"PARTIAL: Component 3 -- index.jsx partially updated "
                      f"(import={has_new_import}, jsx={has_new_jsx}, old_ref={has_old_ref}) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 -- index.jsx not updated to MainApplication")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # --- Component 4: routes.jsx import and usage updated (0.25 points) ---
    try:
        content = read_file(ROUTES_JSX)
        if content is None:
            print("FAIL: Component 4 -- routes.jsx not found")
        else:
            # Check import statement uses MainApplication
            has_new_import = bool(re.search(r'import\s+MainApplication\b', content))
            # Check JSX usage <MainApplication />
            has_new_jsx = bool(re.search(r'<MainApplication\s*/?\s*>', content))
            # Check old 'App' references are gone (identifiers only, not file paths in strings)
            content_no_strings = re.sub(r"['\"][^'\"]*['\"]", '""', content)
            has_old_ref = bool(re.search(r'(?<![A-Za-z])App(?!lication|Routes)(?![A-Za-z])', content_no_strings))

            if has_new_import and has_new_jsx and not has_old_ref:
                print(f"PASS: Component 4 -- routes.jsx fully updated to MainApplication (0.25 pts)")
                total_score += 0.25
            elif has_new_import or has_new_jsx:
                print(f"PARTIAL: Component 4 -- routes.jsx partially updated "
                      f"(import={has_new_import}, jsx={has_new_jsx}, old_ref={has_old_ref}) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 -- routes.jsx not updated to MainApplication")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

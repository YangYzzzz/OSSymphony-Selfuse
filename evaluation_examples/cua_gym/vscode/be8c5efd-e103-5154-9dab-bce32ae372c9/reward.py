"""
Reward Script: VSCode CLI workspace management script verification
Task ID: vscode_gf5_049
Domain: vscode
Scoring: 7 components checking script existence, structure, and CLI usage patterns
"""

import os
import stat
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_049'

SCRIPT_PATH = os.path.join(WORKDIR, 'projects', 'vscode-automation', 'manage_workspace.py')
EXPORTS_PATH = os.path.join(WORKDIR, 'exports', 'extensions.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: script file must exist
    if not os.path.exists(SCRIPT_PATH):
        print(f"CRITICAL: Script not found at {SCRIPT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(SCRIPT_PATH, 'r') as f:
            script_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read script: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Script is executable (0.1 points)
    # This changes from initial (no file) to golden (executable file)
    try:
        file_stat = os.stat(SCRIPT_PATH)
        is_executable = bool(file_stat.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
        if is_executable:
            print(f"PASS: Component 1 — Script is executable (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — Script exists but is not executable (mode: {oct(file_stat.st_mode)})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Script imports subprocess (0.1 points)
    # The task requires using subprocess to run 'code' commands
    try:
        if re.search(r'import\s+subprocess', script_content):
            print(f"PASS: Component 2 — Script imports subprocess (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2 — 'import subprocess' not found in script")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Uses 'code --folder-uri' to open target-repo (0.15 points)
    # Task requires: uses subprocess to run 'code --folder-uri' to open the repo
    try:
        has_folder_uri = bool(re.search(r'--folder-uri', script_content))
        has_target_repo = bool(re.search(r'target-repo', script_content))
        if has_folder_uri and has_target_repo:
            print(f"PASS: Component 3 — Script uses 'code --folder-uri' with target-repo (0.15 pts)")
            total_score += 0.15
        elif has_folder_uri:
            print(f"PARTIAL: Component 3 — Found --folder-uri but no reference to target-repo (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 3 — No '--folder-uri' found in script")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Installs 3 extensions via 'code --install-extension' (0.2 points)
    # Task requires installing 3 specific extensions by ID
    # The script may use a loop with a list, so we count extension IDs and check for --install-extension usage
    try:
        has_install_ext = bool(re.search(r'--install-extension', script_content))
        # Count unique extension ID strings (publisher.name format like "ms-python.python")
        ext_id_pattern = re.findall(r'["\']([a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)["\']', script_content)
        # Filter to likely VSCode extension IDs: publisher.extension-name format
        # Exclude Python module references like os.path, sys.path, json.tool etc.
        python_modules = {'os.path', 'os.environ', 'os.makedirs', 'os.path', 'sys.path', 'sys.modules',
                          'json.tool', 'json.load', 'json.loads', 'json.dump', 'json.dumps',
                          'subprocess.run', 'subprocess.Popen', 'importlib.util', 're.search'}
        likely_ext_ids = [eid for eid in ext_id_pattern
                          if eid not in python_modules
                          and not eid.startswith('os.')
                          and not eid.startswith('sys.')
                          and not eid.startswith('json.')
                          and not eid.startswith('subprocess.')
                          and not eid.startswith('importlib.')
                          and not eid.startswith('re.')
                          and not eid.endswith('.py')
                          and not eid.endswith('.txt')
                          and not eid.endswith('.json')]
        unique_ext_ids = list(set(likely_ext_ids))

        if has_install_ext and len(unique_ext_ids) >= 3:
            print(f"PASS: Component 4 — Script uses --install-extension with {len(unique_ext_ids)} extension IDs: {unique_ext_ids[:6]} (0.2 pts)")
            total_score += 0.2
        elif has_install_ext and len(unique_ext_ids) >= 1:
            partial = round(0.2 * min(len(unique_ext_ids), 3) / 3, 2)
            print(f"PARTIAL: Component 4 — Script uses --install-extension but only {len(unique_ext_ids)} extension IDs found ({partial} pts)")
            total_score += partial
        elif has_install_ext:
            print(f"PARTIAL: Component 4 — Found --install-extension but no recognizable extension IDs (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 — No '--install-extension' usage found in script")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Exports extension list to ~/exports/extensions.txt (0.2 points)
    # Script must use 'code --list-extensions' and write output to exports/extensions.txt
    try:
        has_list_extensions = bool(re.search(r'--list-extensions', script_content))
        has_export_path = bool(re.search(r'exports/extensions\.txt', script_content) or
                               re.search(r'extensions\.txt', script_content))

        if has_list_extensions and has_export_path:
            # Also verify the exports file exists on golden (task completion artifact)
            if os.path.exists(EXPORTS_PATH):
                with open(EXPORTS_PATH, 'r') as f:
                    export_content = f.read().strip()
                if len(export_content) > 0:
                    print(f"PASS: Component 5 — Script lists extensions and writes to exports/extensions.txt; file exists with content (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"PARTIAL: Component 5 — Script has correct logic but exports file is empty (0.1 pts)")
                    total_score += 0.1
            else:
                # Script has the right code but file doesn't exist yet (this is ok for script verification)
                print(f"PARTIAL: Component 5 — Script has --list-extensions and export path but exports file not yet created (0.1 pts)")
                total_score += 0.1
        elif has_list_extensions:
            print(f"PARTIAL: Component 5 — Found --list-extensions but no export path reference (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5 — No '--list-extensions' found in script")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Disables non-allowed extensions via 'code --disable-extension' (0.15 points)
    # Script must read allowed-extensions.txt and disable unlisted extensions
    try:
        has_disable = bool(re.search(r'--disable-extension', script_content))
        has_allowed_ref = bool(re.search(r'allowed[_-]extensions', script_content))

        if has_disable and has_allowed_ref:
            print(f"PASS: Component 6 — Script uses --disable-extension with allowed-extensions reference (0.15 pts)")
            total_score += 0.15
        elif has_disable:
            print(f"PARTIAL: Component 6 — Found --disable-extension but no allowed-extensions reference (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 6 — No '--disable-extension' found in script")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Script prints a summary upon completion (0.1 points)
    # Task requires: "Script completes without Python exceptions and prints a summary"
    try:
        # Check for summary-related prints
        has_summary = bool(re.search(r'(?i)(summary|completed|status|done|finished)', script_content))
        has_main = bool(re.search(r'if\s+__name__\s*==\s*["\']__main__["\']', script_content) or
                        re.search(r'def\s+main\s*\(', script_content))

        if has_summary and has_main:
            print(f"PASS: Component 7 — Script has main entry point and prints summary (0.1 pts)")
            total_score += 0.1
        elif has_summary:
            print(f"PARTIAL: Component 7 — Script has summary text but no clear main entry (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 7 — No summary/completion message found in script")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SCRIPT_PATH):
    print(f"File not found: {SCRIPT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()

"""
Reward Script: Build a VSCode extension showing Git branch name in status bar
Task ID: vscode_gf5_029
Domain: vscode (extension development)
Scoring:
  Component 1 (0.15): Extension directory structure exists (package.json + source file)
  Component 2 (0.25): package.json has valid VSCode extension fields (engines.vscode)
  Component 3 (0.20): Activation events include workspaceContains:.git or onStartupFinished
  Component 4 (0.25): Source file creates status bar item and displays branch name
  Component 5 (0.15): Source file has branch update/change detection mechanism
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_029'
EXT_DIR = os.path.join(WORKDIR, 'projects', 'branch-indicator')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Precondition: Extension directory exists ----
    if not os.path.isdir(EXT_DIR):
        print(f"CRITICAL: Extension directory {EXT_DIR} does not exist")
        print("REWARD: 0.0")
        return 0.0

    # ---- Component 1: Extension structure (0.15 pts) ----
    # package.json AND at least one source file (ts or js) must exist
    try:
        pkg_path = os.path.join(EXT_DIR, 'package.json')
        has_pkg = os.path.isfile(pkg_path)

        # Look for source file in src/ or root (extension.ts, extension.js, etc.)
        source_file = None
        for candidate in [
            os.path.join(EXT_DIR, 'src', 'extension.ts'),
            os.path.join(EXT_DIR, 'src', 'extension.js'),
            os.path.join(EXT_DIR, 'extension.ts'),
            os.path.join(EXT_DIR, 'extension.js'),
            os.path.join(EXT_DIR, 'src', 'index.ts'),
            os.path.join(EXT_DIR, 'src', 'index.js'),
        ]:
            if os.path.isfile(candidate):
                source_file = candidate
                break

        if has_pkg and source_file:
            print(f"PASS: Component 1 — package.json exists and source file found at {source_file} (0.15 pts)")
            total_score += 0.15
        elif has_pkg:
            print(f"FAIL: Component 1 — package.json exists but no source file (extension.ts/js) found")
        else:
            print(f"FAIL: Component 1 — package.json not found in {EXT_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---- Component 2: package.json has VSCode engine (0.25 pts) ----
    try:
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)

        engines = pkg.get('engines', {})
        vscode_engine = engines.get('vscode', '')

        # Must have engines.vscode set to a version string
        if vscode_engine and isinstance(vscode_engine, str) and len(vscode_engine) > 0:
            print(f"PASS: Component 2 — engines.vscode = '{vscode_engine}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — engines.vscode missing or empty, found: {engines}")
    except FileNotFoundError:
        print(f"FAIL: Component 2 — package.json not found")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 2 — package.json is invalid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---- Component 3: Activation events (0.20 pts) ----
    # Must include workspaceContains:.git or onStartupFinished
    try:
        if not has_pkg:
            print(f"FAIL: Component 3 — package.json not found, cannot check activationEvents")
            raise ValueError("no package.json")
        activation_events = pkg.get('activationEvents', [])
        # Also check contributes for activation in newer VS Code extension format
        # In newer VSCode, activationEvents can be inferred from contributes, but
        # explicit listing is expected here.

        has_workspace_git = any('workspaceContains:.git' in str(ev) for ev in activation_events)
        has_startup = any('onStartupFinished' in str(ev) for ev in activation_events)
        # Also accept wildcard activation
        has_wildcard = any(ev == '*' for ev in activation_events)

        if has_workspace_git or has_startup or has_wildcard:
            details = []
            if has_workspace_git:
                details.append('workspaceContains:.git')
            if has_startup:
                details.append('onStartupFinished')
            if has_wildcard:
                details.append('*')
            print(f"PASS: Component 3 — activation events include {', '.join(details)} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — activationEvents missing workspaceContains:.git or onStartupFinished, found: {activation_events}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---- Component 4: Source file creates status bar item with branch display (0.25 pts) ----
    # The source must reference status bar creation AND branch display
    try:
        if source_file is None:
            print(f"FAIL: Component 4 — no source file found")
        else:
            with open(source_file, 'r') as f:
                src_content = f.read()
            src_lower = src_content.lower()

            # Check for status bar item creation
            has_status_bar = (
                'createstatusbaritem' in src_lower or
                'statusbaritem' in src_lower or
                'statusbar' in src_lower or
                'status_bar' in src_lower
            )

            # Check for branch name display - must reference "Branch:" or branch name pattern
            has_branch_display = (
                'branch' in src_lower and
                (
                    'branch:' in src_content or   # literal "Branch:" in template string
                    'Branch:' in src_content or
                    re.search(r'branch.*name', src_lower) is not None or
                    re.search(r'head.*name', src_lower) is not None or
                    'git-branch' in src_lower or   # VSCode codicon
                    'refs/heads' in src_content     # direct git HEAD reading
                )
            )

            if has_status_bar and has_branch_display:
                print(f"PASS: Component 4 — source creates status bar item and displays branch name (0.25 pts)")
                total_score += 0.25
            elif has_status_bar:
                print(f"FAIL: Component 4 — status bar creation found but no branch display logic")
            elif has_branch_display:
                print(f"FAIL: Component 4 — branch display logic found but no status bar item creation")
            else:
                print(f"FAIL: Component 4 — neither status bar creation nor branch display found in source")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---- Component 5: Branch update mechanism (0.15 pts) ----
    # Must have some form of branch change detection: polling, event listener, git API
    try:
        if source_file is None:
            print(f"FAIL: Component 5 — no source file found")
        else:
            # Already have src_content from Component 4
            src_lower = src_content.lower()

            has_polling = (
                'setinterval' in src_lower or
                'settimeout' in src_lower or
                'polling' in src_lower
            )
            has_event_listener = (
                'ondidchange' in src_lower or
                'ondidopen' in src_lower or
                'onDidChangeActiveTextEditor' in src_content or
                'onDidChangeConfiguration' in src_content or
                'ondidchangeactivetexteditor' in src_lower
            )
            has_git_api = (
                'getapi' in src_lower or
                'vscode.git' in src_lower or
                'getextension' in src_lower
            )
            has_file_watcher = (
                'filewatcher' in src_lower or
                'createfilesystemwatcher' in src_lower or
                'watchfile' in src_lower or
                'fs.watch' in src_lower
            )

            if has_polling or has_event_listener or has_git_api or has_file_watcher:
                mechanisms = []
                if has_polling:
                    mechanisms.append('polling')
                if has_event_listener:
                    mechanisms.append('event listeners')
                if has_git_api:
                    mechanisms.append('Git API')
                if has_file_watcher:
                    mechanisms.append('file watcher')
                print(f"PASS: Component 5 — branch update mechanism(s): {', '.join(mechanisms)} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — no branch update/change detection mechanism found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

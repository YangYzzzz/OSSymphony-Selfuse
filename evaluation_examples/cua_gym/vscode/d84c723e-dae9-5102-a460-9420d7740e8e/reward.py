"""
Reward Script: Set up VSCode settings for TypeScript project
Task ID: vscode_code_095
Domain: vs_code
Scoring:
  Component 1 (0.4): Core editor save settings — formatOnSave + organizeImports on save
  Component 2 (0.3): Editor behavior — bracketPairColorization, linkedEditing
  Component 3 (0.3): File settings — trimTrailingWhitespace, insertFinalNewline, eol
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_095'
SETTINGS_PATH = '/home/user/new-project/.vscode/settings.json'


def _is_subset(expected, actual) -> bool:
    """Recursive subset check: expected keys/values must all appear in actual."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def load_settings(path: str):
    """Load settings.json, stripping JSONC-style comments if needed."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip // comments (JSONC support)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Could not parse settings.json: {e}")
        return None


def verify_task(settings_path: str) -> float:
    """
    Verify VSCode workspace settings for TypeScript project.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: settings.json must exist
    if not os.path.exists(settings_path):
        print(f"FAIL: settings.json not found at {settings_path}")
        print("REWARD: 0.0")
        return 0.0

    settings = load_settings(settings_path)
    if settings is None:
        print(f"FAIL: Could not load/parse settings.json at {settings_path}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Loaded settings from {settings_path}")
    print(f"INFO: Settings keys: {list(settings.keys())}")

    # Component 1: Core editor save settings (0.4 points)
    # Task requires: formatOnSave=true AND organizeImports on save
    try:
        format_on_save = settings.get("editor.formatOnSave")
        code_actions = settings.get("editor.codeActionsOnSave", {})
        organize_imports = code_actions.get("source.organizeImports")

        format_ok = format_on_save is True
        organize_ok = organize_imports == "explicit"

        if format_ok and organize_ok:
            print(f"PASS: Component 1 — editor.formatOnSave=true AND source.organizeImports='explicit' (0.4 pts)")
            total_score += 0.4
        elif format_ok and not organize_ok:
            print(f"FAIL: Component 1 — editor.formatOnSave=true but source.organizeImports={organize_imports!r} (expected 'explicit')")
        elif not format_ok and organize_ok:
            print(f"FAIL: Component 1 — source.organizeImports='explicit' but editor.formatOnSave={format_on_save!r} (expected true)")
        else:
            print(f"FAIL: Component 1 — editor.formatOnSave={format_on_save!r}, source.organizeImports={organize_imports!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Editor behavior settings (0.3 points)
    # Task requires: bracketPairColorization.enabled=true, linkedEditing=true
    try:
        bracket_color = settings.get("editor.bracketPairColorization.enabled")
        linked_editing = settings.get("editor.linkedEditing")

        bracket_ok = bracket_color is True
        linked_ok = linked_editing is True

        if bracket_ok and linked_ok:
            print(f"PASS: Component 2 — bracketPairColorization.enabled=true AND linkedEditing=true (0.3 pts)")
            total_score += 0.3
        elif bracket_ok and not linked_ok:
            print(f"FAIL: Component 2 — bracketPairColorization.enabled=true but editor.linkedEditing={linked_editing!r} (expected true)")
        elif not bracket_ok and linked_ok:
            print(f"FAIL: Component 2 — editor.linkedEditing=true but bracketPairColorization.enabled={bracket_color!r} (expected true)")
        else:
            print(f"FAIL: Component 2 — bracketPairColorization.enabled={bracket_color!r}, linkedEditing={linked_editing!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File settings (0.3 points)
    # Task requires: trimTrailingWhitespace=true, insertFinalNewline=true, eol="\n"
    try:
        trim_whitespace = settings.get("files.trimTrailingWhitespace")
        insert_newline = settings.get("files.insertFinalNewline")
        eol = settings.get("files.eol")

        trim_ok = trim_whitespace is True
        newline_ok = insert_newline is True
        eol_ok = eol == "\n"

        if trim_ok and newline_ok and eol_ok:
            print(f"PASS: Component 3 — trimTrailingWhitespace=true, insertFinalNewline=true, eol='\\n' (0.3 pts)")
            total_score += 0.3
        else:
            failed = []
            if not trim_ok:
                failed.append(f"files.trimTrailingWhitespace={trim_whitespace!r} (expected true)")
            if not newline_ok:
                failed.append(f"files.insertFinalNewline={insert_newline!r} (expected true)")
            if not eol_ok:
                failed.append(f"files.eol={eol!r} (expected '\\n')")
            print(f"FAIL: Component 3 — {'; '.join(failed)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against canonical path
verify_task(SETTINGS_PATH)

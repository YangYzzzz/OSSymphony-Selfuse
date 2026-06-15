"""
Reward Script: Enable parameter hints for pd.merge in VSCode
Task ID: vscode_lp_032
Domain: vscode
Scoring:
  Component 1 (0.6): editor.parameterHints.enabled is true
  Component 2 (0.4): parameterHints enabled AND Pylance language server active
                      AND analysis.py with pd.merge call exists (full environment ready)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_032'
SETTINGS_PATH = os.path.expanduser('~/.config/Code/User/settings.json')
ANALYSIS_FILE = os.path.join(WORKDIR, 'workspace', 'analysis.py')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load settings — this is the primary artifact to verify
    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load VSCode settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.parameterHints.enabled is true (0.6 points)
    # This is the core task change — initial has it false, golden has it true
    try:
        param_hints = settings.get('editor.parameterHints.enabled')
        if param_hints is True:
            print(f"PASS: Component 1 — editor.parameterHints.enabled is true (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — editor.parameterHints.enabled expected true, found: {param_hints}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Full environment ready for parameter hints (0.4 points)
    # parameterHints must be enabled AND Pylance must be the language server
    # AND the analysis.py file with pd.merge must exist
    # This compound check is anchored to the task change (parameterHints.enabled)
    try:
        param_hints = settings.get('editor.parameterHints.enabled')
        lang_server = settings.get('python.languageServer')
        hover_enabled = settings.get('editor.hover.enabled')

        # Check analysis.py exists and contains pd.merge
        file_exists = os.path.exists(ANALYSIS_FILE)
        has_merge_call = False
        if file_exists:
            with open(ANALYSIS_FILE, 'r') as f:
                content = f.read()
            has_merge_call = 'pd.merge' in content

        conditions_met = (
            param_hints is True
            and lang_server == 'Pylance'
            and hover_enabled is True
            and file_exists
            and has_merge_call
        )

        if conditions_met:
            print(f"PASS: Component 2 — parameterHints=true, languageServer=Pylance, "
                  f"hover=true, analysis.py with pd.merge exists (0.4 pts)")
            total_score += 0.4
        else:
            details = []
            if param_hints is not True:
                details.append(f"parameterHints={param_hints}")
            if lang_server != 'Pylance':
                details.append(f"languageServer={lang_server}")
            if hover_enabled is not True:
                details.append(f"hover={hover_enabled}")
            if not file_exists:
                details.append("analysis.py missing")
            if not has_merge_call:
                details.append("pd.merge not found in analysis.py")
            print(f"FAIL: Component 2 — conditions not met: {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()

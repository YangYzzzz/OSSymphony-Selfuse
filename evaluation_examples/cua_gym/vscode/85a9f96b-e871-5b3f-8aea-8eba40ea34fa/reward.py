"""
Reward Script: Configure VSCode language-specific indentation settings
Task ID: vscode_web_054
Domain: vscode
Scoring:
  Component 1: [javascript] editor.tabSize == 2  (0.2 pts)
  Component 2: [typescript] editor.tabSize == 2  (0.2 pts)
  Component 3: [json] and [jsonc] editor.tabSize == 2  (0.2 pts)
  Component 4: [python] editor.tabSize == 4  (0.2 pts)
  Component 5: [go] editor.insertSpaces == false  (0.2 pts)
"""

import json
import os
import re

SETTINGS_PATH = os.path.expanduser("~/.config/Code/User/settings.json")


def load_settings():
    """Load VSCode settings.json, stripping JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip // line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that language-specific indentation settings are configured.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: [javascript] editor.tabSize == 2 (0.2 points)
    try:
        js_section = settings.get("[javascript]", {})
        js_tab_size = js_section.get("editor.tabSize")
        if js_tab_size == 2:
            print(f"PASS: Component 1 -- [javascript] editor.tabSize is 2 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- [javascript] editor.tabSize expected 2, found: {js_tab_size}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: [typescript] editor.tabSize == 2 (0.2 points)
    try:
        ts_section = settings.get("[typescript]", {})
        ts_tab_size = ts_section.get("editor.tabSize")
        if ts_tab_size == 2:
            print(f"PASS: Component 2 -- [typescript] editor.tabSize is 2 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- [typescript] editor.tabSize expected 2, found: {ts_tab_size}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: [json] AND [jsonc] editor.tabSize == 2 (0.2 points)
    try:
        json_section = settings.get("[json]", {})
        jsonc_section = settings.get("[jsonc]", {})
        json_tab_size = json_section.get("editor.tabSize")
        jsonc_tab_size = jsonc_section.get("editor.tabSize")
        if json_tab_size == 2 and jsonc_tab_size == 2:
            print(f"PASS: Component 3 -- [json] and [jsonc] editor.tabSize are both 2 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- [json] tabSize={json_tab_size}, [jsonc] tabSize={jsonc_tab_size}, both expected 2")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: [python] editor.tabSize == 4 (0.2 points)
    # NOTE: The default global editor.tabSize is 4, but this component checks that
    # a LANGUAGE-SPECIFIC [python] section exists with editor.tabSize == 4.
    # This is distinct from the global default — the initial_env has no [python] section.
    try:
        py_section = settings.get("[python]")
        if py_section is not None and py_section.get("editor.tabSize") == 4:
            print(f"PASS: Component 4 -- [python] section exists with editor.tabSize 4 (0.2 pts)")
            total_score += 0.2
        else:
            if py_section is None:
                print(f"FAIL: Component 4 -- [python] section does not exist in settings")
            else:
                print(f"FAIL: Component 4 -- [python] editor.tabSize expected 4, found: {py_section.get('editor.tabSize')}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: [go] editor.insertSpaces == false (0.2 points)
    try:
        go_section = settings.get("[go]")
        if go_section is not None and go_section.get("editor.insertSpaces") is False:
            print(f"PASS: Component 5 -- [go] editor.insertSpaces is false (0.2 pts)")
            total_score += 0.2
        else:
            if go_section is None:
                print(f"FAIL: Component 5 -- [go] section does not exist in settings")
            else:
                print(f"FAIL: Component 5 -- [go] editor.insertSpaces expected false, found: {go_section.get('editor.insertSpaces')}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

"""
Reward Script: VSCode language-specific formatter + .prettierrc configuration
Task ID: vscode_gf1_050
Domain: vscode (settings + project config)
Scoring:
  - 4 language-scoped formatter settings in settings.json (0.2 + 0.2 + 0.2 + 0.1 = 0.7)
  - .prettierrc with 3 correct properties (0.1 + 0.1 + 0.1 = 0.3)
  Total: 1.0
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')
PRETTIERRC_PATH = os.path.join(HOME, 'projects', 'frontend', '.prettierrc')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def load_prettierrc():
    """Load .prettierrc as JSON."""
    try:
        with open(PRETTIERRC_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load .prettierrc: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Part A: VSCode settings.json language-scoped formatters ---

    settings = load_settings()
    if settings is None:
        print("CRITICAL: settings.json not loadable — scoring 0 for all settings components")
    else:
        # Component 1: [javascript] editor.defaultFormatter == esbenp.prettier-vscode (0.2 pts)
        try:
            js_section = settings.get('[javascript]', {})
            js_formatter = js_section.get('editor.defaultFormatter', '')
            if js_formatter == 'esbenp.prettier-vscode':
                print(f"PASS: Component 1 — [javascript] defaultFormatter is esbenp.prettier-vscode (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — [javascript] defaultFormatter expected 'esbenp.prettier-vscode', found '{js_formatter}'")
        except Exception as e:
            print(f"ERROR: Component 1 — {e}")

        # Component 2: [typescript] editor.defaultFormatter == esbenp.prettier-vscode (0.2 pts)
        try:
            ts_section = settings.get('[typescript]', {})
            ts_formatter = ts_section.get('editor.defaultFormatter', '')
            if ts_formatter == 'esbenp.prettier-vscode':
                print(f"PASS: Component 2 — [typescript] defaultFormatter is esbenp.prettier-vscode (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — [typescript] defaultFormatter expected 'esbenp.prettier-vscode', found '{ts_formatter}'")
        except Exception as e:
            print(f"ERROR: Component 2 — {e}")

        # Component 3: [css] editor.defaultFormatter == esbenp.prettier-vscode (0.2 pts)
        try:
            css_section = settings.get('[css]', {})
            css_formatter = css_section.get('editor.defaultFormatter', '')
            if css_formatter == 'esbenp.prettier-vscode':
                print(f"PASS: Component 3 — [css] defaultFormatter is esbenp.prettier-vscode (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — [css] defaultFormatter expected 'esbenp.prettier-vscode', found '{css_formatter}'")
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")

        # Component 4: [json] editor.defaultFormatter == esbenp.prettier-vscode (0.1 pts)
        try:
            json_section = settings.get('[json]', {})
            json_formatter = json_section.get('editor.defaultFormatter', '')
            if json_formatter == 'esbenp.prettier-vscode':
                print(f"PASS: Component 4 — [json] defaultFormatter is esbenp.prettier-vscode (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 4 — [json] defaultFormatter expected 'esbenp.prettier-vscode', found '{json_formatter}'")
        except Exception as e:
            print(f"ERROR: Component 4 — {e}")

    # --- Part B: .prettierrc file at /home/user/projects/frontend ---

    prettierrc = load_prettierrc()
    if prettierrc is None:
        print("CRITICAL: .prettierrc not loadable — scoring 0 for all .prettierrc components")
    else:
        # Component 5: singleQuote == true (0.1 pts)
        try:
            sq = prettierrc.get('singleQuote')
            if sq is True:
                print(f"PASS: Component 5 — .prettierrc singleQuote is true (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 5 — .prettierrc singleQuote expected true, found {sq}")
        except Exception as e:
            print(f"ERROR: Component 5 — {e}")

        # Component 6: printWidth == 100 (0.1 pts)
        try:
            pw = prettierrc.get('printWidth')
            if pw == 100:
                print(f"PASS: Component 6 — .prettierrc printWidth is 100 (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 6 — .prettierrc printWidth expected 100, found {pw}")
        except Exception as e:
            print(f"ERROR: Component 6 — {e}")

        # Component 7: trailingComma == "es5" (0.1 pts)
        try:
            tc = prettierrc.get('trailingComma')
            if tc == 'es5':
                print(f"PASS: Component 7 — .prettierrc trailingComma is 'es5' (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 7 — .prettierrc trailingComma expected 'es5', found '{tc}'")
        except Exception as e:
            print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

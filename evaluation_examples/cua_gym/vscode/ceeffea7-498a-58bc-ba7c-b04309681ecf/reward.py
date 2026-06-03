"""
Reward Script: Install TODO Highlight extension and configure keywords in VSCode
Task ID: vscode_ext_033
Domain: vs_code
Scoring:
  - Component 1: TODO Highlight extension installed (0.4 pts)
  - Component 2: settings.json has 'TODO:' keyword with yellow background (0.3 pts)
  - Component 3: settings.json has 'FIXME:' keyword with red background (0.3 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_033'

EXTENSIONS_JSON_PATH = os.path.join(WORKDIR, '.vscode', 'extensions', 'extensions.json')
SETTINGS_JSON_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')
EXTENSION_ID = 'wayou.vscode-todo-highlight'


def load_json_with_comments(file_path):
    """Load a JSON file, stripping // comments (JSONC support).
    Only strips lines where // appears outside of a string context (i.e., at the start of a line after whitespace).
    Uses a conservative approach: only strip lines that start with optional whitespace then //.
    """
    with open(file_path, 'r') as f:
        content = f.read()
    # Only strip lines that START with optional whitespace then //
    # This avoids stripping // inside URL strings like "file:///home/..."
    content_stripped = re.sub(r'^\s*//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content_stripped)


def load_extensions_json(file_path):
    """Load extensions.json directly using standard json.load (it is valid JSON, not JSONC)."""
    with open(file_path, 'r') as f:
        return json.load(f)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: TODO Highlight extension is installed (0.4 points)
    # Check that extensions.json contains an entry for wayou.vscode-todo-highlight
    # AND the extension directory exists under .vscode/extensions/
    try:
        if not os.path.exists(EXTENSIONS_JSON_PATH):
            print(f"FAIL: Component 1 — extensions.json not found at {EXTENSIONS_JSON_PATH}")
        else:
            ext_data = load_extensions_json(EXTENSIONS_JSON_PATH)
            # Check if list contains an entry with identifier.id == EXTENSION_ID
            matching_entries = [
                entry for entry in ext_data
                if isinstance(entry.get('identifier'), dict)
                and entry['identifier'].get('id', '').lower() == EXTENSION_ID.lower()
            ]

            if not matching_entries:
                print(f"FAIL: Component 1 — extension '{EXTENSION_ID}' not found in extensions.json")
            else:
                # Also verify the extension directory actually exists
                ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
                ext_dirs = [d for d in os.listdir(ext_dir) if d.lower().startswith('wayou.vscode-todo-highlight')]
                if ext_dirs:
                    print(f"PASS: Component 1 — TODO Highlight extension installed: {ext_dirs[0]} (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 1 — extensions.json has entry but extension directory not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: settings.json has 'TODO:' keyword configured with yellow background (0.3 points)
    # The todohighlight.keywords list must contain an entry with text='TODO:' and backgroundColor='yellow'
    try:
        if not os.path.exists(SETTINGS_JSON_PATH):
            print(f"FAIL: Component 2 — settings.json not found at {SETTINGS_JSON_PATH}")
        else:
            settings = load_json_with_comments(SETTINGS_JSON_PATH)
            keywords = settings.get('todohighlight.keywords', [])
            if not isinstance(keywords, list) or len(keywords) == 0:
                print(f"FAIL: Component 2 — 'todohighlight.keywords' not found or empty in settings.json")
            else:
                todo_entry = None
                for kw in keywords:
                    if isinstance(kw, dict) and kw.get('text', '').upper() == 'TODO:':
                        todo_entry = kw
                        break
                if todo_entry is None:
                    print(f"FAIL: Component 2 — No keyword with text='TODO:' found in todohighlight.keywords")
                else:
                    bg_color = todo_entry.get('backgroundColor', '')
                    if 'yellow' in str(bg_color).lower():
                        print(f"PASS: Component 2 — TODO: keyword has yellow backgroundColor: '{bg_color}' (0.3 pts)")
                        total_score += 0.3
                    else:
                        print(f"FAIL: Component 2 — TODO: keyword backgroundColor is '{bg_color}', expected yellow")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: settings.json has 'FIXME:' keyword configured with red background (0.3 points)
    # The todohighlight.keywords list must contain an entry with text='FIXME:' and backgroundColor='red'
    try:
        if not os.path.exists(SETTINGS_JSON_PATH):
            print(f"FAIL: Component 3 — settings.json not found at {SETTINGS_JSON_PATH}")
        else:
            settings = load_json_with_comments(SETTINGS_JSON_PATH)
            keywords = settings.get('todohighlight.keywords', [])
            if not isinstance(keywords, list) or len(keywords) == 0:
                print(f"FAIL: Component 3 — 'todohighlight.keywords' not found or empty in settings.json")
            else:
                fixme_entry = None
                for kw in keywords:
                    if isinstance(kw, dict) and kw.get('text', '').upper() == 'FIXME:':
                        fixme_entry = kw
                        break
                if fixme_entry is None:
                    print(f"FAIL: Component 3 — No keyword with text='FIXME:' found in todohighlight.keywords")
                else:
                    bg_color = fixme_entry.get('backgroundColor', '')
                    if 'red' in str(bg_color).lower():
                        print(f"PASS: Component 3 — FIXME: keyword has red backgroundColor: '{bg_color}' (0.3 pts)")
                        total_score += 0.3
                    else:
                        print(f"FAIL: Component 3 — FIXME: keyword backgroundColor is '{bg_color}', expected red")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

"""
Reward Script: Configure Emmet className for JSX/TSX and self-closing tags
Task ID: vscode_web_049
Domain: vs_code
Scoring:
  Component 1 (0.30): emmet.syntaxProfiles jsx/tsx self_closing_tag = xhtml
  Component 2 (0.20): emmet.syntaxProfiles html self_closing_tag = xhtml
  Component 3 (0.30): emmet.preferences jsx.className = true
  Component 4 (0.20): emmet.includeLanguages for JSX/TSX mapping
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_049'

# Possible settings locations (workspace-level and user-level)
WORKSPACE_SETTINGS = os.path.join(WORKDIR, 'projects', 'react-app', '.vscode', 'settings.json')
USER_SETTINGS = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_json_with_comments(path):
    """Load a JSON/JSONC file, stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content)
    return json.loads(content)


def merge_settings():
    """Load settings from workspace and user level, workspace takes precedence."""
    merged = {}
    for path in [USER_SETTINGS, WORKSPACE_SETTINGS]:
        if os.path.exists(path):
            try:
                data = load_json_with_comments(path)
                merged.update(data)
            except Exception as e:
                print(f"WARN: Could not parse {path}: {e}")
    return merged


def verify_task():
    """
    Verify Emmet configuration for className in JSX/TSX and self-closing tags.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = merge_settings()
    if not settings:
        print("CRITICAL: No settings found in workspace or user level")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: emmet.syntaxProfiles jsx/tsx with self_closing_tag = xhtml (0.30 points)
    # This ensures self-closing tags use xhtml style (space before slash) in JSX/TSX
    try:
        syntax_profiles = settings.get("emmet.syntaxProfiles", {})
        jsx_ok = False
        tsx_ok = False

        if isinstance(syntax_profiles, dict):
            # Check jsx profile
            jsx_profile = syntax_profiles.get("jsx", {})
            if isinstance(jsx_profile, dict) and jsx_profile.get("self_closing_tag") == "xhtml":
                jsx_ok = True
            elif isinstance(jsx_profile, str) and jsx_profile.lower() == "xhtml":
                jsx_ok = True

            # Check tsx profile
            tsx_profile = syntax_profiles.get("tsx", {})
            if isinstance(tsx_profile, dict) and tsx_profile.get("self_closing_tag") == "xhtml":
                tsx_ok = True
            elif isinstance(tsx_profile, str) and tsx_profile.lower() == "xhtml":
                tsx_ok = True

        if jsx_ok and tsx_ok:
            print(f"PASS: Component 1 — jsx and tsx syntaxProfiles have self_closing_tag=xhtml (0.30 pts)")
            total_score += 0.30
        elif jsx_ok or tsx_ok:
            print(f"PARTIAL: Component 1 — only one of jsx/tsx has self_closing_tag=xhtml (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — jsx/tsx syntaxProfiles missing or self_closing_tag != xhtml. Found: {syntax_profiles}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: emmet.syntaxProfiles html with self_closing_tag = xhtml (0.20 points)
    # The task says HTML profile should use self-closing with space (e.g. <img />)
    try:
        syntax_profiles = settings.get("emmet.syntaxProfiles", {})
        html_ok = False

        if isinstance(syntax_profiles, dict):
            html_profile = syntax_profiles.get("html", {})
            if isinstance(html_profile, dict) and html_profile.get("self_closing_tag") == "xhtml":
                html_ok = True
            elif isinstance(html_profile, str) and html_profile.lower() == "xhtml":
                html_ok = True

        if html_ok:
            print(f"PASS: Component 2 — html syntaxProfile has self_closing_tag=xhtml (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — html syntaxProfile missing or self_closing_tag != xhtml. Found html_profile: {syntax_profiles.get('html', 'NOT SET')}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: emmet.preferences jsx.className = true (0.30 points)
    # This makes Emmet use className instead of class in JSX/TSX
    try:
        preferences = settings.get("emmet.preferences", {})
        classname_ok = False

        if isinstance(preferences, dict):
            # Check jsx.className
            if preferences.get("jsx.className") is True:
                classname_ok = True

        if classname_ok:
            print(f"PASS: Component 3 — emmet.preferences jsx.className=true (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — emmet.preferences jsx.className not true. Found: {preferences}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: emmet.includeLanguages mapping for JSX/TSX (0.20 points)
    # Ensures Emmet recognizes typescript/javascript files as JSX/TSX
    try:
        include_langs = settings.get("emmet.includeLanguages", {})
        lang_ok = False

        if isinstance(include_langs, dict):
            # Check that typescript or javascript is mapped to their react counterparts
            ts_mapped = include_langs.get("typescript") in ("typescriptreact", "tsx")
            js_mapped = include_langs.get("javascript") in ("javascriptreact", "jsx")
            if ts_mapped or js_mapped:
                lang_ok = True

        if lang_ok:
            print(f"PASS: Component 4 — emmet.includeLanguages configured for JSX/TSX (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — emmet.includeLanguages not configured. Found: {include_langs}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

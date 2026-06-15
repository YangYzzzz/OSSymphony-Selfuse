"""
Reward Script: Install Chrome extensions from Must_have_extensions.docx and create installed_extensions.txt
Task ID: osworld_multi_apps_misc_011
Domain: multi_apps (Chrome + OS)

Scoring Rubric:
  Component 1: 6 required Chrome extensions installed        — 0.60 points (0.10 per extension)
  Component 2: installed_extensions.txt exists on Desktop    — 0.20 points
  Component 3: installed_extensions.txt lists all 6 names    — 0.20 points
  Total: 1.0
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_011'
DESKTOP_PATH = os.path.join(WORKDIR, 'Desktop')
EXTENSIONS_FILE = os.path.join(DESKTOP_PATH, 'installed_extensions.txt')

# The six extensions the task requires to be installed
REQUIRED_EXTENSIONS = [
    'Loom for Chrome',
    'Calendly for Chrome',
    'Miro',
    'Figma',
    'Slack for Chrome',
    'Zoom',
]

# Alias groups: some extensions may appear under variant names
EXTENSION_ALIASES = [
    {'Zoom', 'Zoom for Google Chrome', 'Zoom Chrome Extension'},
    {'Loom for Chrome', 'Loom'},
    {'Slack for Chrome', 'Slack'},
]


def canonicalize_ext(name):
    """Return a canonical name for extension aliases."""
    name_lower = name.lower()
    for group in EXTENSION_ALIASES:
        for alias in group:
            if alias.lower() == name_lower:
                return sorted(group)[0]
    return name


def get_installed_extension_names():
    """Read extension names from Chrome manifest.json files."""
    names = []
    extensions_dir = os.path.expanduser('~/.config/google-chrome/Default/Extensions')
    if not os.path.isdir(extensions_dir):
        # Try snap/chromium path
        extensions_dir = os.path.expanduser('~/snap/chromium/common/chromium/Default/Extensions')
    if not os.path.isdir(extensions_dir):
        return names
    for ext_id in os.listdir(extensions_dir):
        ext_path = os.path.join(extensions_dir, ext_id)
        if not os.path.isdir(ext_path):
            continue
        for version in os.listdir(ext_path):
            manifest = os.path.join(ext_path, version, 'manifest.json')
            if os.path.exists(manifest):
                try:
                    with open(manifest, 'r') as f:
                        data = json.load(f)
                        raw_name = data.get('name', '')
                        # Skip placeholder names that are not real extensions
                        if raw_name and not raw_name.startswith('__MSG_'):
                            names.append(raw_name)
                except Exception:
                    pass
    return names


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Check that all 6 required Chrome extensions are installed (0.60 points)
    # This fails on initial_env (no required extensions) and passes on golden_env (all 6 installed)
    try:
        installed_names = get_installed_extension_names()
        canonical_installed = [canonicalize_ext(n) for n in installed_names]
        canonical_installed_lower = [n.lower() for n in canonical_installed]

        print(f"INFO: Installed extension names (non-placeholder): {installed_names}")

        for required in REQUIRED_EXTENSIONS:
            canonical_req = canonicalize_ext(required)
            # Check by canonical match or substring match for robustness
            found = False
            for installed in installed_names:
                if (installed.lower() == required.lower() or
                        canonicalize_ext(installed).lower() == canonical_req.lower()):
                    found = True
                    break

            if found:
                print(f"PASS: Extension '{required}' is installed (+0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Extension '{required}' is NOT installed in Chrome")
    except Exception as e:
        print(f"ERROR: Component 1 — could not read Chrome extensions: {e}")

    # Component 2: installed_extensions.txt exists on Desktop (0.20 points)
    # This fails on initial_env (file absent) and passes on golden_env (file present)
    try:
        if os.path.isfile(EXTENSIONS_FILE):
            print(f"PASS: Component 2 — '{EXTENSIONS_FILE}' exists (+0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — '{EXTENSIONS_FILE}' does not exist on Desktop")
    except Exception as e:
        print(f"ERROR: Component 2 — could not check file existence: {e}")

    # Component 3: installed_extensions.txt lists all 6 required extension names (0.20 points)
    # This fails on initial_env (file absent) and passes on golden_env (all names listed)
    try:
        if not os.path.isfile(EXTENSIONS_FILE):
            print(f"FAIL: Component 3 — '{EXTENSIONS_FILE}' not found, cannot check content")
        else:
            with open(EXTENSIONS_FILE, 'r') as f:
                content = f.read()
            content_lower = content.lower()

            all_present = True
            for required in REQUIRED_EXTENSIONS:
                canonical_req = canonicalize_ext(required)
                # Check if the extension name (or a canonical alias) appears in the file
                found_in_file = False
                for alias_group in EXTENSION_ALIASES:
                    if required in alias_group:
                        if any(alias.lower() in content_lower for alias in alias_group):
                            found_in_file = True
                            break
                if not found_in_file:
                    if required.lower() in content_lower:
                        found_in_file = True

                if not found_in_file:
                    print(f"FAIL: Component 3 — '{required}' not listed in installed_extensions.txt")
                    all_present = False

            if all_present:
                print(f"PASS: Component 3 — all 6 extensions listed in installed_extensions.txt (+0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — not all 6 extensions found in installed_extensions.txt")
    except Exception as e:
        print(f"ERROR: Component 3 — could not read installed_extensions.txt: {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

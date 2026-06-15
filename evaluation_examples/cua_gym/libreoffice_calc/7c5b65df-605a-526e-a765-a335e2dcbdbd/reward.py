"""
Reward Script: Install Chrome extensions listed in Research_tools.docx
Task ID: osworld_multi_apps_misc_008
Domain: chrome (multi-app task)
Scoring:
  - Component 1: Zotero Connector installed                   (0.2 pts)
  - Component 2: Google Scholar Button installed               (0.2 pts)
  - Component 3: Unpaywall installed                           (0.2 pts)
  - Component 4: Research Rabbit installed                     (0.2 pts)
  - Component 5: Sci-Hub X Now installed                       (0.2 pts)
  Total: 1.0

Verification strategy:
  - Read manifest.json files from Chrome Extensions directory
  - Check that each required extension is present by name match
  - Also verify against the extensions.settings in Preferences for enabled state
  - None of these extensions exist in initial_env (only system extensions do),
    so ALL checks correctly fail on initial and pass only on golden.
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_008'

# Chrome profile path on Linux VM
CHROME_DEFAULT = os.path.expanduser('~/.config/google-chrome/Default')
EXTENSIONS_DIR = os.path.join(CHROME_DEFAULT, 'Extensions')
PREFS_FILE = os.path.join(CHROME_DEFAULT, 'Preferences')

# The five required research extensions (by normalized lowercase name)
# These are task-introduced changes — none exist in initial_env
REQUIRED_EXTENSIONS = [
    'zotero connector',
    'google scholar button',
    'unpaywall',
    'research rabbit',
    'sci-hub x now',
]

POINTS_PER_EXTENSION = 0.2


def get_installed_extension_names():
    """
    Read manifest.json files from Extensions directory and return
    a list of installed extension names (lowercased).
    """
    names = []
    if not os.path.isdir(EXTENSIONS_DIR):
        print(f"WARN: Extensions directory not found: {EXTENSIONS_DIR}")
        return names

    for ext_id in os.listdir(EXTENSIONS_DIR):
        ext_path = os.path.join(EXTENSIONS_DIR, ext_id)
        if not os.path.isdir(ext_path):
            continue
        for version in os.listdir(ext_path):
            manifest_path = os.path.join(ext_path, version, 'manifest.json')
            if os.path.exists(manifest_path):
                try:
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    name = data.get('name', '')
                    if name and not name.startswith('__MSG_'):
                        names.append(name.lower())
                except Exception as e:
                    print(f"WARN: Could not read manifest for {ext_id}/{version}: {e}")
    return names


def get_prefs_extension_names():
    """
    Read extension names from Chrome Preferences settings (backup method).
    Returns a list of extension names (lowercased) that are enabled (state==1).
    """
    names = []
    if not os.path.exists(PREFS_FILE):
        print(f"WARN: Preferences file not found: {PREFS_FILE}")
        return names

    try:
        with open(PREFS_FILE, 'r', encoding='utf-8') as f:
            prefs = json.load(f)
        ext_settings = prefs.get('extensions', {}).get('settings', {})
        for ext_id, settings in ext_settings.items():
            name = settings.get('manifest', {}).get('name', '')
            state = settings.get('state', 0)
            # state == 1 means enabled
            if name and state == 1 and not name.startswith('__MSG_'):
                names.append(name.lower())
    except Exception as e:
        print(f"WARN: Could not read Preferences: {e}")
    return names


def verify_task():
    """
    Verify that all five required Chrome extensions have been installed.
    Each extension is worth 0.2 points, totaling 1.0.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Gather installed extension names from both sources
    manifest_names = get_installed_extension_names()
    prefs_names = get_prefs_extension_names()

    # Union: extension is considered installed if found in either source
    all_installed = set(manifest_names) | set(prefs_names)
    print(f"INFO: Installed extensions detected: {sorted(all_installed)}")

    # Verify each required extension
    for ext_name in REQUIRED_EXTENSIONS:
        # Component: <ext_name> installed (0.2 points)
        try:
            found = any(ext_name in installed_name or installed_name in ext_name
                        for installed_name in all_installed)
            if found:
                print(f"PASS: Extension '{ext_name}' is installed ({POINTS_PER_EXTENSION} pts)")
                total_score += POINTS_PER_EXTENSION
            else:
                print(f"FAIL: Extension '{ext_name}' is NOT installed (expected after task)")
        except Exception as e:
            print(f"ERROR: Could not check extension '{ext_name}': {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
if not os.path.isdir(EXTENSIONS_DIR):
    print(f"CRITICAL: Chrome Extensions directory not found: {EXTENSIONS_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()

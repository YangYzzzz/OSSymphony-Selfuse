"""
Reward Script: Install Chrome extensions mentioned in Streaming_extensions.docx
Task ID: osworld_multi_apps_misc_009
Domain: chrome (multi-app: LibreOffice Writer + Chrome)
Scoring:
  - Component 1: Video Speed Controller extension installed (0.35 pts)
  - Component 2: Enhancer for YouTube extension installed (0.35 pts)
  - Component 3: Teleparty extension installed (0.30 pts)
  Total: 1.0

The task requires the agent to open 'Streaming_extensions.docx' and install
all three streaming extensions listed in it:
  1. Video Speed Controller
  2. Enhancer for YouTube
  3. Netflix Party is now Teleparty (installed as 'Teleparty')

Verification strategy: Read manifest.json files from Chrome's Extensions directory
and check extension state in Preferences. Extensions installed from the Web Store
will have a manifest.json under ~/.config/google-chrome/Default/Extensions/<ext_id>/
and state=1 in Preferences settings.
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_009'

# Chrome extension IDs for the required extensions
EXTENSION_INFO = {
    'nffaoalbilbmmfgbnbgppjihopabppdk': {
        'name': 'Video Speed Controller',
        'keywords': ['video speed controller', 'video speed'],
        'score': 0.35,
    },
    'gcnceeflimggoamelclcbhcdggcmnglm': {
        'name': 'Enhancer for YouTube',
        'keywords': ['enhancer for youtube', 'enhancer for youtube™'],
        'score': 0.35,
    },
    'oocalimimngaihdkbihfgmpkcpnmlaoa': {
        'name': 'Teleparty',
        'keywords': ['teleparty', 'netflix party'],
        'score': 0.30,
    },
}


def get_installed_extensions_from_filesystem():
    """
    Read all extension names from manifest.json files in the Chrome Extensions directory.
    Returns a dict of {ext_id: name} for each installed extension.
    """
    chrome_default = os.path.expanduser('~/.config/google-chrome/Default')
    extensions_dir = os.path.join(chrome_default, 'Extensions')
    installed = {}

    if not os.path.isdir(extensions_dir):
        print(f"WARN: Extensions directory not found: {extensions_dir}")
        return installed

    for ext_id in os.listdir(extensions_dir):
        ext_path = os.path.join(extensions_dir, ext_id)
        if not os.path.isdir(ext_path):
            continue
        for version in os.listdir(ext_path):
            manifest_path = os.path.join(ext_path, version, 'manifest.json')
            if os.path.exists(manifest_path):
                try:
                    with open(manifest_path, 'r') as f:
                        data = json.load(f)
                    installed[ext_id] = data.get('name', '')
                except Exception as e:
                    installed[ext_id] = f'PARSE_ERROR: {e}'
    return installed


def get_extension_state_from_preferences(ext_id):
    """
    Read the extension state from Chrome Preferences file.
    Returns the state value (1 = enabled) or None if not found.
    """
    chrome_default = os.path.expanduser('~/.config/google-chrome/Default')
    prefs_file = os.path.join(chrome_default, 'Preferences')

    try:
        with open(prefs_file, 'r') as f:
            prefs = json.load(f)
        ext_settings = prefs.get('extensions', {}).get('settings', {})
        if ext_id in ext_settings:
            return ext_settings[ext_id].get('state', None)
        return None
    except Exception as e:
        print(f"WARN: Could not read Preferences: {e}")
        return None


def verify_task():
    """
    Verify that all three required Chrome extensions are installed.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Get all installed extensions from filesystem
    try:
        installed_extensions = get_installed_extensions_from_filesystem()
        print(f"INFO: Found {len(installed_extensions)} extensions installed")
        for ext_id, name in installed_extensions.items():
            print(f"  - {ext_id}: {name}")
    except Exception as e:
        print(f"CRITICAL: Cannot read extensions directory: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Video Speed Controller (0.35 points)
    # Task says: install 'Video Speed Controller' extension
    # Extension ID: nffaoalbilbmmfgbnbgppjihopabppdk
    try:
        ext_id_vsc = 'nffaoalbilbmmfgbnbgppjihopabppdk'
        ext_name_vsc = EXTENSION_INFO[ext_id_vsc]['name']

        vsc_present = ext_id_vsc in installed_extensions
        vsc_state = get_extension_state_from_preferences(ext_id_vsc)
        vsc_enabled = (vsc_state == 1)

        if vsc_present and vsc_enabled:
            total_score += 0.35
            actual_name = installed_extensions.get(ext_id_vsc, '')
            print(f"PASS: Component 1 — '{ext_name_vsc}' extension installed and enabled "
                  f"(manifest name: '{actual_name}', state={vsc_state}) (0.35 pts)")
        elif vsc_present and not vsc_enabled:
            print(f"FAIL: Component 1 — '{ext_name_vsc}' extension files present but not enabled "
                  f"(state={vsc_state})")
        else:
            print(f"FAIL: Component 1 — '{ext_name_vsc}' extension not found in Extensions directory "
                  f"(expected ID: {ext_id_vsc})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Enhancer for YouTube (0.35 points)
    # Task says: install 'Enhancer for YouTube' extension
    # Extension ID: gcnceeflimggoamelclcbhcdggcmnglm
    try:
        ext_id_ey = 'gcnceeflimggoamelclcbhcdggcmnglm'
        ext_name_ey = EXTENSION_INFO[ext_id_ey]['name']

        ey_present = ext_id_ey in installed_extensions
        ey_state = get_extension_state_from_preferences(ext_id_ey)
        ey_enabled = (ey_state == 1)

        if ey_present and ey_enabled:
            total_score += 0.35
            actual_name = installed_extensions.get(ext_id_ey, '')
            print(f"PASS: Component 2 — '{ext_name_ey}' extension installed and enabled "
                  f"(manifest name: '{actual_name}', state={ey_state}) (0.35 pts)")
        elif ey_present and not ey_enabled:
            print(f"FAIL: Component 2 — '{ext_name_ey}' extension files present but not enabled "
                  f"(state={ey_state})")
        else:
            print(f"FAIL: Component 2 — '{ext_name_ey}' extension not found in Extensions directory "
                  f"(expected ID: {ext_id_ey})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Teleparty (0.30 points)
    # Task says: install 'Netflix Party is now Teleparty' extension
    # Extension ID: oocalimimngaihdkbihfgmpkcpnmlaoa
    try:
        ext_id_tp = 'oocalimimngaihdkbihfgmpkcpnmlaoa'
        ext_name_tp = EXTENSION_INFO[ext_id_tp]['name']

        tp_present = ext_id_tp in installed_extensions
        tp_state = get_extension_state_from_preferences(ext_id_tp)
        tp_enabled = (tp_state == 1)

        if tp_present and tp_enabled:
            total_score += 0.30
            actual_name = installed_extensions.get(ext_id_tp, '')
            print(f"PASS: Component 3 — '{ext_name_tp}' extension installed and enabled "
                  f"(manifest name: '{actual_name}', state={tp_state}) (0.30 pts)")
        elif tp_present and not tp_enabled:
            print(f"FAIL: Component 3 — '{ext_name_tp}' extension files present but not enabled "
                  f"(state={tp_state})")
        else:
            print(f"FAIL: Component 3 — '{ext_name_tp}' extension not found in Extensions directory "
                  f"(expected ID: {ext_id_tp})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

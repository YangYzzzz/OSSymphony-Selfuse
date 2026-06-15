"""
Reward Script: Install Chrome security extensions from Security_extensions.docx
Task ID: osworld_multi_apps_misc_010
Domain: chrome (multi-app)
Scoring:
  Component 1: uBlock Origin installed               — 0.2 points
  Component 2: Privacy Badger installed              — 0.2 points
  Component 3: HTTPS Everywhere installed            — 0.2 points
  Component 4: DuckDuckGo Privacy Essentials installed — 0.2 points
  Component 5: ClearURLs installed                   — 0.2 points
  Total: 1.0
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_010'

# Chrome extensions directory on Linux VM
CHROME_DEFAULT = os.path.join(WORKDIR, '.config', 'google-chrome', 'Default')
EXTENSIONS_DIR = os.path.join(CHROME_DEFAULT, 'Extensions')

# The five extensions that must be installed per the task document.
# Known extension IDs on this VM (identified from golden_env exploration):
#   uBlock Origin            -> cjpalhdlnbpafiamejdnhcphjbkeiagm
#   Privacy Badger           -> pkehgijcmpdhfbdbbnkijodmdjhbjlgp
#   HTTPS Everywhere         -> gcbommkclmclpchllfjekcdonpmejbdp
#   DuckDuckGo Privacy Essentials -> bkbkknnmegbbqmchmkfnbeknhkjkihai
#   ClearURLs                -> lckanjgmijmafbedldinpkdnmejbknbf

REQUIRED_EXTENSIONS = [
    {
        "name": "uBlock Origin",
        "id": "cjpalhdlnbpafiamejdnhcphjbkeiagm",
        "expected_name_fragments": ["ublock origin", "ublock"]
    },
    {
        "name": "Privacy Badger",
        "id": "pkehgijcmpdhfbdbbnkijodmdjhbjlgp",
        "expected_name_fragments": ["privacy badger"]
    },
    {
        "name": "HTTPS Everywhere",
        "id": "gcbommkclmclpchllfjekcdonpmejbdp",
        "expected_name_fragments": ["https everywhere"]
    },
    {
        "name": "DuckDuckGo Privacy Essentials",
        "id": "bkbkknnmegbbqmchmkfnbeknhkjkihai",
        "expected_name_fragments": ["duckduckgo privacy essentials", "duckduckgo"]
    },
    {
        "name": "ClearURLs",
        "id": "lckanjgmijmafbedldinpkdnmejbknbf",
        "expected_name_fragments": ["clearurls"]
    },
]


def get_installed_extension_names():
    """
    Enumerate all extensions in the Chrome Extensions directory and return
    a set of lowercased extension names from their manifest.json files.
    Also return a set of installed extension IDs.
    """
    names = set()
    ids = set()
    if not os.path.isdir(EXTENSIONS_DIR):
        return names, ids
    for ext_id in os.listdir(EXTENSIONS_DIR):
        ext_path = os.path.join(EXTENSIONS_DIR, ext_id)
        if not os.path.isdir(ext_path):
            continue
        ids.add(ext_id)
        for version in os.listdir(ext_path):
            manifest_path = os.path.join(ext_path, version, 'manifest.json')
            if os.path.exists(manifest_path):
                try:
                    with open(manifest_path, 'r') as f:
                        data = json.load(f)
                    ext_name = data.get('name', '')
                    names.add(ext_name.lower())
                except Exception:
                    pass
    return names, ids


def check_extension_installed(ext_info, installed_ids, installed_names):
    """
    Check whether a required extension is installed.
    Primary check: extension ID directory exists.
    Fallback check: manifest name matches expected name fragment.
    Returns True if installed, False otherwise.
    """
    # Primary: check by known extension ID
    if ext_info['id'] in installed_ids:
        return True

    # Fallback: check by manifest name (in case ID differs but same extension)
    for fragment in ext_info['expected_name_fragments']:
        for installed_name in installed_names:
            if fragment in installed_name:
                return True

    return False


def verify_task():
    """
    Verify that all five security extensions from Security_extensions.docx
    are installed in Chrome.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    POINTS_PER_EXTENSION = 0.2

    # Precondition: Extensions directory must exist
    if not os.path.isdir(EXTENSIONS_DIR):
        print(f"CRITICAL: Chrome Extensions directory not found: {EXTENSIONS_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Gather installed extensions once
    try:
        installed_names, installed_ids = get_installed_extension_names()
        print(f"INFO: Found {len(installed_ids)} extension directories: {installed_ids}")
        print(f"INFO: Extension names: {installed_names}")
    except Exception as e:
        print(f"CRITICAL: Cannot read extensions directory: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Score each required extension
    for i, ext_info in enumerate(REQUIRED_EXTENSIONS, start=1):
        try:
            is_installed = check_extension_installed(ext_info, installed_ids, installed_names)
            if is_installed:
                print(f"PASS: Component {i} — '{ext_info['name']}' is installed ({POINTS_PER_EXTENSION} pts)")
                total_score += POINTS_PER_EXTENSION
            else:
                print(f"FAIL: Component {i} — '{ext_info['name']}' is NOT installed (expected ID: {ext_info['id']})")
        except Exception as e:
            print(f"ERROR: Component {i} — Could not verify '{ext_info['name']}': {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: run verification on this VM
verify_task()

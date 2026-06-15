"""
FINAL REWARD SCRIPT - SUCCESS
Task: I keep missing build errors in my TypeScript project—could you help me install the “Error Lens” extension so the issues show up inline while I’m coding?
Generated: 2025-09-11 15:30:04
Status: success
Model: azure-o3
Total Steps: 18
"""

import os
import pathlib
import re
import subprocess
import shutil
import traceback

"""
Reward Script for the task:  *Install the VS Code extension “Error Lens” (publisher: usernamehw)*

The script verifies installation in two independent ways:
1. **Filesystem evidence (definitive – 1.0 pts)**
   A directory named   `usernamehw.errorlens-<version>`   must be present in one of the standard
   VS Code extension folders (local, insiders, remote-server, test, root, or XDG path).
2. **VS Code CLI evidence (strong – 0.8 pts)**
   The command  `code --list-extensions`  must list  `usernamehw.errorlens` .  If this is true
   but the folder cannot be found (e.g., remote container), partial credit (0.8) is awarded.

Scoring:
    • 1.0  – Extension folder found (task fully completed)
    • 0.8  – CLI lists extension but folder not located (very likely installed)
    • 0.0  – No evidence of installation

The script prints detailed diagnostics for transparency and ALWAYS outputs the final score as
"REWARD: <float>".
"""

# Constants ------------------------------------------------------------------
EXT_PUBLISHER = "usernamehw"
EXT_NAME      = "errorlens"
EXT_ID_REGEX  = rf"^{EXT_PUBLISHER}\\.{EXT_NAME}"          # used for CLI output
FOLDER_REGEX  = re.compile(rf"^{re.escape(EXT_PUBLISHER)}\\.{EXT_NAME}-.*", re.IGNORECASE)

# ----------------------------------------------------------------------------
# Helper: safe path existence (suppresses permission errors)
# ----------------------------------------------------------------------------

def safe_exists(path: pathlib.Path) -> bool:
    try:
        return path.exists()
    except PermissionError:
        print(f"⚠️  Permission denied accessing {path}")
        return False
    except Exception as e:
        print(f"⚠️  Error accessing {path}: {e}")
        return False

# ----------------------------------------------------------------------------
# Method 1: Filesystem verification
# ----------------------------------------------------------------------------

def check_via_filesystem() -> bool:
    """Return True if a folder matching the Error Lens extension exists."""
    home = pathlib.Path.home()

    candidate_dirs = [
        home / '.vscode' / 'extensions',
        home / '.vscode-insiders' / 'extensions',
        home / '.vscode-server' / 'extensions',
        home / '.vscode-server-insiders' / 'extensions',
        home / '.vscode-test' / 'extensions',
        home / '.vscode-test-insiders' / 'extensions',
    ]

    # XDG data path (e.g. ~/.local/share/Code/extensions)
    xdg_data_home = os.environ.get('XDG_DATA_HOME')
    if xdg_data_home:
        candidate_dirs.append(pathlib.Path(xdg_data_home) / 'Code' / 'extensions')

    # Possible root-user locations (guarded by safe_exists)
    candidate_dirs.extend([
        pathlib.Path('/root/.vscode/extensions'),
        pathlib.Path('/root/.vscode-server/extensions'),
    ])

    for ext_dir in candidate_dirs:
        if not safe_exists(ext_dir):
            continue
        try:
            for item in ext_dir.iterdir():
                if item.is_dir() and FOLDER_REGEX.match(item.name):
                    print(f"✅ Found Error Lens directory: {item}")
                    return True
        except PermissionError:
            print(f"⚠️  Permission denied listing {ext_dir}")
        except Exception as e:
            print(f"⚠️  Error scanning {ext_dir}: {e}")
    print("❌ No Error Lens directory found in known locations.")
    return False

# ----------------------------------------------------------------------------
# Method 2: VS Code CLI verification
# ----------------------------------------------------------------------------

def check_via_cli() -> bool:
    """Return True if `code --list-extensions` reports the extension."""
    code_bin = shutil.which('code')
    if not code_bin:
        print("⚠️  'code' CLI not found – skipping CLI check.")
        return False

    try:
        result = subprocess.run([code_bin, '--list-extensions'], capture_output=True, text=True, timeout=25)
    except Exception as e:
        print(f"⚠️  Failed to execute 'code --list-extensions': {e}")
        return False

    if result.returncode != 0:
        print(f"⚠️  'code --list-extensions' returned exit code {result.returncode}. stderr:\n{result.stderr}")
        return False

    extensions_listed = [line.strip().lower() for line in result.stdout.splitlines() if line.strip()]
    found = any(re.match(EXT_ID_REGEX, ext) for ext in extensions_listed)
    print(f"CLI check: total extensions = {len(extensions_listed)}. Error Lens present = {found}.")
    return found

# ----------------------------------------------------------------------------
# Main Verification & Scoring
# ----------------------------------------------------------------------------

def verify_task() -> float:
    filesystem_evidence = check_via_filesystem()   # definitive
    cli_evidence        = check_via_cli()          # supportive

    if filesystem_evidence:
        score = 1.0
    elif cli_evidence:
        score = 0.8
    else:
        score = 0.0

    print(f"Computed score = {score}/1.0")
    return score

# ----------------------------------------------------------------------------
# Script entry point
# ----------------------------------------------------------------------------

if __name__ == '__main__':
    reward = verify_task()
    print(f"REWARD: {reward}")


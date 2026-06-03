"""
Reward Script: Install the official Docker extension by Microsoft in VSCode
Task ID: vscode_ext_008
Domain: vs_code
Scoring:
  Component 1 (0.4): Docker extension directory exists in ~/.vscode/extensions/
  Component 2 (0.3): extensions.json contains entry with id 'ms-azuretools.vscode-docker'
  Component 3 (0.3): Extension package.json confirms publisher is 'ms-azuretools' (official Microsoft Docker ext)
"""

import os
import json
import glob

EXTENSIONS_DIR = '/home/user/.vscode/extensions'
EXTENSIONS_JSON = '/home/user/.vscode/extensions/extensions.json'
DOCKER_EXTENSION_ID = 'ms-azuretools.vscode-docker'

def verify_task():
    """
    Verify task completion with progressive scoring.
    Checks that the official Docker extension by Microsoft (ms-azuretools.vscode-docker)
    is installed in VSCode.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: extensions directory must exist
    if not os.path.isdir(EXTENSIONS_DIR):
        print(f"CRITICAL: Extensions directory not found: {EXTENSIONS_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Docker extension directory exists (0.4 points)
    # The extension is installed as a directory named ms-azuretools.vscode-docker-<version>
    try:
        pattern = os.path.join(EXTENSIONS_DIR, 'ms-azuretools.vscode-docker-*')
        matching_dirs = glob.glob(pattern)
        # Filter to only directories (not files)
        matching_dirs = [d for d in matching_dirs if os.path.isdir(d)]
        if matching_dirs:
            print(f"PASS: Component 1 — Docker extension directory found: {matching_dirs[0]} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No directory matching '{pattern}' found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: extensions.json contains entry with id 'ms-azuretools.vscode-docker' (0.3 points)
    # VSCode maintains a registry of installed extensions in extensions.json
    try:
        with open(EXTENSIONS_JSON, 'r') as f:
            extensions_list = json.load(f)

        docker_entry = None
        for entry in extensions_list:
            entry_id = entry.get('identifier', {}).get('id', '')
            if entry_id.lower() == DOCKER_EXTENSION_ID.lower():
                docker_entry = entry
                break

        if docker_entry is not None:
            entry_id = docker_entry.get('identifier', {}).get('id', '')
            print(f"PASS: Component 2 — extensions.json has entry with id '{entry_id}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — extensions.json does not contain entry with id '{DOCKER_EXTENSION_ID}'")
            print(f"      Current extensions.json entries: {[e.get('identifier', {}).get('id', '') for e in extensions_list]}")
    except FileNotFoundError:
        print(f"FAIL: Component 2 — extensions.json not found at {EXTENSIONS_JSON}")
    except json.JSONDecodeError as e:
        print(f"ERROR: Component 2 — Could not parse extensions.json: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Extension package.json confirms publisher is 'ms-azuretools' (official Microsoft Docker ext) (0.3 points)
    # This ensures the installed extension is the OFFICIAL Docker extension by Microsoft,
    # not a third-party or unofficial extension
    try:
        pattern = os.path.join(EXTENSIONS_DIR, 'ms-azuretools.vscode-docker-*')
        matching_dirs = [d for d in glob.glob(pattern) if os.path.isdir(d)]
        if not matching_dirs:
            print(f"FAIL: Component 3 — No Docker extension directory found to inspect package.json")
        else:
            pkg_json_path = os.path.join(matching_dirs[0], 'package.json')
            with open(pkg_json_path, 'r') as f:
                pkg_data = json.load(f)
            publisher = pkg_data.get('publisher', '')
            ext_name = pkg_data.get('name', '')
            version = pkg_data.get('version', 'unknown')
            # Official extension: publisher='ms-azuretools', name='vscode-docker'
            if publisher == 'ms-azuretools' and ext_name == 'vscode-docker':
                print(f"PASS: Component 3 — Official Microsoft Docker ext confirmed: publisher='{publisher}', name='{ext_name}', version='{version}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Got publisher='{publisher}', name='{ext_name}'; expected 'ms-azuretools'/'vscode-docker'")
    except FileNotFoundError as e:
        print(f"FAIL: Component 3 — package.json not found: {e}")
    except json.JSONDecodeError as e:
        print(f"ERROR: Component 3 — Could not parse package.json: {e}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()

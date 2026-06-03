"""
Reward Script: Install the C/C++ extension (ms-vscode.cpptools) in VSCode
Task ID: vscode_stu_027
Domain: vscode
Scoring:
  Component 1 (0.6 pts): Extension directory present in ~/.vscode/extensions/
  Component 2 (0.4 pts): Extension package.json exists and contains correct publisher/name
"""

import os
import json
import glob

HOME = os.path.expanduser("~")
EXTENSIONS_DIR = os.path.join(HOME, ".vscode", "extensions")
EXTENSION_ID = "ms-vscode.cpptools"  # publisher.name format
PUBLISHER = "ms-vscode"
NAME = "cpptools"


def verify_task():
    """
    Verify that the C/C++ extension (ms-vscode.cpptools) is installed in VSCode.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Extension directory exists in ~/.vscode/extensions/ (0.6 points)
    # The extension installs to a folder like ms-vscode.cpptools-<version>-linux-x64
    try:
        if not os.path.isdir(EXTENSIONS_DIR):
            print(f"FAIL: Component 1 -- Extensions directory does not exist: {EXTENSIONS_DIR}")
        else:
            ext_dirs = os.listdir(EXTENSIONS_DIR)
            matching_dirs = [d for d in ext_dirs if d.lower().startswith(EXTENSION_ID.lower())]
            if matching_dirs:
                print(f"PASS: Component 1 -- Found extension directory: {matching_dirs[0]} (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 1 -- No directory starting with '{EXTENSION_ID}' in {EXTENSIONS_DIR}")
                print(f"  Available dirs: {ext_dirs[:20]}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Extension package.json has correct identity (0.4 points)
    # Verify the extension metadata to ensure it's the real C/C++ extension
    try:
        # Find any directory starting with the extension ID
        if os.path.isdir(EXTENSIONS_DIR):
            ext_dirs = os.listdir(EXTENSIONS_DIR)
            matching_dirs = [d for d in ext_dirs if d.lower().startswith(EXTENSION_ID.lower())]
            if matching_dirs:
                pkg_json_path = os.path.join(EXTENSIONS_DIR, matching_dirs[0], "package.json")
                if os.path.isfile(pkg_json_path):
                    with open(pkg_json_path, "r") as f:
                        pkg = json.load(f)
                    pkg_name = pkg.get("name", "").lower()
                    pkg_publisher = pkg.get("publisher", "").lower()
                    if pkg_name == NAME.lower() and pkg_publisher == PUBLISHER.lower():
                        print(f"PASS: Component 2 -- package.json confirms publisher='{pkg_publisher}', name='{pkg_name}' (0.4 pts)")
                        total_score += 0.4
                    else:
                        print(f"FAIL: Component 2 -- package.json has publisher='{pkg_publisher}', name='{pkg_name}'; expected publisher='{PUBLISHER}', name='{NAME}'")
                else:
                    print(f"FAIL: Component 2 -- package.json not found at {pkg_json_path}")
            else:
                print(f"FAIL: Component 2 -- No matching extension directory found")
        else:
            print(f"FAIL: Component 2 -- Extensions directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()

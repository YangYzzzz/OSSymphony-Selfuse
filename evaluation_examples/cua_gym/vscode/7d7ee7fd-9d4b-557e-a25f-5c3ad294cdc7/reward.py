"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve wrapped up my web project and want to tidy up my editor—could you guide me on uninstalling the “Live Server” extension from VS Code?
Generated: 2025-09-11 13:31:27
Status: success
Model: azure-o3
Total Steps: 4
"""

import pathlib
import re


def verify_live_server_uninstalled():
    """Reward script to verify that the VS Code extension “Live Server”
    (identifier: ritwickdey.liveserver) has been uninstalled.

    The verification inspects the typical VS Code extension folders that can
    exist on a Linux system and awards a progressive score based on how many
    of those existing folders are free of the extension.
    """

    # Home directory
    home = pathlib.Path.home()

    # Potential extension directories (GUI VS Code, remote/server, snap install)
    dirs_to_check = [
        home / ".vscode" / "extensions",                 # Standard desktop VS Code
        home / ".vscode-server" / "extensions",          # VS Code Server / SSH / WSL
        home / "snap" / "code" / "current" / ".vscode" / "extensions",  # Snap package
    ]

    # Regex pattern for the Live Server extension directory names, e.g.
    # ritwickdey.liveserver-5.7.9
    ext_pattern = re.compile(r"^ritwickdey\.liveserver-.*", re.IGNORECASE)

    print("Starting verification of 'Live Server' uninstallation…")

    total_checks = 0   # Number of extension directories that actually exist
    success_checks = 0 # Number of those directories in which Live Server is absent

    for dir_path in dirs_to_check:
        print(f"Checking directory: {dir_path}")

        if not dir_path.exists():
            # Directory is absent → cannot contain the extension, but we exclude
            # it from scoring to avoid giving points for natural conditions.
            print("  ✱ Directory does not exist; skipping (does not affect score).")
            continue

        total_checks += 1
        found_live_server = []

        try:
            for item in dir_path.iterdir():
                if item.is_dir() and ext_pattern.match(item.name):
                    found_live_server.append(item.name)
        except Exception as e:
            # If we cannot read the directory, treat as failure for safety.
            print(f"  ✗ Error while scanning directory: {e}")
            continue

        if found_live_server:
            print(f"  ✗ Live Server extension FOUND: {found_live_server}")
        else:
            print("  ✓ Live Server extension NOT found in this directory.")
            success_checks += 1

    # Scoring logic ---------------------------------------------------------
    if total_checks == 0:
        # No VS Code extension folders exist at all; assume the extension is
        # not installed anywhere on this system, grant full credit.
        print("No VS Code extension directories detected. Assuming Live Server is not installed.")
        return 1.0

    score = success_checks / total_checks  # Progressive score (0.0 – 1.0)

    print(f"Verification summary: {success_checks}/{total_checks} directories free of Live Server.")
    print(f"Computed score: {score}")
    return score


if __name__ == "__main__":
    reward = verify_live_server_uninstalled()
    print(f"REWARD: {reward}")

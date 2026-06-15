"""
FINAL REWARD SCRIPT - SUCCESS
Task: While I’m focused on a large C++ refactor, the “Pylance” Python language server keeps hogging CPU in the background—could you show me how to temporarily turn that extension off until I’m back on Python work?
Generated: 2025-09-11 14:26:24
Status: success
Model: azure-o3
Total Steps: 11
"""

import subprocess
import pathlib
import re
import os


def verify_pylance_disabled():
    """Verify that the VS Code Pylance extension is *temporarily turned off*.

    The task asks the user to show how to disable the extension.  In the end-state
    we expect the extension **not** to be active (i.e. not listed by the CLI and
    no on-disk copy remaining in the standard extension locations).

    The check awards up to 1.0 points:
        • 0.7 pts – Pylance **not** listed in `code --list-extensions`
        • 0.3 pts – No Pylance extension directory exists in common paths

    Progressive scoring ensures partial credit if only one criterion is met.
    """

    max_score = 1.0
    total_score = 0.0
    print("Starting verification for Pylance disabled state…")

    # --------------------------------------------------------------
    # 1) Pylance NOT reported by `code --list-extensions`  (0.7 pts)
    # --------------------------------------------------------------
    try:
        output = subprocess.check_output(["code", "--list-extensions"], text=True)
        extensions = [line.strip() for line in output.split("\n") if line.strip()]
        print(f"Installed extensions ({len(extensions)}): {extensions}")

        if "ms-python.vscode-pylance" not in extensions:
            print("✓ Pylance extension is NOT listed in VS Code (0.7)")
            total_score += 0.7
        else:
            print("✗ Pylance extension is still listed in VS Code (0 points)")
    except FileNotFoundError:
        print("✗ VS Code CLI 'code' not found – cannot verify extensions (0 points)")
    except subprocess.CalledProcessError as exc:
        print(f"✗ Error executing `code --list-extensions`: {exc} (0 points)")

    # --------------------------------------------------------------
    # 2) No Pylance directory present in common extension paths (0.3)
    # --------------------------------------------------------------
    pylance_dirs = []
    candidate_roots = [
        pathlib.Path.home() / ".vscode/extensions",
        pathlib.Path.home() / ".vscode-server/extensions",
        pathlib.Path.home() / ".local/share/code/extensions",
        pathlib.Path.home() / ".config/Code/extensions",
    ]

    for root in candidate_roots:
        if root.exists():
            for sub in root.iterdir():
                if re.search(r"vscode[-.]pylance", sub.name, re.IGNORECASE):
                    pylance_dirs.append(sub)

    if not pylance_dirs:
        print("✓ No Pylance extension directories found (0.3)")
        total_score += 0.3
    else:
        print("✗ Pylance extension directories are still present:")
        for d in pylance_dirs:
            print("  -", d)

    # --------------------------------------------------------------
    # Final score & reporting
    # --------------------------------------------------------------
    final_score = round(min(total_score, max_score), 2)
    print(f"Total score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_pylance_disabled()

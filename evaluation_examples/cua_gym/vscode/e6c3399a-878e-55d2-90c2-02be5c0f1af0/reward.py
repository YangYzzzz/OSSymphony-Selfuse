"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve just cloned a data-science repo full of .ipynb files—could you help me install the official “Jupyter” extension so I can run and edit those notebooks directly in VS Code?
Generated: 2025-09-11 12:10:19
Status: success
Model: azure-o3
Total Steps: 9
"""

import subprocess


def verify_vscode_jupyter_extension():
    """
    Reward script to validate that the official VS Code Jupyter extension
    (ms-toolsai.jupyter) is installed.

    Progressive scoring
    -------------------
    1.0 – Official extension present
    0.6 – A different Jupyter-related extension present
    0.0 – No Jupyter extension found or VS Code CLI missing
    """

    # 1) Verify the VS Code CLI is available
    try:
        cli_proc = subprocess.run(
            ["code", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
        )
        if cli_proc.returncode != 0:
            print("✗ VS Code CLI returned non-zero exit code – cannot verify extensions")
            print("REWARD: 0.0")
            return 0.0
        else:
            print("✓ VS Code CLI detected – proceeding with extension verification …")
    except FileNotFoundError:
        print("✗ VS Code CLI (`code`) not found in PATH – cannot verify extensions")
        print("REWARD: 0.0")
        return 0.0
    except Exception as exc:
        print(f"✗ Unexpected error invoking VS Code CLI: {exc}")
        print("REWARD: 0.0")
        return 0.0

    # 2) Get the list of installed extensions
    try:
        list_proc = subprocess.run(
            ["code", "--list-extensions"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )
        if list_proc.returncode != 0:
            print("✗ Unable to list VS Code extensions – cannot proceed")
            print("REWARD: 0.0")
            return 0.0
    except Exception as exc:
        print(f"✗ Exception while listing extensions: {exc}")
        print("REWARD: 0.0")
        return 0.0

    extensions = [ext.strip().lower() for ext in list_proc.stdout.splitlines() if ext.strip()]
    print(f"Detected {len(extensions)} installed extension(s)")
    if extensions:
        print("First few extensions:", extensions[:20])

    # 3) Scoring logic based on actual findings
    if "ms-toolsai.jupyter" in extensions:
        print("✅ Official Jupyter extension (‘ms-toolsai.jupyter’) found – FULL credit")
        score = 1.0
    else:
        jupyter_related = any("jupyter" in ext for ext in extensions)
        if jupyter_related:
            print("⚠️ Jupyter-related extension present but not the official one – PARTIAL credit (0.6)")
            score = 0.6
        else:
            print("✗ No Jupyter extension detected – ZERO credit")
            score = 0.0

    print(f"REWARD: {score}")
    return score


if __name__ == "__main__":
    verify_vscode_jupyter_extension()

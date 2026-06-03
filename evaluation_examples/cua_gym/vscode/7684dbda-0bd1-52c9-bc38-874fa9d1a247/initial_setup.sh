#!/usr/bin/env bash
# File: ~/vscode_python_rollback_task/init_setup.sh
# Purpose:  Prepare a workspace where the **latest** Python extension is
#           installed so the user needs to roll it back to 2023.16.0.

set -euo pipefail

echo "-------------------------------------------------------------"
echo " VS Code Python-extension rollback – INITIAL STATE"
echo "-------------------------------------------------------------"

###############################################################################
# 1.  Workspace skeleton
###############################################################################
WORKSPACE="$HOME/vscode_python_rollback_task"
echo "Creating workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"

# A trivial Python file
cat > "$WORKSPACE/src/app.py" <<'EOF'
import sys
print(f"Python executable: {sys.executable}")
print("If the Python extension can't see the venv, downgrade it!")
EOF

###############################################################################
# 2.  OPTIONAL – create a venv to make the ‘missing-venv’ story believable
###############################################################################
if command -v python3 >/dev/null 2>&1; then
  echo "Creating virtual environment (.venv) ..."
  python3 -m venv "$WORKSPACE/.venv"
else
  echo "python3 not found – skipping virtual-environment creation."
fi

###############################################################################
# 3.  Install or upgrade to the LATEST Python extension
###############################################################################
# NOTE: Requires internet access. If the machine has no network, the install
#       will fail and the user will see the problem immediately.
echo "Installing / upgrading the Python extension to the newest version ..."
code --install-extension ms-python.python --force

###############################################################################
# 4.  Task instructions for the learner
###############################################################################
cat > "$WORKSPACE/.task_info.txt" <<'EOF'
TASK: The Python extension has been upgraded and no longer detects the local
virtual environment.  Roll the extension **back** to version 2023.16.0.

Hint (GUI):
1. Open the Extensions side-bar (⇧⌘X / Ctrl+Shift+X)
2. Locate “Python” by Microsoft
3. Click the ⚙️  (gear) → “Install Another Version…”
4. Select “2023.16.0” and reload VS Code

CLI alternative:
code --install-extension ms-python.python@2023.16.0 --force
EOF

###############################################################################
# 5.  Open VS Code so the user can start the exercise
###############################################################################
echo "Opening VS Code ..."
code "$WORKSPACE" &

###############################################################################
# 6.  Verification output (purely informational for the console)
###############################################################################
echo "Current Python extension version(s):"
code --list-extensions --show-versions | grep -E '^ms-python.python' || \
  echo "  (none installed)"

echo "Initial set-up complete – user must now DOWNGRADE the extension."
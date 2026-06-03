#!/usr/bin/env bash
###############################################################################
# File:   setup_initial_python_ruler_task.sh
# Purpose: Prepare a VS Code workspace that lacks the required 100-column
#          ruler for Python files. The user will later add it via VS Code.
###############################################################################
set -euo pipefail

echo ">>> Creating initial state for Python 100-column ruler task…"

# ---------------------------------------------------------------------------
# 1. Workspace location (chosen freely because the task gives no fixed path)
# ---------------------------------------------------------------------------
WORKSPACE="$HOME/vscode_python_ruler_task"

# Ensure a clean slate
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"
echo "Workspace folder created at: $WORKSPACE"

# ---------------------------------------------------------------------------
# 2. Sample Python file with >100-character line to make the issue obvious
# ---------------------------------------------------------------------------
cat > "$WORKSPACE/src/example.py" << 'EOF'
"""
This module intentionally contains lines longer than 100 characters so you can clearly
see where the vertical ruler should appear once you configure VS Code correctly.
"""

def very_long_function_name_with_plenty_of_parameters(param_one, param_two, param_three, param_four, param_five):
    print("This print statement is also intentionally long so that you can observe what happens once the 100-character ruler is enabled in your VS Code editor window!")
EOF
echo "Sample Python file with long lines created."

# ---------------------------------------------------------------------------
# 3. VS Code workspace settings WITHOUT the 100-column ruler
# ---------------------------------------------------------------------------
mkdir -p "$WORKSPACE/.vscode"
cat > "$WORKSPACE/.vscode/settings.json" << 'EOF'
{
  // Current workspace settings
  "editor.tabSize": 4,
  "files.autoSave": "off",
  "editor.wordWrap": "off",
  // Intentionally wrong ruler (set at 80) so the user must fix it
  "editor.rulers": [80]
}
EOF
echo "Initial .vscode/settings.json created WITHOUT the 100-column ruler."

# ---------------------------------------------------------------------------
# 4. Task marker for graders / users
# ---------------------------------------------------------------------------
cat > "$WORKSPACE/.task_info.txt" << 'EOF'
TASK: Add a vertical ruler at exactly 100 characters for ALL Python files.
SUGGESTION: Use language-specific settings:
{
  "[python]": {
    "editor.rulers": [100]
  }
}
EOF

# ---------------------------------------------------------------------------
# 5. Verification that initial state indeed lacks the correct ruler
# ---------------------------------------------------------------------------
if grep -q '"editor.rulers": \[100\]' "$WORKSPACE/.vscode/settings.json"; then
  echo "ERROR: A 100-column ruler is already present — this should be an initial state without it."
  exit 1
else
  echo "Verified: No 100-column ruler yet (expected)."
fi

# ---------------------------------------------------------------------------
# 6. Open VS Code
# ---------------------------------------------------------------------------
echo "Opening VS Code…"
code "$WORKSPACE" &>/dev/null &
sleep 2

echo ">>> Initial setup complete. VS Code is ready."
#!/usr/bin/env bash
# initial_setup_ruler_task.sh
#
# Prepares a VS Code workspace that is missing the 140-character ruler.
# The user’s job: add a 140-character ruler via VS Code’s Settings UI or
# by editing .vscode/settings.json.
#
# After running, VS Code opens the workspace so the user can perform
# the task.

set -euo pipefail

echo "========== VS Code Ruler Task – Initial Setup =========="

# ---------------------------------------------------------------------
# 1. Workspace creation
# ---------------------------------------------------------------------
WORKSPACE="$HOME/vscode_ruler_task"
echo "Using workspace: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src" "$WORKSPACE/.vscode"

# ---------------------------------------------------------------------
# 2. Populate realistic project content
# ---------------------------------------------------------------------
cat > "$WORKSPACE/src/main.py" << 'EOF'
def very_long_function_name(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8):
    print("This is a purposely very long line so that you can see where the 140-character ruler should appear in the editor window --------------------------")
EOF

# ---------------------------------------------------------------------
# 3. Create initial VS Code workspace settings (NO ruler yet)
# ---------------------------------------------------------------------
cat > "$WORKSPACE/.vscode/settings.json" << 'EOF'
{
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    "files.autoSave": "off"
}
EOF
echo "Initial settings.json created (no ruler configured)."

# ---------------------------------------------------------------------
# 4. Verification that the ruler is indeed missing
# ---------------------------------------------------------------------
if grep -q '"editor.rulers"' "$WORKSPACE/.vscode/settings.json"; then
    echo "ERROR: Ruler unexpectedly present in initial state!"
    exit 1
fi
echo "Verified: No 'editor.rulers' entry found."

# ---------------------------------------------------------------------
# 5. Task instruction marker (for automated graders / human hint)
# ---------------------------------------------------------------------
echo "Add \"editor.rulers\": [140] to .vscode/settings.json" \
  > "$WORKSPACE/README_TASK.txt"

# ---------------------------------------------------------------------
# 6. Open VS Code for the user
# ---------------------------------------------------------------------
echo "Opening VS Code..."
code "$WORKSPACE" &

echo "Initial setup complete – VS Code is ready for the user to add the 140-character ruler."
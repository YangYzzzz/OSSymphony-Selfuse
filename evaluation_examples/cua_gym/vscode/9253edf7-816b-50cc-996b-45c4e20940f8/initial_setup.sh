#!/usr/bin/env bash
set -euo pipefail
#
# Initial setup for the “Assign Ctrl+Shift+V to Markdown Preview” task
#

echo "===== VS Code Keybinding Task: Initial State ====="

###############################################################################
# 1. Prepare workspace content
###############################################################################
WORKSPACE="$HOME/vscode_markdown_preview_task"
README_FILE="$WORKSPACE/README.md"

echo "Creating fresh workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE"

cat > "$README_FILE" << 'EOF'
# Markdown Preview Task

This **README** is here so you can try out the *Markdown Preview* feature in VS Code.

1. Update this file.
2. Use the keyboard shortcut (to be configured) to open the preview instantly.
EOF
echo "README.md created."

###############################################################################
# 2. Create an initial keybindings.json WITHOUT the desired shortcut
###############################################################################
VSCODE_USER_DIR="$HOME/.config/Code/User"
KEYBIND_FILE="$VSCODE_USER_DIR/keybindings.json"

echo "Ensuring VS Code user configuration directory exists: $VSCODE_USER_DIR"
mkdir -p "$VSCODE_USER_DIR"

# Back up existing keybindings (if present)
if [[ -f "$KEYBIND_FILE" ]]; then
  cp "$KEYBIND_FILE" "${KEYBIND_FILE}.bak"
  echo "Existing keybindings.json backed up to ${KEYBIND_FILE}.bak"
fi

# Write a simple keybindings.json that does NOT include ctrl+shift+v
cat > "$KEYBIND_FILE" << 'EOF'
[
  {
    "key": "ctrl+alt+n",
    "command": "workbench.action.files.newUntitledFile"
  }
]
EOF
echo "Initial keybindings.json written WITHOUT Ctrl+Shift+V."

###############################################################################
# 3. Verification of initial state
###############################################################################
if grep -qi '"key": "ctrl+shift+v"' "$KEYBIND_FILE"; then
  echo "ERROR: Ctrl+Shift+V is already assigned – initial state invalid."
  exit 1
else
  echo "Verified: Ctrl+Shift+V NOT set yet (expected for initial state)."
fi

###############################################################################
# 4. Task reminder for the student
###############################################################################
echo "Assign Ctrl + Shift + V to Markdown preview (command: markdown.showPreview)" \
  > "$WORKSPACE/.task_info.txt"

###############################################################################
# 5. Launch VS Code
###############################################################################
echo "Opening VS Code…"
code "$WORKSPACE" &

echo "===== Initial setup complete. ====="
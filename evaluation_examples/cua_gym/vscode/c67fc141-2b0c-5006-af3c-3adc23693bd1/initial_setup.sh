#!/usr/bin/env bash
# File: setup_initial.sh
# Purpose: Prepare VS Code so that **all extension auto-updates are disabled**.
# The user’s job will be to turn them back on.
# ---------------------------------------------
set -euo pipefail

echo "========== VS Code Extension Auto-Update Task – Initial State =========="

# 1. Create a tiny workspace so VS Code opens somewhere meaningful
WORKSPACE="$HOME/vscode_extension_update_task"
echo "Creating workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE"

# 2. Prepare a simple README so something shows in Explorer
cat > "$WORKSPACE/README.md" <<'EOF'
# Extension Auto-Update Task

Your goal: turn on automatic updates for every extension you have installed in VS Code.
Hint: open the Settings UI (File → Preferences → Settings) or edit settings.json directly.
EOF

# 3. Ensure the VS Code user settings directory exists
VSCODE_USER_DIR="$HOME/.config/Code/User"
mkdir -p "$VSCODE_USER_DIR"
SETTINGS_FILE="$VSCODE_USER_DIR/settings.json"

# 4. Create/overwrite settings.json with auto-updates **disabled**
cat > "$SETTINGS_FILE" <<'EOF'
{
  // ---- EXISTING USER SETTINGS ----
  "workbench.colorTheme": "Default Dark+",
  "editor.fontSize": 14,

  // ---- EXTENSION UPDATES ----
  "extensions.autoUpdate": false,
  "extensions.autoCheckUpdates": false
}
EOF

echo "Created user settings with extensions.autoUpdate = false"

# 5. Verification of initial state
if grep -q '"extensions.autoUpdate": false' "$SETTINGS_FILE"; then
    echo "Verified: Auto-update is currently OFF"
else
    echo "ERROR: Initial settings not applied correctly" >&2
    exit 1
fi

# 6. Drop an in-editor task hint file
echo "Turn ON \"Extensions: Auto Update\" for all extensions." \
     > "$WORKSPACE/.task_info.txt"

# 7. Launch VS Code pointed at the workspace
echo "Opening VS Code…"
code "$WORKSPACE" &

echo "======================================================================="
echo "Initial environment ready.  The user must now enable auto-updates."
#!/usr/bin/env bash
# ============================================================
# VS Code Theme Task – Initial Setup
# ------------------------------------------------------------
# Prepares a workspace where the current color theme is NOT
# “Solarized Light”.  The user’s task will be to switch the
# theme to “Solarized Light” through the VS Code interface.
# ============================================================

set -euo pipefail

echo "============= VS CODE THEME TASK – INITIAL SETUP ============="

# -----------------------------------------------------------------
# 1. Define paths
# -----------------------------------------------------------------
# Location of VS Code user-level settings (Linux/macOS default)
VSCODE_USER_DIR="$HOME/.config/Code/User"
SETTINGS_FILE="$VSCODE_USER_DIR/settings.json"

# Workspace that will be opened in VS Code
WORKSPACE="$HOME/vscode_theme_task"
mkdir -p "$WORKSPACE"

# -----------------------------------------------------------------
# 2. Ensure settings directory exists
# -----------------------------------------------------------------
mkdir -p "$VSCODE_USER_DIR"

# -----------------------------------------------------------------
# 3. Create an initial settings.json that **does not** use
#    “Solarized Light”.  We’ll pick a popular dark theme instead.
#    Any existing settings.json is backed up.
# -----------------------------------------------------------------
if [[ -f "$SETTINGS_FILE" ]]; then
    cp "$SETTINGS_FILE" "${SETTINGS_FILE}.bak.$(date +%s)"
    echo "Backed up existing settings.json → ${SETTINGS_FILE}.bak.*"
fi

cat > "$SETTINGS_FILE" << 'EOF'
{
  "workbench.colorTheme": "GitHub Dark Default",
  "editor.fontSize": 14,
  "files.autoSave": "off"
}
EOF

echo "Initial theme set to: GitHub Dark Default"

# -----------------------------------------------------------------
# 4. Verification – confirm theme is NOT “Solarized Light”
# -----------------------------------------------------------------
if grep -q '"workbench.colorTheme": "Solarized Light"' "$SETTINGS_FILE"; then
  echo "ERROR: Theme was already Solarized Light!"
  exit 1
fi
echo "Verified theme is NOT Solarized Light ✅"

# -----------------------------------------------------------------
# 5. Provide task instruction inside the workspace
# -----------------------------------------------------------------
cat > "$WORKSPACE/README_TASK.md" << 'EOF'
# VS Code Theme Task

The room is too bright – please switch VS Code to the **“Solarized Light”** color theme.
EOF

# -----------------------------------------------------------------
# 6. Launch VS Code so the user can perform the task
# -----------------------------------------------------------------
echo "Opening VS Code…"
code "$WORKSPACE" &
sleep 2   # Give VS Code a moment to start

echo "Initial setup complete.  Your task: Change the color theme to “Solarized Light”."
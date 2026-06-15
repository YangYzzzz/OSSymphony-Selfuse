#!/usr/bin/env bash
# Purpose : Prepare a VS Code environment that is currently using a BRIGHT theme.
#           The ensuing task for the learner is to switch the theme to “Dracula”.

set -euo pipefail

echo "=============================================="
echo " VS Code Theme Task – Initial Setup           "
echo "=============================================="

# 1. Paths --------------------------------------------------------------------
VSCODE_USER_DIR="$HOME/.config/Code/User"
SETTINGS_JSON="$VSCODE_USER_DIR/settings.json"

WORKSPACE_DIR="$HOME/vscode_dracula_theme_task"
TASK_INFO_FILE="$WORKSPACE_DIR/.task_info.txt"

# 2. Create directories -------------------------------------------------------
mkdir -p "$VSCODE_USER_DIR"
rm -rf  "$WORKSPACE_DIR"
mkdir -p "$WORKSPACE_DIR"

# 3. Configure a bright theme -------------------------------------------------
BRIGHT_THEME="Default Light+"

if command -v jq >/dev/null 2>&1 && [ -f "$SETTINGS_JSON" ]; then
    # If a settings.json already exists, force-set a bright theme
    tmp="$(mktemp)"
    jq --arg theme "$BRIGHT_THEME" '.["workbench.colorTheme"] = $theme' \
        "$SETTINGS_JSON" > "$tmp"
    mv "$tmp" "$SETTINGS_JSON"
else
    # Either jq not present or no settings.json yet → write minimal file
    cat > "$SETTINGS_JSON" <<EOF
{
  "workbench.colorTheme": "$BRIGHT_THEME"
}
EOF
fi

echo "Initial VS Code theme set to \"$BRIGHT_THEME\" at: $SETTINGS_JSON"

# 4. Create a dummy project file ----------------------------------------------
echo -e "# Dracula Theme Task Workspace\n\nThis is a sample README." \
  > "$WORKSPACE_DIR/README.md"

# 5. Task instruction marker --------------------------------------------------
echo "Change VS Code theme to: Dracula" > "$TASK_INFO_FILE"

# 6. Verification output ------------------------------------------------------
CURRENT_THEME=$(grep -oP '"workbench.colorTheme":\s*"\K[^"]+' "$SETTINGS_JSON" || true)
echo "Current theme is: ${CURRENT_THEME:-<not-set>}"
if [ "$CURRENT_THEME" = "Dracula" ]; then
    echo "Warning: Theme already set to Dracula. Resetting to bright theme."
fi

# 7. Launch VS Code -----------------------------------------------------------
echo "Opening VS Code workspace. Please switch the theme to \"Dracula\"."
code "$WORKSPACE_DIR" &

echo "Initial setup complete."
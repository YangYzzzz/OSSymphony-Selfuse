#!/usr/bin/env bash
# material_theme_initial.sh
# Purpose: Prepare a workspace where VS Code is using a non-Material theme,
#          prompting the user to switch to “Material Theme”.
set -euo pipefail

echo "==============================================================="
echo "VS Code – Material Theme CHANGE TASK (INITIAL STATE)"
echo "==============================================================="

# -----------------------------------------------------------------
# 1. Locate VS Code user settings directory (Linux/macOS default)
# -----------------------------------------------------------------
VSCODE_USER_DIR="${HOME}/.config/Code/User"
mkdir -p "${VSCODE_USER_DIR}"
SETTINGS_FILE="${VSCODE_USER_DIR}/settings.json"

# -----------------------------------------------------------------
# 2. Create / overwrite settings.json with a bright default theme
# -----------------------------------------------------------------
cat > "${SETTINGS_FILE}" << 'EOF'
{
  // Theme intentionally set to something bright so the user
  // immediately notices the change requirement.
  "workbench.colorTheme": "Default Light+",
  "editor.fontSize": 14,
  "files.autoSave": "off"
}
EOF
echo "✓ VS Code settings initialised: Default Light+ theme in place."

# -----------------------------------------------------------------
# 3. Prepare a small sample workspace
# -----------------------------------------------------------------
WORKSPACE="${HOME}/vscode_material_theme_task"
rm -rf "${WORKSPACE}"
mkdir -p "${WORKSPACE}/src"

echo "# Material Theme Task"                >  "${WORKSPACE}/README.md"
echo "console.log('Theme task');"          >  "${WORKSPACE}/src/app.js"

# Helpful marker file so the learner sees the objective.
echo "Switch VS Code theme to 'Material Theme'." \
    > "${WORKSPACE}/.task_info.txt"

echo "✓ Sample workspace created at: ${WORKSPACE}"

# -----------------------------------------------------------------
# 4. Verification of current theme
# -----------------------------------------------------------------
echo -n "Current configured theme: "
if command -v jq >/dev/null 2>&1; then
    jq -r '.["workbench.colorTheme"]' "${SETTINGS_FILE}"
else
    # Fallback (grep) if jq is unavailable
    grep -o '"workbench.colorTheme"[[:space:]]*:[[:space:]]*"[^"]*"' "${SETTINGS_FILE}"
fi

# -----------------------------------------------------------------
# 5. Launch VS Code for the learner
# -----------------------------------------------------------------
echo "Opening VS Code…"
code "${WORKSPACE}" &

echo "---------------------------------------------------------------"
echo "TASK: In VS Code, open the Command Palette (Ctrl+Shift+P), run"
echo "'Preferences: Color Theme', and pick “Material Theme”."
echo "---------------------------------------------------------------"
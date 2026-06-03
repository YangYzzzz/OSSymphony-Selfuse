#!/usr/bin/env bash
# Purpose : Prepare VS Code environment where Auto-Save is OFF
# Task     : The learner must enable `"files.autoSave": "afterDelay"`
#            with `"files.autoSaveDelay": 2000`
# Author   : VS-Code Automation Specialist

set -euo pipefail

echo "========== VS Code Auto-Save TASK : Initial Setup =========="

# ------------------------------------------------------------------
# 1) Define paths
# ------------------------------------------------------------------
WORKSPACE="$HOME/vscode_autosave_task"
VSCODE_USER_DIR="$HOME/.config/Code/User"
SETTINGS_FILE="$VSCODE_USER_DIR/settings.json"

# ------------------------------------------------------------------
# 2) Create clean workspace with a few files to edit
# ------------------------------------------------------------------
echo "Creating workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"

cat > "$WORKSPACE/README.md" <<'EOF'
# Auto-Save Practice Workspace
Edit any file, then enable Auto-Save with a 2-second delay so you never lose work!
EOF

cat > "$WORKSPACE/src/example.py" <<'EOF'
def greet(name):
    print(f"Hello, {name}!")

greet("VS Code User")
EOF

# ------------------------------------------------------------------
# 3) Ensure USER settings exist & set Auto-Save OFF
# ------------------------------------------------------------------
echo "Configuring user settings: $SETTINGS_FILE"
mkdir -p "$VSCODE_USER_DIR"

# If a settings.json exists, back it up once (non-destructive)
if [ -f "$SETTINGS_FILE" ] && [ ! -f "${SETTINGS_FILE}.bak_autosave_task" ]; then
    cp "$SETTINGS_FILE" "${SETTINGS_FILE}.bak_autosave_task"
    echo "Existing settings backed-up to ${SETTINGS_FILE}.bak_autosave_task"
fi

# Create minimal settings with Auto-Save disabled
cat > "$SETTINGS_FILE" <<'EOF'
{
  "files.autoSave": "off",
  "editor.fontSize": 16
}
EOF

# ------------------------------------------------------------------
# 4) Verification – make sure Auto-Save really is OFF
# ------------------------------------------------------------------
echo "Verifying initial state ..."
if command -v jq >/dev/null 2>&1; then
    autosave_state=$(jq -r '."files.autoSave"' "$SETTINGS_FILE")
    if [[ "$autosave_state" != "off" ]]; then
        echo "ERROR: Expected files.autoSave to be 'off', found '$autosave_state'"
        exit 1
    fi
else
    # Fallback: simple grep check
    grep -q '"files.autoSave": "off"' "$SETTINGS_FILE"
fi
echo "Initial verification PASSED (Auto-Save is OFF)"

# ------------------------------------------------------------------
# 5) Task info hint
# ------------------------------------------------------------------
echo "Turn ON Auto-Save afterDelay with 2-second delay" > "$WORKSPACE/.task_info.txt"

# ------------------------------------------------------------------
# 6) Open VS Code
# ------------------------------------------------------------------
echo "Opening VS Code now – perform the task!"
code "$WORKSPACE" &

echo "========== Initial setup complete =========="
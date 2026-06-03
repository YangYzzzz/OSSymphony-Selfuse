#!/usr/bin/env bash
# ================================================================
# initial_setup.sh
# Prepares a workspace where the minimap is still enabled.
# ================================================================
set -euo pipefail

echo "──────────────────────────────────────────────"
echo "VS Code Minimap Disable – INITIAL STATE SETUP"
echo "──────────────────────────────────────────────"

# ----------------------------------------------------------------
# 1. Workspace skeleton
# ----------------------------------------------------------------
WORKSPACE="$HOME/vscode_minimap_task"
echo "Creating fresh workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/.vscode"

# ----------------------------------------------------------------
# 2. Sample large files to show the minimap distraction
# ----------------------------------------------------------------
python_file="$WORKSPACE/big_script.py"
ts_file="$WORKSPACE/big_module.ts"

yes "print('line')"           | head -n 400 > "$python_file"
yes "console.log('line');"    | head -n 400 > "$ts_file"

# ----------------------------------------------------------------
# 3. Workspace settings – minimap is ON
# ----------------------------------------------------------------
cat > "$WORKSPACE/.vscode/settings.json" <<'EOF'
{
  "editor.minimap.enabled": true,
  "files.autoSave": "off",
  "editor.fontSize": 14
}
EOF

# ----------------------------------------------------------------
# 4. Small task description for the learner
# ----------------------------------------------------------------
cat > "$WORKSPACE/TASK.md" <<'EOF'
# Disable the Minimap
Open .vscode/settings.json in this workspace and change:

    "editor.minimap.enabled": false

Save the file. The minimap on the right should disappear immediately.
EOF

# ----------------------------------------------------------------
# 5. Verification of current state (should be true)
# ----------------------------------------------------------------
echo -n "Current minimap setting: "
if command -v jq >/dev/null 2>&1; then
    jq '.["editor.minimap.enabled"]' "$WORKSPACE/.vscode/settings.json"
else
    grep -o '"editor.minimap.enabled":[^,]*' "$WORKSPACE/.vscode/settings.json"
fi

# ----------------------------------------------------------------
# 6. Open VS Code
# ----------------------------------------------------------------
echo "Opening VS Code…"
code "$WORKSPACE" &>/dev/null &

echo "Initial setup complete – minimap is currently ENABLED."
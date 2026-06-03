#!/usr/bin/env bash
# PURPOSE  : Re-create the annoying Workspace-Trust banner scenario
#            so the user can learn to disable it globally.
# CREATES  : - A demo repo at /home/work/mixed-stack   (fallback: $HOME/work/mixed-stack)
#           - A user-level settings.json **without** `"security.workspace.trust.enabled": false`
# OPENS    : VS Code pointed at the repo (banner should appear)
# ----------

set -euo pipefail

echo "🛠  Preparing initial Workspace-Trust task environment …"

########## 1) Resolve VS Code user-settings location ###########################
if [[ "$OSTYPE" == "darwin"* ]]; then
    VSCODE_USER_DIR="$HOME/Library/Application Support/Code/User"
else
    VSCODE_USER_DIR="$HOME/.config/Code/User"
fi
mkdir -p "$VSCODE_USER_DIR"
SETTINGS_FILE="$VSCODE_USER_DIR/settings.json"

########## 2) Backup any existing user settings ###############################
if [[ -f "$SETTINGS_FILE" ]]; then
    cp "$SETTINGS_FILE" "${SETTINGS_FILE}.pre_workspace_trust_task.bak"
    echo "🔒  Existing settings backed up to ${SETTINGS_FILE}.pre_workspace_trust_task.bak"
fi

########## 3) Create a settings.json that WILL trigger the banner #############
# We force `"security.workspace.trust.enabled": true` (or leave it absent)
cat > "$SETTINGS_FILE" <<'EOF'
{
  // VS Code Workspace-Trust task – initial state (banner should show up)
  "editor.fontSize": 14,
  "security.workspace.trust.untrustedFiles": "prompt",
  "security.workspace.trust.enabled": true
}
EOF
echo "✅  settings.json written WITHOUT disabling Workspace Trust."

########## 4) Create a realistic repo that user will open #####################
# We try to create at /home/work/mixed-stack; if we lack permission, fall back.
TARGET_ROOT="/home/work"
if ! mkdir -p "$TARGET_ROOT" 2>/dev/null; then
    TARGET_ROOT="$HOME/work"
    mkdir -p "$TARGET_ROOT"
    echo "⚠️  /home/work not writable – using $TARGET_ROOT instead."
fi
WORKSPACE="$TARGET_ROOT/mixed-stack"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src" "$WORKSPACE/backend" "$WORKSPACE/.vscode"

# Sample files
echo "console.log('Hello from the frontend');" > "$WORKSPACE/src/app.js"
echo -e "def api():\n    return {'msg': 'hi'}" > "$WORKSPACE/backend/api.py"
echo "# Mixed-Stack Demo Repo" > "$WORKSPACE/README.md"

echo "📂  Demo repository created at: $WORKSPACE"

########## 5) Verification – property should NOT be 'false' ###################
if command -v jq >/dev/null 2>&1; then
    if jq -e '.["security.workspace.trust.enabled"] == false' "$SETTINGS_FILE" > /dev/null; then
        echo "❌  settings.json already disables Workspace Trust – aborting."
        exit 1
    fi
fi
echo "🔍  Verification passed – Workspace Trust still ENABLED."

########## 6) Launch VS Code ##################################################
echo "🚀  Launching VS Code … (Banner should appear on top)"
code "$WORKSPACE" &> /dev/null &
sleep 2   # give VS Code a moment to start

echo "📝  TASK: Open Settings (Ctrl+,) ➜ search for 'workspace trust' ➜"
echo "       set **Security › Workspace › Trust: Enabled** to ‘false’"
echo "----------------------------------------------------------------"
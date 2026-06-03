#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# VS Code Auto-Save Task – Golden State
# Applies the expected configuration: auto-save enabled with 1000 ms delay.
###############################################################################

echo "✨  Applying golden configuration ..."

WORKSPACE="$HOME/ts_autosave_task"
VSCODE_USER_DIR="$HOME/.config/Code/User"
SETTINGS_FILE="$VSCODE_USER_DIR/settings.json"

# Safety check
if [[ ! -d "$WORKSPACE" ]]; then
    echo "❌  Workspace not found: $WORKSPACE" >&2
    exit 1
fi

mkdir -p "$VSCODE_USER_DIR"
[[ -f "$SETTINGS_FILE" ]] || echo "{}" > "$SETTINGS_FILE"

# ---------------------------------------------------------------------------
# 1. Update settings: afterDelay + 1000 ms
# ---------------------------------------------------------------------------
if command -v jq >/dev/null 2>&1; then
    tmp="$(mktemp)"
    jq '.["files.autoSave"]="afterDelay" | .["files.autoSaveDelay"]=1000' \
       "$SETTINGS_FILE" > "$tmp"
    mv "$tmp" "$SETTINGS_FILE"
else
    # Manual overwrite if jq missing
    cat > "$SETTINGS_FILE" <<'EOF'
{
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000
}
EOF
fi

# ---------------------------------------------------------------------------
# 2. Verification of final state
# ---------------------------------------------------------------------------
if grep -q '"files.autoSave": "afterDelay"' "$SETTINGS_FILE" \
   && grep -q '"files.autoSaveDelay": 1000' "$SETTINGS_FILE"; then
    echo "✅  Verified: auto-save set to afterDelay with 1000 ms delay."
else
    echo "❌  Auto-save settings not correctly applied." >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# 3. Launch VS Code to showcase the completed task
# ---------------------------------------------------------------------------
echo "🚀  Opening VS Code with golden configuration applied."
code "$WORKSPACE" &
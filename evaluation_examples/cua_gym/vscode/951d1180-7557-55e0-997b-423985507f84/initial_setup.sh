#!/usr/bin/env bash
# ❷  Golden Setup Script: Completed state (vertical ruler at 85)
set -euo pipefail

echo "========== VS Code Ruler Task: Golden Setup =========="

WORKSPACE="$HOME/vscode_ruler_task"
SETTINGS_FILE="$WORKSPACE/.vscode/settings.json"

# -----------------------------------------------------------------
# 1. Ensure workspace exists
# -----------------------------------------------------------------
if [ ! -f "$SETTINGS_FILE" ]; then
    echo "ERROR: Workspace not found. Run the initial setup script first." >&2
    exit 1
fi

# -----------------------------------------------------------------
# 2. Add 'editor.rulers': [85] to settings.json
#    • Use jq if available for safe JSON manipulation
#    • Fallback: write full file manually
# -----------------------------------------------------------------
if command -v jq >/dev/null 2>&1; then
    echo "Adding vertical ruler using jq..."
    tmp="$(mktemp)"
    # If editor.rulers already exists, merge 85; otherwise add new array
    if jq 'has("editor.rulers")' "$SETTINGS_FILE" | grep -q true; then
        jq '.["editor.rulers"] |= (if type=="array" then (. + [85] | unique) else [85] end)' \
           "$SETTINGS_FILE" > "$tmp"
    else
        jq '. + {"editor.rulers":[85]}' "$SETTINGS_FILE" > "$tmp"
    fi
    mv "$tmp" "$SETTINGS_FILE"
else
    echo "jq not found; writing settings.json manually..."
    cat > "$SETTINGS_FILE" << 'EOF'
{
    "editor.tabSize": 4,
    "editor.wordWrap": "off",
    "files.autoSave": "afterDelay",
    "editor.rulers": [85]
}
EOF
fi

echo "Vertical ruler at column 85 has been configured."

# -----------------------------------------------------------------
# 3. Verification – confirm 85 is present
# -----------------------------------------------------------------
if command -v jq >/dev/null 2>&1; then
    if jq '.["editor.rulers"] | index(85)' "$SETTINGS_FILE" | grep -q null; then
        echo "ERROR: 85 not found in editor.rulers – configuration failed" >&2
        exit 1
    fi
    echo "Verified: editor.rulers now contains 85."
else
    echo "(jq not found; manual verification may be required)"
fi

# -----------------------------------------------------------------
# 4. Open VS Code to show completed state
# -----------------------------------------------------------------
echo "Opening VS Code with completed configuration..."
code "$WORKSPACE" &

echo "Golden setup complete.  You should see a vertical guideline at column 85."
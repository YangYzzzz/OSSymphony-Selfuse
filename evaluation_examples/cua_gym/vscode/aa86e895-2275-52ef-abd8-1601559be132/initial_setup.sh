#!/usr/bin/env bash
###############################################################################
# initial_setup.sh – Prepare workspace where the built-in HTML formatter
#                    is still enabled so it will clash with Prettier.
###############################################################################
set -euo pipefail

echo "⏳  Preparing VS Code HTML-formatter task (initial state)…"

# ------------------------------------------------------------------
# 1. Workspace skeleton
# ------------------------------------------------------------------
WORKSPACE="$HOME/vscode_html_formatter_task"
rm -rf  "$WORKSPACE"                 # start fresh every time
mkdir -p "$WORKSPACE/.vscode"

# ------------------------------------------------------------------
# 2. Sample (poorly-formatted) HTML file
# ------------------------------------------------------------------
cat > "$WORKSPACE/index.html" <<'EOF'
<!DOCTYPE html><html><head><title>Formatter Clash</title></head><body><h1>Formatter Clash Example</h1><p>This file is intentionally badly formatted.</p></body></html>
EOF

# ------------------------------------------------------------------
# 3. VS Code workspace settings –
#    • Prettier is the default formatter
#    • Built-in HTML formatter is STILL ENABLED  -> conflict
# ------------------------------------------------------------------
cat > "$WORKSPACE/.vscode/settings.json" <<'EOF'
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "html.format.enable": true
}
EOF

# ------------------------------------------------------------------
# 4. Extension recommendation (helps VS Code suggest Prettier)
# ------------------------------------------------------------------
cat > "$WORKSPACE/.vscode/extensions.json" <<'EOF'
{
  "recommendations": [
    "esbenp.prettier-vscode"
  ]
}
EOF

# ------------------------------------------------------------------
# 5. Verification of initial state
# ------------------------------------------------------------------
echo "🔍  Verifying that built-in formatter is ON…"
if command -v jq >/dev/null 2>&1; then
    jq -e '.["html.format.enable"] == true' "$WORKSPACE/.vscode/settings.json" \
      >/dev/null && echo "✅  html.format.enable = true (as expected)"
else
    grep -q '"html.format.enable": *true' "$WORKSPACE/.vscode/settings.json" \
      && echo "✅  html.format.enable = true (as expected)"
fi

echo "📋  TASK for the user:"
echo "     Disable the built-in HTML formatter:"
echo "     → Set \"html.format.enable\": false      (workspace or user level)"
echo

# ------------------------------------------------------------------
# 6. Open VS Code
# ------------------------------------------------------------------
code "$WORKSPACE" &                   # launches VS Code in background
echo "🚀  VS Code opened with workspace: $WORKSPACE"
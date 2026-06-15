#!/usr/bin/env bash
# ------------------------------------------------------------------
# Initial Setup – HTML Doctype Insertion Task
# ------------------------------------------------------------------
set -euo pipefail

echo "=== VS Code HTML Doctype Task • Initial Setup ==="

# ---------- 1.  Workspace ----------------------------------------------------
WORKSPACE="$HOME/vscode_html_task"
echo "[info] Creating fresh workspace: $WORKSPACE"
rm -rf  "$WORKSPACE"
mkdir -p "$WORKSPACE/public"

# ---------- 2.  Project Content ---------------------------------------------
cat > "$WORKSPACE/public/index.html" <<'EOF'
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Doctype Task</title>
</head>
<body>
  <h1>Hi there 👋</h1>
  <p>You need to add the DOCTYPE!</p>
</body>
</html>
EOF

echo "[info] index.html created WITHOUT <!DOCTYPE html>"

# ---------- 3.  Workspace Recommendations (Live Server) ----------------------
mkdir -p "$WORKSPACE/.vscode"
cat > "$WORKSPACE/.vscode/extensions.json" <<'EOF'
{
  "recommendations": ["ritwickdey.LiveServer"]
}
EOF

# ---------- 4.  Ensure files.autoSave is disabled ----------------------------
USER_VSCODE_DIR="$HOME/.config/Code/User"
SETTINGS_FILE="$USER_VSCODE_DIR/settings.json"
mkdir -p "$USER_VSCODE_DIR"

# create file if it doesn't exist yet
if [[ ! -f "$SETTINGS_FILE" ]]; then
  echo "{}" > "$SETTINGS_FILE"
fi

# turn off auto-save (keep any existing settings intact)
if command -v jq >/dev/null 2>&1; then
  tmp="$(mktemp)"
  jq '. + {"files.autoSave":"off"}' "$SETTINGS_FILE" > "$tmp"
  mv "$tmp" "$SETTINGS_FILE"
else
  # naïve append when jq not available
  grep -q '"files.autoSave"' "$SETTINGS_FILE" 2>/dev/null \
    || sed -i '1s;^;{\n  "files.autoSave": "off"\n};' "$SETTINGS_FILE"
fi
echo "[info] VS Code user setting files.autoSave set to off"

# ---------- 5.  Verification -------------------------------------------------
if grep -q "<!DOCTYPE html>" "$WORKSPACE/public/index.html"; then
  echo "[error] Unexpected DOCTYPE already present!" >&2
  exit 1
fi
echo "[pass] Verified: DOCTYPE not present (task still to be done)"

# ---------- 6.  Open VS Code -------------------------------------------------
echo "[info] Launching VS Code..."
code "$WORKSPACE" &
sleep 2

echo "=== Setup complete. In VS Code, open public/index.html,"
echo "=== insert \"<!DOCTYPE html>\" as the FIRST line, then press Ctrl+S."
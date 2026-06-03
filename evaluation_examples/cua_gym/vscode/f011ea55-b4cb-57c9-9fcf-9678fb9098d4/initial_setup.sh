#!/usr/bin/env bash
#
# 01_setup_initial.sh
# -------------------
# Prepares the VS Code workspace /home/user/frontend.code-workspace
# and guarantees that “Format Document” is *NOT* yet bound to
# Ctrl+Shift+F.  VS Code is opened at the end so the learner can
# perform the key-binding task manually.
#
set -euo pipefail

echo ">>> [INITIAL] Creating realistic React client workspace …"

##############################################################################
# 1.  Create project structure
##############################################################################
WORKSPACE_FILE="/home/user/frontend.code-workspace"   # <- MUST match task text
PROJECT_DIR="/home/user/frontend"                     # folder referenced by WS

# Re-create clean slate
rm -rf  "$PROJECT_DIR"  "$WORKSPACE_FILE"
mkdir -p "$PROJECT_DIR/src"

# Minimal React-style scaffolding
cat > "$PROJECT_DIR/package.json" << 'EOF'
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "scripts": {
    "start": "echo 'Pretend dev-server'"
  }
}
EOF

cat > "$PROJECT_DIR/src/index.js" << 'EOF'
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
EOF

cat > "$PROJECT_DIR/src/App.js" << 'EOF'
import React from "react";

export default function App() {
  return <h1>Hello, VS Code Tasks!</h1>;
}
EOF

##############################################################################
# 2.  Generate .code-workspace file
##############################################################################
cat > "$WORKSPACE_FILE" << EOF
{
  "folders": [
    { "path": "$PROJECT_DIR" }
  ],
  "settings": {
    "files.autoSave": "off"
  }
}
EOF
echo ">>> [INITIAL] Workspace file created at: $WORKSPACE_FILE"

##############################################################################
# 3.  Ensure user keybindings file exists & contains NO Ctrl+Shift+F override
##############################################################################
VSCODE_USER_DIR="$HOME/.config/Code/User"
mkdir -p "$VSCODE_USER_DIR"
KEYBINDINGS_JSON="$VSCODE_USER_DIR/keybindings.json"

# If the file does not exist, create a minimal placeholder; otherwise preserve.
if [[ ! -f "$KEYBINDINGS_JSON" ]]; then
  echo "[]" > "$KEYBINDINGS_JSON"
fi

# ----- verification: Ctrl+Shift+F must NOT be bound to Format Document ------
if command -v jq >/dev/null 2>&1; then
  BOUND=$(jq '
    map(select(.key?=="ctrl+shift+f" and .command?=="editor.action.formatDocument"))
    | length' "$KEYBINDINGS_JSON")
else
  # Fallback grep (non-strict)
  BOUND=$(grep -c '"key": *"ctrl+shift+f"' "$KEYBINDINGS_JSON" || true)
fi

if [[ "$BOUND" -eq 0 ]]; then
  echo ">>> [INITIAL] Verification PASSED – no Ctrl+Shift+F mapping yet."
else
  echo ">>> [INITIAL] WARNING – Ctrl+Shift+F is already mapped.  Removing…"
  if command -v jq >/dev/null 2>&1; then
    jq 'map(select(.key!="ctrl+shift+f"))' "$KEYBINDINGS_JSON" > "$KEYBINDINGS_JSON.tmp"
    mv "$KEYBINDINGS_JSON.tmp" "$KEYBINDINGS_JSON"
  fi
fi

##############################################################################
# 4.  Open VS Code so the learner can perform the task
##############################################################################
echo ">>> [INITIAL] Opening VS Code …"
code "$WORKSPACE_FILE" &
sleep 2

echo ">>> [INITIAL] Environment ready.  Please map “Format Document” to Ctrl+Shift+F."
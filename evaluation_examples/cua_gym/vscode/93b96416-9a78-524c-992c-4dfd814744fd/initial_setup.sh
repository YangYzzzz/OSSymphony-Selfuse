#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# VS Code Snippet Task – Initial State
# -----------------------------------------------------------------------------
# Creates a small React workspace and a user-snippet file that is **missing**
# the requested "rfunc" snippet.  VS Code is opened at the end so the user can
# add the snippet manually through the GUI (Ctrl+Shift+P → “Preferences: Open
# User Snippets” → javascriptreact.json, etc.).
# -----------------------------------------------------------------------------
set -euo pipefail

echo "─────────────────────────────────────────────────────────────"
echo "Setting up INITIAL state for the React snippet task …"
echo "─────────────────────────────────────────────────────────────"

# ---------- variables ---------------------------------------------------------
WORKSPACE="$HOME/react_snippet_task"
SNIPPET_DIR="$HOME/.config/Code/User/snippets"
SNIPPET_FILE="$SNIPPET_DIR/javascriptreact.json"
BACKUP_FILE="$SNIPPET_FILE.backup.$(date +%s)"

# ---------- clean / create workspace -----------------------------------------
echo "Preparing workspace: $WORKSPACE"
rm -rf  "$WORKSPACE"
mkdir -p "$WORKSPACE/src"

cat > "$WORKSPACE/src/App.jsx" <<'EOF'
import React from 'react';

export default function App() {
  return (
    <div>
      {/* Type `rfunc` ⇥ here once you have created the snippet! */}
    </div>
  );
}
EOF

cat > "$WORKSPACE/package.json" <<'EOF'
{
  "name": "snippet-demo",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
EOF

echo "Created sample React project."

# ---------- prepare snippet file ---------------------------------------------
mkdir -p "$SNIPPET_DIR"

if [[ -f "$SNIPPET_FILE" ]]; then
  echo "Existing javascriptreact.json detected – backing up to $BACKUP_FILE"
  cp "$SNIPPET_FILE" "$BACKUP_FILE"
fi

# Create a file that intentionally lacks the "rfunc" snippet
cat > "$SNIPPET_FILE" <<'EOF'
{
  // Example snippet (kept on purpose):
  "printToConsole": {
    "prefix": "log",
    "body": [
      "console.log('$1');",
      "$2"
    ],
    "description": "Log output to console"
  }
}
EOF

echo "Wrote fresh snippet file WITHOUT the rfunc entry."

# ---------- verification ------------------------------------------------------
if grep -q '"rfunc"' "$SNIPPET_FILE"; then
  echo "ERROR: rfunc snippet already present – aborting."
  exit 1
fi
echo "Verified: 'rfunc' snippet is NOT present (expected for initial state)."

# ---------- task instructions -------------------------------------------------
cat > "$WORKSPACE/.task_info.txt" <<'EOF'
⚠️  TASK: Add a new "rfunc" snippet for a React functional component
   • File to edit: ~/.config/Code/User/snippets/javascriptreact.json
   • Trigger text : rfunc
   • After adding, type "rfunc" inside App.jsx, press Ctrl+Space then Tab and the component template should appear.
EOF
echo "Created task instructions – open this file in VS Code for guidance."

# ---------- open VS Code ------------------------------------------------------
echo "Opening VS Code…"
code "$WORKSPACE" &

echo "Initial setup complete – VS Code is ready."
#!/usr/bin/env bash
###############################################################################
# VS Code Task – Initial State
# Creates a Node.js workspace that still needs the user to switch on
#   "files.autoSave": "afterDelay"
#   "files.autoSaveDelay": 1000
#
# After execution you will see VS Code open with a simple Node project in which
# autosave is still OFF.  A task hint file points out the change you must make.
###############################################################################
set -euo pipefail

echo "🔧  Preparing initial autosave task workspace …"

# -----------------------------------------------------------------------------
# 1. Workspace location
# -----------------------------------------------------------------------------
WORKSPACE="$HOME/node_autosave_task"
if [[ -d "$WORKSPACE" ]]; then
  echo "⚠️  Removing pre-existing workspace at $WORKSPACE"
  rm -rf "$WORKSPACE"
fi
mkdir -p "$WORKSPACE/.vscode"

# -----------------------------------------------------------------------------
# 2. Create a minimal Node.js project
# -----------------------------------------------------------------------------
cat > "$WORKSPACE/package.json" << 'EOF'
{
  "name": "autosave-demo",
  "version": "1.0.0",
  "description": "Demo project for VS Code autosave task",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js"
  },
  "license": "MIT"
}
EOF

mkdir -p "$WORKSPACE/src"
cat > "$WORKSPACE/src/index.js" << 'EOF'
const fs = require('fs');
console.log("Edit me, then stop typing – nothing will auto-save yet!");
EOF

cat > "$WORKSPACE/config.json" << 'EOF'
{
  "port": 3000,
  "env": "development"
}
EOF

# -----------------------------------------------------------------------------
# 3. Workspace-level VS Code settings (autosave still OFF)
# -----------------------------------------------------------------------------
cat > "$WORKSPACE/.vscode/settings.json" << 'EOF'
{
  "files.autoSave": "off",
  "editor.tabSize": 2,
  "javascript.format.insertSpaceAfterCommaDelimiter": true
}
EOF

# -----------------------------------------------------------------------------
# 4. Task marker to remind the user what to do
# -----------------------------------------------------------------------------
cat > "$WORKSPACE/README_TASK.md" << 'EOF'
# VS Code Task – Enable Auto Save

Open the Command Palette (Ctrl+Shift+P) → “Preferences: Open Workspace Settings (JSON)”
and add:

  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000

so that every .js / .json file is saved 1 second after typing stops.
EOF

# -----------------------------------------------------------------------------
# 5. Verification of initial state
# -----------------------------------------------------------------------------
echo "✅  Verifying that autosave is currently OFF …"
if grep -q '"files.autoSave": "off"' "$WORKSPACE/.vscode/settings.json"; then
  echo "   ✔  autosave is OFF as expected."
else
  echo "   ❌  Unexpected autosave setting – aborting."
  exit 1
fi

# -----------------------------------------------------------------------------
# 6. Open VS Code
# -----------------------------------------------------------------------------
echo "🚀  Opening VS Code at $WORKSPACE"
code "$WORKSPACE" &

echo "📝  Initial setup complete.  Perform the task as described!"
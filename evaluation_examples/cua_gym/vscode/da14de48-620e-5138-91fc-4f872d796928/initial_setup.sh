#!/usr/bin/env bash
# File: setup_initial.sh
# Purpose: Prepare the workspace that still needs the Prettier extension
# Author: VS-Code Automation Task Generator

set -euo pipefail

echo "=== VS Code Prettier Task – Initial Setup ==="

###############################################################################
# 1. Define workspace location
###############################################################################
WORKSPACE="$HOME/ts_prettier_task"
SRC_DIR="$WORKSPACE/src"
VSCODE_DIR="$WORKSPACE/.vscode"

###############################################################################
# 2. Start fresh
###############################################################################
rm -rf  "$WORKSPACE"
mkdir -p "$SRC_DIR" "$VSCODE_DIR"

###############################################################################
# 3. Create a badly-formatted TypeScript file
###############################################################################
cat > "$SRC_DIR/index.ts" <<'EOF'
/* A deliberately poorly formatted TypeScript file */

function  helloWorld ( name:string){console.log( "Hello, "+name   ) }

helloWorld("VS Code" )
EOF

###############################################################################
# 4. Minimal workspace settings – no Prettier yet
###############################################################################
cat > "$VSCODE_DIR/settings.json" <<'EOF'
{
  // Prettier is NOT configured yet
  "editor.formatOnSave": false
}
EOF

###############################################################################
# 5. Task instructions for the learner (marker file)
###############################################################################
cat > "$WORKSPACE/TASK.md" <<'EOF'
# Task
Install the “Prettier – Code formatter” extension and configure VS Code
so that this project:
1. Uses Prettier as the default formatter
2. Automatically formats on save
Save *src/index.ts* afterwards to verify that it is reformatted.
EOF

###############################################################################
# 6. Verify current (negative) state – Prettier should NOT be installed
###############################################################################
if code --list-extensions | grep -q "esbenp.prettier-vscode"; then
  echo "WARNING: Prettier extension already installed for this user."
  echo "       The workspace, however, is still unconfigured."
else
  echo "OK: Prettier extension not installed yet (expected)."
fi

###############################################################################
# 7. Open VS Code
###############################################################################
echo "Opening VS Code at $WORKSPACE ..."
code "$WORKSPACE" &
echo "=== Initial setup complete. ==="
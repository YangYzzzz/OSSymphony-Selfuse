#!/usr/bin/env bash
# --------------------------------------------
# initialize_task.sh
# --------------------------------------------
# Prepares the workspace for the user task:
# “Replace every occurrence of ‘import’ with ‘require’ in
#  /home/user/project/server.js”
# --------------------------------------------
set -euo pipefail

echo "===== VS Code Task – INITIAL SETUP ====="

# 1. Create the project directory structure
PROJECT_DIR="/home/user/project"
SERVER_JS="$PROJECT_DIR/server.js"
VSCODE_DIR="$PROJECT_DIR/.vscode"

echo "Creating fresh workspace at: $PROJECT_DIR"
rm -rf "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR" "$VSCODE_DIR"

# 2. Seed server.js with multiple occurrences of the word 'import'
cat > "$SERVER_JS" << 'EOF'
/**
 * server.js – Example Node server to be migrated from ES Modules
 * The task is to replace ALL occurrences of the keyword "import"
 * with "require" (CommonJS style).
 */

import http from "http";                      // <-- 1st occurrence
import { readFileSync } from "fs";            // <-- 2nd occurrence

function startServer() {
    console.log("Starting server...");

    // The word 'import' also appears inside a string:
    const note = "We still need to import more utils later";
    console.log(note);
}

startServer();
EOF
echo "Created $SERVER_JS with dummy 'import' statements."

# 3. Add a minimal workspace settings.json (optional realism)
cat > "$VSCODE_DIR/settings.json" << 'EOF'
{
    "editor.tabSize": 2,
    "files.autoSave": "off"
}
EOF

# 4. Simple verification – ensure the keyword "import" is present
if grep -q "import" "$SERVER_JS"; then
  echo "✅ Verification passed: 'import' found in server.js"
else
  echo "❌ ERROR: 'import' not found in server.js"; exit 1
fi

# 5. Open the project in VS Code for the user
echo "Opening VS Code..."
code "$PROJECT_DIR" &

echo "===== Initial setup complete – user may now perform the task. ====="
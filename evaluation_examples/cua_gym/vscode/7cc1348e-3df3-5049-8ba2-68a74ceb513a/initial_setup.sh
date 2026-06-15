#!/usr/bin/env bash
set -euo pipefail

###############################################################################
#  VS Code Task – Initial State
#  1. Creates an Express project in /home/user/projects/todo-app
#  2. Removes the REST Client extension if present
#  3. Ensures .env files are VISIBLE (no files.exclude setting)
#  4. Opens the workspace in VS Code
###############################################################################

echo "==============  VS Code REST-Client Task : Initial Setup  =============="

WORKSPACE="/home/user/projects/todo-app"
USER_VSCODE_DIR="$HOME/.config/Code/User"
EXTENSION_ID="humao.rest-client"

###############################################################################
# 1. Create Express project skeleton
###############################################################################
echo "[1/5] Creating project directory: ${WORKSPACE}"
rm -rf "${WORKSPACE}"
mkdir -p "${WORKSPACE}"/{src,routes}

echo "[2/5] Adding sample package.json and server.js"
cat > "${WORKSPACE}/package.json" <<'EOF'
{
  "name": "todo-app",
  "version": "1.0.0",
  "main": "src/server.js",
  "scripts": {
    "start": "node src/server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "dotenv": "^16.3.1"
  }
}
EOF

cat > "${WORKSPACE}/src/server.js" <<'EOF'
require('dotenv').config();
const express = require('express');
const app = express();

app.get('/api/v1/todos', (req, res) => {
  res.json([{ id: 1, title: 'Buy milk' }]);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`API running on port ${PORT}`));
EOF

###############################################################################
# 2. Create a couple of .env files so the user can see they are visible
###############################################################################
echo "[3/5] Creating .env files to verify visibility later"
cat > "${WORKSPACE}/.env" <<'EOF'
PORT=3000
EOF

# A second .env file elsewhere under /home/user/ to enforce “anywhere” scope
echo "DEBUG=true" > "/home/user/.env"

###############################################################################
# 3. Make sure REST Client extension is NOT installed so the user needs to add it
###############################################################################
if code --list-extensions | grep -q "${EXTENSION_ID}" ; then
  echo "[4/5] REST Client extension detected. Uninstalling to create task need…"
  code --uninstall-extension "${EXTENSION_ID}" || true
else
  echo "[4/5] REST Client extension not present – perfect."
fi

###############################################################################
# 4. Ensure user settings DO NOT hide .env files
###############################################################################
echo "[5/5] Removing any .env exclusion rules from user settings"
mkdir -p "${USER_VSCODE_DIR}"
SETTINGS_FILE="${USER_VSCODE_DIR}/settings.json"
if [[ -f "${SETTINGS_FILE}" ]]; then
  # Remove .env rules if present (fallback to cat if jq missing)
  if command -v jq >/dev/null 2>&1; then
    jq 'del(.["files.exclude"]["**/.env"]) | del(.["files.exclude"]["**/.env.*"])' \
       "${SETTINGS_FILE}" > "${SETTINGS_FILE}.tmp" 2>/dev/null || cat "${SETTINGS_FILE}" > "${SETTINGS_FILE}.tmp"
    mv "${SETTINGS_FILE}.tmp" "${SETTINGS_FILE}"
  fi
fi

###############################################################################
# 5. Verification
###############################################################################
echo
echo "---------  Verification  ----------"
echo "REST Client installed?  $(code --list-extensions | grep -q "${EXTENSION_ID}" && echo "YES (unexpected!)" || echo "NO (expected)")"
echo ".env exclusion present? $(grep -q '"\*\*/\.env"' "${SETTINGS_FILE:-/dev/null}" && echo "YES (unexpected!)" || echo "NO (expected)")"
echo "-----------------------------------"
echo

###############################################################################
# 6. Launch VS Code on the workspace
###############################################################################
echo "Opening VS Code…"
code "${WORKSPACE}" &

echo "Initial setup complete.  User now needs to:"
echo "   • Install the “REST Client” extension."
echo "   • Hide all .env files via files.exclude."
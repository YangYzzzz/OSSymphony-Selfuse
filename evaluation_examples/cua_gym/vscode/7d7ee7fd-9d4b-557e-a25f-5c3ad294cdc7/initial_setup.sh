#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# VS Code Task: Uninstall the “Live Server” extension                         #
# This script prepares the initial state where:                               #
#   1. A small web-project workspace exists                                   #
#   2. The “Live Server” extension appears to be installed                    #
# The learner’s job (inside VS Code) is to uninstall that extension.          #
###############################################################################

echo "──────────────────────────────────────────────────────────────"
echo "🔧  Preparing initial environment for the Live Server task..."
echo "──────────────────────────────────────────────────────────────"

# ------------------------------------------------------------------
# 1. Create workspace with a simple web project
# ------------------------------------------------------------------
WORKSPACE="$HOME/vscode_live_server_task"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE"
cat > "$WORKSPACE/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>VS Code Live Server Demo</title>
</head>
<body>
  <h1>Hello, Live Server!</h1>
</body>
</html>
EOF
echo "📁  Workspace created at: $WORKSPACE"

# ------------------------------------------------------------------
# 2. Make sure the Live Server extension *looks* installed
# ------------------------------------------------------------------
EXT_ID="ritwickdey.LiveServer"
echo "⚙️  Ensuring extension \"$EXT_ID\" is installed..."

# Preferred path to the user’s extensions folder
EXT_DIR="$HOME/.vscode/extensions"
mkdir -p "$EXT_DIR"

INSTALL_OK=false

# (a) First attempt: use VS Code CLI (works if Internet access is available)
if command -v code >/dev/null 2>&1; then
  if code --install-extension "$EXT_ID" --force >/dev/null 2>&1; then
    echo "✅  Installed via VS Code CLI."
    INSTALL_OK=true
  fi
else
  echo "⚠️  'code' command not found in PATH."
fi

# (b) Fallback: fabricate a minimal stub so that `code --list-extensions`
#     shows the extension even without network access.
if [ "$INSTALL_OK" = false ]; then
  STUB="$EXT_DIR/${EXT_ID}-0.0.0"
  mkdir -p "$STUB"
  cat > "$STUB/package.json" << 'EOF'
{
  "name": "live-server",
  "displayName": "Live Server (stub)",
  "version": "0.0.0",
  "publisher": "ritwickdey",
  "engines": { "vscode": "^1.40.0" },
  "activationEvents": [],
  "main": ""
}
EOF
  echo "🛠️  Created local stub extension at: $STUB"
fi

# ------------------------------------------------------------------
# 3. Verify installation
# ------------------------------------------------------------------
if code --list-extensions | grep -q "^${EXT_ID}$"; then
  echo "🔍  Verification passed: $EXT_ID is listed as installed."
else
  echo "❌  ERROR: $EXT_ID is NOT listed. Aborting."
  exit 1
fi

# ------------------------------------------------------------------
# 4. Create a task marker file so the learner knows what to do
# ------------------------------------------------------------------
echo "Uninstall the \"Live Server\" extension from VS Code." > "$WORKSPACE/.task_info.txt"
echo "📝  Task instruction saved to .task_info.txt"

# ------------------------------------------------------------------
# 5. Open VS Code pointing to the workspace
# ------------------------------------------------------------------
echo "🚀  Launching VS Code..."
code "$WORKSPACE" &

echo "✅  Initial environment ready. Learner should now uninstall the extension."
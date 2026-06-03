#!/usr/bin/env bash
###############################################################################
# VS Code Task: Install a local VSIX with snippets                            #
# INITIAL SETUP SCRIPT                                                        #
# This script creates a workspace at /home/user/workspace that contains a     #
# locally built VSIX file (/home/user/workspace/my-snippets.vsix).            #
# The VSIX is NOT installed yet – the user must install it from within VSCode #
###############################################################################
set -euo pipefail

echo "Preparing initial environment for the VSIX-install task …"

# ---------------------------------------------------------------------------
# 1. Create the workspace folder structure
# ---------------------------------------------------------------------------
WS_PATH="/home/user/workspace"
mkdir -p "$WS_PATH"
echo "Workspace folder ensured at: $WS_PATH"

# ---------------------------------------------------------------------------
# 2. Build a minimal snippet extension → my-snippets.vsix
#    (VSIX = ordinary zip archive with some mandatory files)
# ---------------------------------------------------------------------------
EXT_DIR="$WS_PATH/ext_tmp"
rm -rf "$EXT_DIR"
mkdir -p "$EXT_DIR/snippets"

# Minimal package.json (identifier: local.my-snippets)
cat > "$EXT_DIR/package.json" <<'EOF'
{
  "name": "my-snippets",
  "displayName": "My Snippets",
  "description": "Personal code snippets exported by the user.",
  "version": "0.0.1",
  "publisher": "local",
  "engines": {
    "vscode": "^1.50.0"
  },
  "contributes": {
    "snippets": [
      {
        "language": "javascript",
        "path": "./snippets/javascript.json"
      }
    ]
  }
}
EOF

# One tiny snippet
cat > "$EXT_DIR/snippets/javascript.json" <<'EOF'
{
  "log": {
    "prefix": "log",
    "body": [
      "console.log('$1');"
    ],
    "description": "Console log"
  }
}
EOF

# Create the VSIX (zip) – MUST be named exactly as required by the task
pushd "$EXT_DIR" >/dev/null
zip -qr "$WS_PATH/my-snippets.vsix" .
popd >/dev/null
echo "VSIX built at: $WS_PATH/my-snippets.vsix"
rm -rf "$EXT_DIR"      # cleanup temp folder

# ---------------------------------------------------------------------------
# 3. Provide a sample project file where the user can try the snippet
# ---------------------------------------------------------------------------
cat > "$WS_PATH/app.js" <<'EOF'
/*
 * Open this file after installing the VSIX.
 * Type "log" and hit <TAB> to expand the snippet!
 */
function main() {
  // place snippet here
}
main();
EOF
echo "Sample file created: app.js"

# ---------------------------------------------------------------------------
# 4. Ensure the extension is **NOT** installed yet (clean initial state)
# ---------------------------------------------------------------------------
if code --list-extensions | grep -q "local.my-snippets"; then
  echo "Previous installation detected – uninstalling to restore initial state."
  code --uninstall-extension "local.my-snippets" || true
fi

# ---------------------------------------------------------------------------
# 5. Drop a task hint for the learner
# ---------------------------------------------------------------------------
echo "INSTALL the VSIX located in the workspace root to enable your snippets." \
  > "$WS_PATH/.task_info.txt"

# ---------------------------------------------------------------------------
# 6. Open the workspace in VS Code
# ---------------------------------------------------------------------------
echo "Launching VS Code…"
code "$WS_PATH" &

echo "Initial setup complete. User now needs to install the VSIX (Ctrl+Shift+P → 'Extensions: Install from VSIX…')."
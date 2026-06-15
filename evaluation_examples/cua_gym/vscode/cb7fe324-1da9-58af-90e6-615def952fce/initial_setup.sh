#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial VS Code task setup
# 1. Creates a small Rust workspace that supposedly contains a bug
# 2. Builds a **local** VS Code extension package at the EXACT path required
#    (/home/user/temp/debug-tool.vsix) – but DOES NOT install it
# 3. Verifies the extension is NOT yet installed
# 4. Opens VS Code on the workspace so the user can perform the GUI task
###############################################################################

echo "🔧  Preparing initial environment for local-extension-install task …"

# --------------------------------------------------------------------------
# 0. House-keeping
# --------------------------------------------------------------------------
WORKSPACE_DIR="/home/user/projects/rust-bug"
VSIX_PATH="/home/user/temp/debug-tool.vsix"
EXT_PUBLISHER="local"
EXT_NAME="debug-tool"
EXT_FULL_ID="${EXT_PUBLISHER}.${EXT_NAME}"   # ->  local.debug-tool

rm -rf  "$WORKSPACE_DIR"           # start clean every run
mkdir -p "$WORKSPACE_DIR/src"
mkdir -p "$(dirname "$VSIX_PATH")"  # /home/user/temp

# --------------------------------------------------------------------------
# 1. Create a very small Rust project with a deliberate bug
# --------------------------------------------------------------------------
cat > "$WORKSPACE_DIR/src/main.rs" <<'EOF'
fn main() {
    // BUG: panic on purpose
    panic!("Something went wrong!");
}
EOF

cat > "$WORKSPACE_DIR/Cargo.toml" <<'EOF'
[package]
name = "rust_bug"
version = "0.1.0"
edition = "2021"
EOF

echo "📁  Rust workspace created at $WORKSPACE_DIR"

# --------------------------------------------------------------------------
# 2. Build a **minimal** VSIX package so the task is fully self-contained
#      (VSIX is just a ZIP file; we create the required structure manually)
# --------------------------------------------------------------------------
TMP_BUILD_DIR="/tmp/${EXT_NAME}_build"
rm -rf "$TMP_BUILD_DIR"
mkdir -p "$TMP_BUILD_DIR/extension"

# 2a. Extension manifest
cat > "$TMP_BUILD_DIR/extension/package.json" <<EOF
{
  "name": "${EXT_NAME}",
  "displayName": "Debug Tool",
  "description": "A tiny helper to track nasty bugs.",
  "version": "0.0.1",
  "publisher": "${EXT_PUBLISHER}",
  "engines": { "vscode": "^1.50.0" },
  "categories": ["Other"],
  "main": "./extension.js",
  "activationEvents": [ "*" ],
  "contributes": {}
}
EOF

# 2b. Extremely small JS entry
echo 'console.log("Debug Tool extension activated");' \
  > "$TMP_BUILD_DIR/extension/extension.js"

# 2c. README
echo '# Debug Tool – local helper' > "$TMP_BUILD_DIR/extension/README.md"

# 2d. Pack it into a VSIX (zip) at the EXACT path requested
(
  cd "$TMP_BUILD_DIR"
  zip -q -r "$VSIX_PATH" .
)
echo "📦  Local extension packaged at $VSIX_PATH"

# --------------------------------------------------------------------------
# 3. Verification – make sure the extension is NOT yet installed
# --------------------------------------------------------------------------
if code --list-extensions | grep -q "$EXT_FULL_ID"; then
    echo "⚠️  Extension ${EXT_FULL_ID} is already installed; removing for a clean start."
    code --uninstall-extension "$EXT_FULL_ID" --force || true
fi
echo "✅  Verified that ${EXT_FULL_ID} is NOT currently installed."

# --------------------------------------------------------------------------
# 4. Open VS Code on the workspace – user will now install the extension
# --------------------------------------------------------------------------
echo "🚀  Launching VS Code.  Use:
        • File → Preferences → Extensions → … menu
        • or Command Palette → “Extensions: Install from VSIX…”
      and choose  $VSIX_PATH"
code "$WORKSPACE_DIR" &

###############################################################################
echo "Initial setup complete. Happy debugging! 🐞"
###############################################################################
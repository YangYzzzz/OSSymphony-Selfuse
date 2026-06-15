#!/usr/bin/env bash
# Purpose: Prepare the initial VS Code workspace where no background image is
#          configured yet.
set -euo pipefail

echo "=== VS Code Background-Image TASK – Initial Setup ==="

# ---------------------------------------------------------------------------
# 1. Create workspace directory structure
# ---------------------------------------------------------------------------
WORKSPACE="/home/user/workspace"
ASSET_DIR="$WORKSPACE/assets"
VSCODE_DIR="$WORKSPACE/.vscode"

echo "Creating workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$ASSET_DIR" "$VSCODE_DIR"

# ---------------------------------------------------------------------------
# 2. Add placeholder project content
# ---------------------------------------------------------------------------
cat > "$WORKSPACE/README.md" << 'EOF'
# VS Code Background Image Task

This workspace is prepared for a task where you will configure VS Code to use
an image located at /home/user/workspace/assets/bg.jpg as the editor's
background.  
EOF

# ---------------------------------------------------------------------------
# 3. Create the background image file (dummy placeholder)
# ---------------------------------------------------------------------------
echo "Creating dummy background image …"
# A 1-pixel transparent PNG renamed to .jpg (keeps script self-contained)
base64 -d > "$ASSET_DIR/bg.jpg" << 'BASE64'
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=
BASE64

# ---------------------------------------------------------------------------
# 4. Prepare VS Code settings (no background configured)
# ---------------------------------------------------------------------------
cat > "$VSCODE_DIR/settings.json" << 'EOF'
{
  // Initial editor settings – NO BACKGROUND IMAGE YET
  "workbench.colorTheme": "Default Dark+",
  "editor.fontSize": 14
}
EOF
echo "Initial settings written to $VSCODE_DIR/settings.json"

# ---------------------------------------------------------------------------
# 5. Task instructions marker (helpful for reviewers)
# ---------------------------------------------------------------------------
echo "Configure /home/user/workspace/assets/bg.jpg as VS Code background image." \
  > "$WORKSPACE/.task_info.txt"

# ---------------------------------------------------------------------------
# 6. Open VS Code
# ---------------------------------------------------------------------------
echo "Launching VS Code…"
code "$WORKSPACE" &

# ---------------------------------------------------------------------------
# 7. Verification of initial state
# ---------------------------------------------------------------------------
if jq -e 'has("background.customImages")' "$VSCODE_DIR/settings.json" >/dev/null; then
  echo "WARN: background.customImages already present – unexpected for initial state."
else
  echo "Verified: No background image configured yet (expected)."
fi

echo "=== Initial setup complete. ==="
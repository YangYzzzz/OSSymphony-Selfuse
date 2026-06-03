#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# VS Code Auto-Save Task – INITIAL STATE
# Turns Auto Save ON so the user needs to switch it OFF manually.
# ------------------------------------------------------------------------------

set -euo pipefail

echo "=== Preparing initial workspace with Auto Save ENABLED ==="

# ---------------------------------------------------------------------------
# 1. Workspace creation
# ---------------------------------------------------------------------------
WORKSPACE="$HOME/vscode_auto_save_task"
VSCODE_DIR="$WORKSPACE/.vscode"

# Start fresh
rm -rf "$WORKSPACE"
mkdir -p "$VSCODE_DIR"

# ---------------------------------------------------------------------------
# 2. Sample project files
# ---------------------------------------------------------------------------
cat > "$WORKSPACE/main.py" << 'EOF'
print("Hello!  Edit me and watch VS Code auto-save.")
EOF

cat > "$WORKSPACE/README.md" << 'EOF'
# VS Code Auto-Save Task

Your goal:
1) Open `.vscode/settings.json`
2) Disable Auto Save (set `"files.autoSave": "off"`).
EOF

# ---------------------------------------------------------------------------
# 3. Workspace-level settings with Auto Save ON
# ---------------------------------------------------------------------------
cat > "$VSCODE_DIR/settings.json" << 'EOF'
{
  // Auto Save is currently ON. Change this to "off".
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000
}
EOF

echo "Workspace settings written to $VSCODE_DIR/settings.json"

# ---------------------------------------------------------------------------
# 4. Verification of initial state
# ---------------------------------------------------------------------------
if grep -q '"files.autoSave": "afterDelay"' "$VSCODE_DIR/settings.json"; then
    echo "✓ Verification passed: Auto Save is ENABLED (afterDelay)."
else
    echo "✗ Verification failed: Auto Save not set as expected."
    exit 1
fi

# ---------------------------------------------------------------------------
# 5. Task cue file
# ---------------------------------------------------------------------------
echo "Disable Auto Save in VS Code (set to \"off\")" > "$WORKSPACE/.task_info.txt"

# ---------------------------------------------------------------------------
# 6. Open VS Code
# ---------------------------------------------------------------------------
echo "Opening VS Code…"
code "$WORKSPACE" &

echo "=== Initial setup complete. ==="
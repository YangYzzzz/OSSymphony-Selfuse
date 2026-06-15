#!/usr/bin/env bash
# Purpose: Prepare a workspace where Ctrl+E is *NOT* bound to the terminal yet.
# A task marker tells the user to change it.

set -euo pipefail

echo "=== VS Code Keybinding Task: Initial Setup ==="

# ---------------------------------------------------------------------------
# 1. Determine user-level VS Code settings location
# ---------------------------------------------------------------------------
if [[ "$(uname)" == "Darwin" ]]; then
    VSCODE_USER_DIR="$HOME/Library/Application Support/Code/User"
else
    VSCODE_USER_DIR="$HOME/.config/Code/User"
fi
mkdir -p "$VSCODE_USER_DIR"

KEYBINDINGS_FILE="$VSCODE_USER_DIR/keybindings.json"

# ---------------------------------------------------------------------------
# 2. Create an initial keybinding set
#    - Ctrl+E is currently mapped to Quick Open (the VS Code default on Windows)
# ---------------------------------------------------------------------------
cat > "$KEYBINDINGS_FILE" << 'EOF'
[
  {
    "key": "ctrl+e",
    "command": "workbench.action.quickOpen"
  },
  {
    "key": "ctrl+`",
    "command": "workbench.action.terminal.toggleTerminal"
  }
]
EOF
echo "Created initial keybindings at: $KEYBINDINGS_FILE"

# ---------------------------------------------------------------------------
# 3. Prepare a realistic Python workspace
# ---------------------------------------------------------------------------
WORKSPACE="$HOME/vscode_terminal_toggle_task"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"

cat > "$WORKSPACE/src/app.py" << 'EOF'
import time

def busy_loop():
    print("Busy looping – press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped.")

if __name__ == "__main__":
    busy_loop()
EOF

cat > "$WORKSPACE/README.md" << 'EOF'
# Ctrl+E Terminal Toggle Task

Goal: Re-bind **Ctrl+E** so it toggles the integrated terminal
(`workbench.action.terminal.toggleTerminal`).
EOF

# ---------------------------------------------------------------------------
# 4. Add a task marker file so the user sees the instructions
# ---------------------------------------------------------------------------
echo "Add keybinding: Bind Ctrl+E to workbench.action.terminal.toggleTerminal" \
  > "$WORKSPACE/.task_info.txt"

# ---------------------------------------------------------------------------
# 5. Verification – ensure Ctrl+E is *not* yet mapped to the terminal
# ---------------------------------------------------------------------------
echo "Verifying that Ctrl+E is NOT yet mapped to the terminal..."
if command -v jq &> /dev/null; then
    BINDED=$(jq -r '.[] | select(.key=="ctrl+e") | .command' "$KEYBINDINGS_FILE")
    if [[ "$BINDED" == "workbench.action.terminal.toggleTerminal" ]]; then
        echo "ERROR: Ctrl+E already mapped to terminal. Aborting initial setup."
        exit 1
    fi
else
    echo "Warning: jq not installed – skipping automated verification."
fi
echo "Verification passed."

# ---------------------------------------------------------------------------
# 6. Open VS Code
# ---------------------------------------------------------------------------
echo "Opening VS Code..."
code "$WORKSPACE" &

echo "=== Initial setup complete. ==="
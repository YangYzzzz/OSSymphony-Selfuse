#!/usr/bin/env bash
# Purpose: Prepare an initial state where VS Code uses a bright theme,
# prompting the user to change it to “Tomorrow Night Blue”.

set -euo pipefail

echo "=============================="
echo " VS Code Theme Task - Initial "
echo "=============================="

# 1. Define key paths
WORKSPACE="$HOME/vscode_theme_task"
VSCODE_USER_DIR="$HOME/.config/Code/User"
SETTINGS_FILE="$VSCODE_USER_DIR/settings.json"

# 2. Create workspace and sample content
echo "Creating workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE"
cat > "$WORKSPACE/README.md" << 'EOF'
# Night-Owl Coding

You’ve been coding late—let’s make the editor easier on your eyes!
EOF

# 3. Ensure the VS Code user settings folder exists
mkdir -p "$VSCODE_USER_DIR"

# 4. Write an *intentionally bright* theme into settings.json
cat > "$SETTINGS_FILE" << 'EOF'
{
  // Initial state for the task
  "workbench.colorTheme": "Default Light+",
  "editor.fontSize": 14,
  "files.autoSave": "off"
}
EOF

echo "Initial settings written to $SETTINGS_FILE"

# 5. Verification ‑ confirm theme is NOT “Tomorrow Night Blue”
if grep -q '"workbench.colorTheme": "Tomorrow Night Blue"' "$SETTINGS_FILE"; then
  echo "ERROR: Theme is already Tomorrow Night Blue – aborting initial setup." >&2
  exit 1
else
  echo "Verification passed: Theme is currently NOT Tomorrow Night Blue."
fi

# 6. Provide a task hint for the learner
echo "Switch the color theme to \"Tomorrow Night Blue\" via the Command Palette or Settings UI." \
  > "$WORKSPACE/.task_info.txt"

# 7. Open VS Code on the workspace
echo "Opening VS Code..."
code "$WORKSPACE" &

echo "Initial environment ready – happy theming!"
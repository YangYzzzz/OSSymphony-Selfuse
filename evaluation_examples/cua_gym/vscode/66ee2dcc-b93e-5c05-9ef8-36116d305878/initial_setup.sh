#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial Setup Script – VS Code Theme Change Task
# Creates a TypeScript workspace and forces the editor to use the default
# light theme.  The user’s job will be to switch to the “Cobalt2” theme.
###############################################################################

echo "🛠  Preparing initial environment for the Cobalt2 theme task..."

# ---------------------------------------------------------------------------
# 1. Locate VS Code user-settings directory (Linux/macOS default paths only)
# ---------------------------------------------------------------------------
if [[ "$OSTYPE" == "darwin"* ]]; then
  VSCODE_USER_DIR="$HOME/Library/Application Support/Code/User"
else
  VSCODE_USER_DIR="$HOME/.config/Code/User"
fi
mkdir -p "$VSCODE_USER_DIR"

SETTINGS_FILE="$VSCODE_USER_DIR/settings.json"

# ---------------------------------------------------------------------------
# 2. Force the default light theme in user settings
# ---------------------------------------------------------------------------
cat > "$SETTINGS_FILE" <<'EOF'
{
  // VS Code task – starting in the default light theme
  "workbench.colorTheme": "Default Light+",
  "editor.fontSize": 14,
  "files.autoSave": "off"
}
EOF
echo "✅  User settings written to $SETTINGS_FILE"

# ---------------------------------------------------------------------------
# 3. Create a realistic TypeScript workspace
# ---------------------------------------------------------------------------
WORKSPACE="$HOME/cobalt2_theme_task"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"

# Sample TypeScript files
cat > "$WORKSPACE/src/index.ts" <<'EOF'
export function greet(name: string): string {
  return `Hello, \${name}!`;
}

console.log(greet('VS Code'));
EOF

cat > "$WORKSPACE/tsconfig.json" <<'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "strict": true,
    "outDir": "dist"
  },
  "include": ["src"]
}
EOF

# Task reminder for the user
echo "Switch VS Code to the 'Cobalt2' color theme." > "$WORKSPACE/TASK.txt"

echo "📂  TypeScript workspace created at: $WORKSPACE"

# ---------------------------------------------------------------------------
# 4. Verification of initial state (should be Default Light+)
# ---------------------------------------------------------------------------
if grep -q '"workbench.colorTheme": "Default Light+"' "$SETTINGS_FILE"; then
  echo "✅  Verification passed: VS Code is configured with the Default Light+ theme."
else
  echo "❌  Verification failed: Expected Default Light+ theme not set." >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# 5. Launch VS Code
# ---------------------------------------------------------------------------
echo "🚀  Opening VS Code... (use this window to perform the task)"
code "$WORKSPACE" &
sleep 2
echo "📝  Initial setup complete."
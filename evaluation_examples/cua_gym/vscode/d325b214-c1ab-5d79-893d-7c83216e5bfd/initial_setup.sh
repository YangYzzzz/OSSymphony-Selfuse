#!/usr/bin/env bash
# -------------------------------------------
#  Initial Setup for “Prettier Workspace Task”
# -------------------------------------------
set -euo pipefail

echo "🛠  Creating initial Node.js workspace…"

# ------------------------------------------------------------------
# Workspace location
# ------------------------------------------------------------------
WORKSPACE="$HOME/nodejs_prettier_task"
rm -rf "$WORKSPACE"          # start clean every time the script runs
mkdir -p "$WORKSPACE/.vscode"

# ------------------------------------------------------------------
# Populate a small Node.js project
# ------------------------------------------------------------------
mkdir -p "$WORKSPACE/src"
cat > "$WORKSPACE/src/index.js" <<'EOF'
function add(a, b) {
    return a + b;      // <- indented with 4 spaces intentionally
}
console.log(add(2, 3));
EOF

cat > "$WORKSPACE/package.json" <<'EOF'
{
  "name": "prettier-task-demo",
  "version": "1.0.0",
  "main": "src/index.js",
  "license": "MIT"
}
EOF

# ------------------------------------------------------------------
# Create NON-compliant VS Code settings (user must fix these)
# ------------------------------------------------------------------
cat > "$WORKSPACE/.vscode/settings.json" <<'EOF'
{
  "editor.tabSize": 4,
  "editor.formatOnSave": false,
  "files.exclude": {
    "**/.git": true
  }
}
EOF

# Extension recommendations deliberately omit Prettier
cat > "$WORKSPACE/.vscode/extensions.json" <<'EOF'
{
  "recommendations": [
    "dbaeumer.vscode-eslint"
  ]
}
EOF

# ------------------------------------------------------------------
# Task instructions (visible in the workspace)
# ------------------------------------------------------------------
cat > "$WORKSPACE/TASK_INSTRUCTIONS.txt" <<'EOF'
🔧 VS Code Task:
Edit .vscode/settings.json so that VS Code…
  • Uses the "esbenp.prettier-vscode@9.0.0" extension as the default formatter
  • Formats automatically on save
  • Enforces a 2-space tab size
  • Hides node_modules in the Explorer

(Optional) Add Prettier as a recommended extension.
EOF

# ------------------------------------------------------------------
# Launch VS Code
# ------------------------------------------------------------------
echo "🚀 Opening VS Code…"
code "$WORKSPACE" &

# ------------------------------------------------------------------
# Verification of initial state
# ------------------------------------------------------------------
echo "✅ Initial state created at $WORKSPACE"
echo "Current settings file:"
cat "$WORKSPACE/.vscode/settings.json"
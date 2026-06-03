#!/usr/bin/env bash
# setup_initial.sh
# Purpose: prepare initial workspace that still needs .vscode/tasks.json
set -euo pipefail

echo "🔧  Preparing initial VS Code build-task exercise …"

# ---------- 1. Workspace -----------------------------------------------------------------
WORKSPACE="$HOME/vscode_build_task"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"
cd "$WORKSPACE"

# ---------- 2. Sample Node project -------------------------------------------------------
cat > package.json <<'EOF'
{
  "name": "build-task-demo",
  "version": "1.0.0",
  "description": "Demo project for VS Code task creation",
  "scripts": {
    "start": "node src/index.js",
    "lint": "echo Linting…"
  },
  "dependencies": {}
}
EOF

echo "console.log('Hello Task');" > src/index.js

# ---------- 3. VS Code folder (NO tasks.json yet) ----------------------------------------
mkdir -p .vscode
# Leave tasks.json missing on purpose

# ---------- 4. Task instructions ---------------------------------------------------------
cat > .task_info.txt <<'EOF'
=== VS Code Task ===
Create a file .vscode/tasks.json containing:
{
  "version": "2.0.0",
  "tasks": [
      // you can add npm scripts here later
  ]
}
EOF

# ---------- 5. Verification of initial state --------------------------------------------
if [ -f ".vscode/tasks.json" ]; then
    echo "⚠️  ERROR: tasks.json should NOT exist yet." >&2
    exit 1
fi
echo "✅  Verified: .vscode/tasks.json is absent (as expected)."

# ---------- 6. Launch VS Code ------------------------------------------------------------
echo "🚀  Opening VS Code.  Follow instructions in .task_info.txt."
code "$WORKSPACE" &

echo "Initial setup complete."
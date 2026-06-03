#!/usr/bin/env bash
# Purpose: Prepare an unsaved multi-root session in VS Code so the user can
#          manually run “File → Save Workspace As…” and store it as
#          /home/user/workspaces/myproject.code-workspace
set -euo pipefail

echo "========== VS Code Workspace Save Task – Initial Setup =========="

# 1. Create a few realistic project folders
echo "Creating sample project folders..."
PROJECT_ROOT="/home/user/projects"
API_DIR="$PROJECT_ROOT/api"
WEB_DIR="$PROJECT_ROOT/web"
DOCS_DIR="$PROJECT_ROOT/docs"

rm -rf "$PROJECT_ROOT"
mkdir -p "$API_DIR" "$WEB_DIR" "$DOCS_DIR"

echo "console.log('API');"  > "$API_DIR/index.js"
echo "<!-- Web front-end -->" > "$WEB_DIR/index.html"
echo "# Docs" > "$DOCS_DIR/README.md"

# 2. Ensure the workspace storage directory exists and is empty
WORKSPACE_DIR="/home/user/workspaces"
mkdir -p "$WORKSPACE_DIR"
rm -f "$WORKSPACE_DIR/myproject.code-workspace"

# 3. Provide a task hint file so the user sees clear instructions
cat > "$PROJECT_ROOT/README_TASK.md" << 'EOF'
# VS Code Task

Use the VS Code menu:

File → Save Workspace As…

…and save the workspace as:

/home/user/workspaces/myproject.code-workspace
EOF

# 4. Open VS Code with the three folders (multi-root) but WITHOUT an existing workspace file
echo "Launching VS Code with unsaved multi-root workspace..."
code -n "$API_DIR" "$WEB_DIR" "$DOCS_DIR" &

echo "=============================================================="
echo "Your environment is ready. Please save the workspace as instructed."
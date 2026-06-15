#!/usr/bin/env bash
# Purpose : Prepare the workspace for the VS Code task
# Task    : User must create /home/user/database/scripts/schema.sql
# Author  : VS Code Automation Assistant
# Usage   : ./initial_setup.sh
# ------------------------------------------------------------------
set -euo pipefail

echo "=== Initial VS Code task setup ==="

TARGET_DIR="/home/user/database/scripts"
TARGET_FILE="/home/user/database/scripts/schema.sql"
WORKSPACE_ROOT="/home/user/database"

# Clean up any previous runs (safety-guarded)
if [ -d "$WORKSPACE_ROOT" ]; then
    echo "Removing existing workspace at $WORKSPACE_ROOT to ensure a clean start…"
    rm -rf "$WORKSPACE_ROOT"
fi

echo "Creating workspace directory structure…"
mkdir -p "$TARGET_DIR"

# Populate a couple of realistic helper files
cat > "$WORKSPACE_ROOT/README.md" << 'EOF'
# Database Project

This workspace will contain all SQL scripts, migrations, and documentation for our database.
EOF

cat > "$TARGET_DIR/seed_data.sql" << 'EOF'
-- Sample seed data (placeholder)
INSERT INTO users (id, name) VALUES (1, 'Initial User');
EOF

# Guarantee the task file is ABSENT
if [ -f "$TARGET_FILE" ]; then
    echo "Removing existing $TARGET_FILE to enforce the task requirement…"
    rm -f "$TARGET_FILE"
fi

# Quick verification
if [ ! -f "$TARGET_FILE" ]; then
    echo "Verified: $TARGET_FILE does NOT yet exist (task still pending)"
else
    echo "ERROR: $TARGET_FILE unexpectedly exists." >&2
    exit 1
fi

# Provide a task hint file
echo "TODO: Create a new file named 'schema.sql' inside /home/user/database/scripts" \
  > "$WORKSPACE_ROOT/.task_info.txt"

# Optional VS Code workspace-level configuration
mkdir -p "$WORKSPACE_ROOT/.vscode"
cat > "$WORKSPACE_ROOT/.vscode/settings.json" << 'EOF'
{
    "files.autoSave": "off",
    "editor.tabSize": 4
}
EOF

echo "Opening VS Code…"
code "$WORKSPACE_ROOT" &

echo "=== Initial setup complete. VS Code is ready – create schema.sql in 'scripts' ==="
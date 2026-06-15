#!/usr/bin/env bash
# ------------------------------------------------------------------
# VS Code CLI-Help Task – Initial State
# Creates a workspace that is missing docs/cli_help.txt so the user
# has to run `code --help > docs/cli_help.txt` manually in VS Code.
# ------------------------------------------------------------------
set -euo pipefail

echo "==== VS Code CLI-Help Task : Initial Setup ===="

# ------------------------------------------------------------------
# 1.  Workspace boot-strapping
# ------------------------------------------------------------------
WORKSPACE="$HOME/vscode_cli_help_task"
DOCS_DIR="$WORKSPACE/docs"

echo "Creating fresh workspace at: $WORKSPACE"
rm -rf  "$WORKSPACE"
mkdir -p "$DOCS_DIR"

# README so the Explorer isn’t empty
cat > "$WORKSPACE/README.md" <<'EOF'
# VS Code CLI-Help Capture Task

Goal: open a terminal, execute

    code --help > ./docs/cli_help.txt

so the whole team has an up-to-date reference of all VS Code CLI
options shipped with VS Code 1.83.0 on Ubuntu 22.04.
EOF

# Drop a task marker that graders can look at quickly
echo "Run: code --help > ./docs/cli_help.txt" > "$WORKSPACE/.task_info.txt"

# ------------------------------------------------------------------
# 2.  Optional helper – a VS Code task the user could run (shown in UI)
# ------------------------------------------------------------------
mkdir -p "$WORKSPACE/.vscode"
cat > "$WORKSPACE/.vscode/tasks.json" <<'EOF'
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Capture VS Code CLI Help",
      "type": "shell",
      "command": "code --help > ./docs/cli_help.txt",
      "problemMatcher": []
    }
  ]
}
EOF

# ------------------------------------------------------------------
# 3.  Verification of initial state
# ------------------------------------------------------------------
if [[ -f "$DOCS_DIR/cli_help.txt" ]]; then
  echo "ERROR: docs/cli_help.txt already exists!  Aborting to keep task meaningful."
  exit 1
fi
echo "Verified: docs/cli_help.txt does NOT yet exist. Task is ready."

# ------------------------------------------------------------------
# 4.  Launch VS Code so the user can start working
# ------------------------------------------------------------------
echo "Opening workspace in VS Code..."
code "$WORKSPACE" &  # Runs in background so script can exit
sleep 2              # Give VS Code a moment to start

echo "Initial setup complete – user can now perform the task."
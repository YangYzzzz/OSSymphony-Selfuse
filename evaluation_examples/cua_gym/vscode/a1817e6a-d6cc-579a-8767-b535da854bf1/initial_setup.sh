#!/usr/bin/env bash
# initial_setup.sh
#
# Creates a workspace that is missing the required build task.
# The user must add a Ctrl+Shift+B task that overwrites
# task_output.txt with the text “VSCodeTask”.

set -euo pipefail

echo "===== VS Code shell-task INITIAL setup ====="

# 1. Workspace location
WORKSPACE="$HOME/vscode_shell_task"
echo "Using workspace: $WORKSPACE"

# 2. Re-create workspace from scratch
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/.vscode"

# 3. Seed project files
cat > "$WORKSPACE/README.md" << 'EOF'
# VS Code Shell Task Demo

Your goal: create a default *Build* task (Ctrl+Shift+B) that runs:

    echo 'VSCodeTask' > task_output.txt

When the task is executed it must create (or overwrite) task_output.txt
in the workspace root with exactly the text `VSCodeTask`.
EOF

# 4. Placeholder tasks.json (JSONC is allowed by VS Code)
cat > "$WORKSPACE/.vscode/tasks.json" << 'EOF'
{
  // VS Code 2.0.0 task schema
  "version": "2.0.0",
  "tasks": [
    // TODO: Add a default build task here
  ]
}
EOF

# 5. Task marker for graders / users
echo "Add a default build task that writes VSCodeTask into task_output.txt" \
  > "$WORKSPACE/.task_info.txt"

# 6. Verification — ensure the final command is NOT present yet
if grep -q "VSCodeTask" "$WORKSPACE/.vscode/tasks.json"; then
  echo "ERROR: tasks.json already contains final command; aborting." >&2
  exit 1
fi
echo "Verified that tasks.json still needs to be completed."

# 7. Open VS Code
echo "Opening VS Code..."
code "$WORKSPACE" & disown

echo "===== Initial setup complete. ====="
#!/usr/bin/env bash
###############################################################################
# 01_initial_setup.sh
# Sets up a workspace that **requires** the user to create a build task
# (Ctrl+Shift+B) which writes the running VS Code version to .vscode/version.txt
###############################################################################
set -euo pipefail

echo "===== VS Code Version-Task  |  Initial Setup ====="

# ---------------------------------------------------------------------------
# 1. Workspace skeleton
# ---------------------------------------------------------------------------
WORKSPACE="$HOME/vscode_version_task"
echo "Creating fresh workspace at: $WORKSPACE"
rm -rf  "$WORKSPACE"
mkdir -p "$WORKSPACE/.vscode"

# Simple project files so the folder looks realistic
cat > "$WORKSPACE/main.py" <<'EOF'
def hello():
    print("Hello VS Code task demo!")
if __name__ == "__main__":
    hello()
EOF

# ---------------------------------------------------------------------------
# 2. Provide a minimal (empty) tasks.json so that Ctrl+Shift+B prompts
# ---------------------------------------------------------------------------
cat > "$WORKSPACE/.vscode/tasks.json" <<'EOF'
{
    // TODO: Create a build task that writes VS Code version
    "version": "2.0.0",
    "tasks": []
}
EOF
echo "Minimal tasks.json created"

# ---------------------------------------------------------------------------
# 3. Clear any existing version.txt so the task is obviously missing
# ---------------------------------------------------------------------------
rm -f "$WORKSPACE/.vscode/version.txt"

# ---------------------------------------------------------------------------
# 4. Task instruction marker for the learner / evaluator
# ---------------------------------------------------------------------------
cat > "$WORKSPACE/TASK_INSTRUCTIONS.txt" <<'EOF'
TASK: Configure a default 'build' task (Ctrl+Shift+B) that
runs:
  code --version | head -n1 > .vscode/version.txt
Result: Every time you press Ctrl+Shift+B, .vscode/version.txt
        should contain the first line of `code --version`
EOF

echo "Instruction file created"

# ---------------------------------------------------------------------------
# 5. Open VS Code on the workspace
# ---------------------------------------------------------------------------
echo "Opening VS Code..."
code "$WORKSPACE" &

echo "===== Initial environment ready ====="
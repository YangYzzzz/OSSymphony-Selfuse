#!/usr/bin/env bash
# ------------------------------------------------------------------
# Initial workspace preparation for “extensions.json recommendation”
# task.  The user will need to add the required extension ID/version.
# ------------------------------------------------------------------
set -euo pipefail

echo "🔧  Preparing initial VS Code workspace…"

# ------------------------------------------------------------------
# 1. Workspace skeleton
# ------------------------------------------------------------------
WORKSPACE="$HOME/python_extension_task"
if [[ -d "$WORKSPACE" ]]; then
    echo "⚠️  Removing old workspace at $WORKSPACE"
    rm -rf "$WORKSPACE"
fi

mkdir -p "$WORKSPACE/.vscode"
mkdir -p "$WORKSPACE/src"

# Sample project content
cat > "$WORKSPACE/README.md" <<'EOF'
# Python Extension Task

Clone this repo and make sure VS Code recommends the required Python
extension (specific version) to every collaborator.
EOF

cat > "$WORKSPACE/src/main.py" <<'EOF'
def hello():
    print("Hello, VS Code!")

if __name__ == "__main__":
    hello()
EOF

# ------------------------------------------------------------------
# 2. Deliberately missing / placeholder extensions.json
# ------------------------------------------------------------------
cat > "$WORKSPACE/.vscode/extensions.json" <<'EOF'
{
  // TODO: Add extension recommendations here
}
EOF

# ------------------------------------------------------------------
# 3. Task instructions for the learner
# ------------------------------------------------------------------
cat > "$WORKSPACE/.task_info.txt" <<'EOF'
VS CODE TASK:
Create/replace .vscode/extensions.json with the exact content

{
  "recommendations": [
    "ms-python.python@2024.5.11081006"
  ]
}

so that every collaborator is prompted to install that specific
Python extension version.
EOF

echo "📝  Task instructions written to $WORKSPACE/.task_info.txt"

# ------------------------------------------------------------------
# 4. Verification of initial state
# ------------------------------------------------------------------
if grep -q "ms-python.python@2024.5.11081006" "$WORKSPACE/.vscode/extensions.json"; then
    echo "❌  ERROR: Required extension already present in initial state."
    exit 1
fi
echo "✅  Verified: required extension NOT present yet (good)."

# ------------------------------------------------------------------
# 5. Open VS Code
# ------------------------------------------------------------------
echo "🚀  Opening VS Code.  Perform the task there."
code "$WORKSPACE" &

echo "Initial setup complete."
#!/usr/bin/env bash
# File: /tmp/initial_setup.sh
# Purpose: Prepare a Python project that still needs
#          1) tests folder added to the workspace
#          2) .pytest_cache hidden in Explorer

set -euo pipefail

echo "========== Initial VS Code task setup =========="

# ------------------------------------------------------------------
# 1. Create the real project folders EXACTLY as requested
# ------------------------------------------------------------------
echo "Creating project folders and sample files ..."

mkdir -p "/home/user/src"
mkdir -p "/home/user/tests"
mkdir -p "/home/user/src/.pytest_cache"     # clutter to be hidden later

cat > "/home/user/src/main.py" <<'EOF'
def add(a, b):
    return a + b

if __name__ == "__main__":
    print("2 + 3 =", add(2, 3))
EOF

cat > "/home/user/tests/test_main.py" <<'EOF'
from src.main import add

def test_add():
    assert add(2, 3) == 5
EOF

echo "Sample project files created."

# ------------------------------------------------------------------
# 2. Create an *incomplete* multi-root workspace
#    - At first it ONLY contains /home/user/src
#    - No rule yet to hide .pytest_cache
# ------------------------------------------------------------------
WORKSPACE_FILE="/home/user/my_python_project.code-workspace"

cat > "${WORKSPACE_FILE}" <<'EOF'
{
  "folders": [
    { "path": "/home/user/src" }
  ],
  "settings": {
    "files.exclude": {
      "**/.git": true,
      "**/.DS_Store": true
    }
  }
}
EOF

echo "Workspace created at ${WORKSPACE_FILE}"

# ------------------------------------------------------------------
# 3. Quick verification of the initial state
# ------------------------------------------------------------------
echo "Verifying initial workspace state ..."
if grep -q "/home/user/src" "$WORKSPACE_FILE" && ! grep -q "/home/user/tests" "$WORKSPACE_FILE"; then
    echo "✅  Only /home/user/src present in workspace (expected)"
else
    echo "❌  Workspace verification failed!"
    exit 1
fi

if ! grep -q ".pytest_cache" "$WORKSPACE_FILE"; then
    echo "✅  .pytest_cache NOT yet excluded (expected)"
else
    echo "❌  .pytest_cache already excluded – this should be added by the user later."
    exit 1
fi

# ------------------------------------------------------------------
# 4. Open VS Code so the user can perform the task
# ------------------------------------------------------------------
echo "Opening VS Code..."
code "${WORKSPACE_FILE}" &

echo "========== Initial setup complete =========="
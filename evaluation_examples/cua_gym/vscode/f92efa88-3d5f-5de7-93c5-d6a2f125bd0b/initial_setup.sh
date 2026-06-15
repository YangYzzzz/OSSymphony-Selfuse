#!/usr/bin/env bash
# -----------------------------------------------
#  VS Code Task  ▸  Initial State Preparation
#  Goal: create a project that is littered with
#        “.pytest_cache” folders that are fully
#        visible in the VS Code Explorer.
# -----------------------------------------------
set -euo pipefail

echo "🔧  Preparing initial workspace with visible .pytest_cache folders …"

# ---------- 1. Create workspace skeleton ----------
WORKSPACE="/home/user/projects/my_app"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE"/{src,tests/unit,tests/integration}
mkdir -p "$WORKSPACE/.vscode"

# ---------- 2. Populate project files ----------
cat > "$WORKSPACE/README.md" << 'EOF'
# my_app
Sample project to demonstrate hiding `.pytest_cache` folders in VS Code.
EOF

cat > "$WORKSPACE/src/app.py" << 'EOF'
def add(a, b):
    """Simple add function."""
    return a + b
EOF

cat > "$WORKSPACE/tests/unit/test_app.py" << 'EOF'
from src.app import add

def test_add():
    assert add(2, 3) == 5
EOF

# ---------- 3. Simulate pytest runs (create caches) ----------
echo "📁  Sprinkling .pytest_cache directories …"
for DIR in "$WORKSPACE" "$WORKSPACE/tests" "$WORKSPACE/tests/unit" "$WORKSPACE/tests/integration"
do
  mkdir -p "$DIR/.pytest_cache/v/cache"
  echo '{"version": "1.0"}' > "$DIR/.pytest_cache/metadata.json"
done

# ---------- 4. Workspace settings (none set yet) ----------
cat > "$WORKSPACE/.vscode/settings.json" << 'EOF'
{
  // Nothing excluded yet. .pytest_cache will be visible!
}
EOF

# ---------- 5. Verification ----------
echo "✅  Verifying that .pytest_cache folders exist:"
find "$WORKSPACE" -type d -name ".pytest_cache"

# ---------- 6. Open VS Code ----------
echo "🚀  Launching VS Code…"
code "$WORKSPACE" &

echo "📝  Task for the user:"
echo "   In VS Code, hide all '.pytest_cache' folders from the Explorer."
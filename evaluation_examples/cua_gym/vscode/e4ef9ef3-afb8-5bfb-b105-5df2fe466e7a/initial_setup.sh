#!/usr/bin/env bash
set -euo pipefail

echo "========== Initial VS Code task setup =========="

# 1. Re-create CLEAN workspace ------------------------------------------------
WS="/home/user/webapp"
echo "Rebuilding workspace at: $WS"
rm -rf "$WS"
mkdir -p "$WS"

# 2. Create a realistic Python project ----------------------------------------
mkdir -p "$WS/app" "$WS/tests"

cat > "$WS/app/main.py" << 'PY'
def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    print("3 + 4 =", add(3, 4))
PY

cat > "$WS/tests/test_add.py" << 'PY'
from app.main import add

def test_add():
    assert add(2, 5) == 7
PY

# Simulate mypy runs that generated cache directories
for d in "$WS" "$WS/app" "$WS/tests"; do
    mkdir -p "$d/.mypy_cache"
    echo "Dummy cache file" > "$d/.mypy_cache/metadata.json"
done
echo "Created .mypy_cache directories to clutter the Explorer."

# 3. Add a minimal VS Code configuration (NO exclusions yet) ------------------
mkdir -p "$WS/.vscode"
cat > "$WS/.vscode/settings.json" << 'EOF'
{
  // Workspace settings (no cache exclusion yet)
  "python.analysis.typeCheckingMode": "basic"
}
EOF
echo "Initial settings.json written (without .mypy_cache exclusion)."

# 4. Verification -------------------------------------------------------------
echo "Verifying initial state..."
if grep -q "\"**/.mypy_cache\"" "$WS/.vscode/settings.json"; then
    echo "ERROR: Exclusion already present – something is wrong."
    exit 1
else
    echo "OK: settings.json does NOT yet hide .mypy_cache (expected)."
fi

echo "Listing found cache dirs:"
find "$WS" -type d -name ".mypy_cache" -print

# 5. Open VS Code -------------------------------------------------------------
echo "Opening VS Code..."
code "$WS" &

echo "========== Setup complete – User should now HIDE '.mypy_cache' =========="
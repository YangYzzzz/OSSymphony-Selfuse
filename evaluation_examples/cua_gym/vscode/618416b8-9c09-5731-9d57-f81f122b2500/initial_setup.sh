#!/usr/bin/env bash
# initial_setup.sh
#
# Prepares a realistic starting point where the VS Code workspace
# contains ONLY the “src” folder.  
# The learner must add “/home/user/src” and “/home/user/tests” to the
# workspace.

set -euo pipefail

echo "========================"
echo " Initial VS Code Task Setup "
echo "========================"

# 1. Create project directory structure
echo "Creating project directories ..."
mkdir -p /home/user/src
mkdir -p /home/user/tests

# 2. Add sample files
echo "Populating sample files ..."
cat > /home/user/src/main.py <<'PY'
def add(a, b):
    return a + b

if __name__ == "__main__":
    print("2 + 3 =", add(2, 3))
PY

cat > /home/user/tests/test_main.py <<'PY'
from src.main import add

def test_add():
    assert add(2, 3) == 5
PY

# 3. Create an **empty** (almost) workspace that only contains the src folder
WORKSPACE_FILE="/home/user/project.code-workspace"
echo "Creating initial workspace file at ${WORKSPACE_FILE} ..."
cat > "${WORKSPACE_FILE}" <<'JSON'
{
  "folders": [
    {
      "path": "/home/user/src"
    }
  ],
  "settings": {
    "python.testing.unittestArgs": [
      "-v",
      "-s",
      "/home/user/tests",
      "-p",
      "test_*.py"
    ],
    "python.testing.pytestEnabled": false,
    "python.testing.unittestEnabled": true
  }
}
JSON

# 4. Verification ‑ ensure ONLY /home/user/src is present
if command -v jq >/dev/null 2>&1; then
  COUNT=$(jq '.folders | length' "${WORKSPACE_FILE}")
  if [[ "${COUNT}" -ne 1 ]]; then
    echo "ERROR: Expected exactly one folder in workspace; found ${COUNT}"
    exit 1
  fi
  FIRST_PATH=$(jq -r '.folders[0].path' "${WORKSPACE_FILE}")
  if [[ "${FIRST_PATH}" != "/home/user/src" ]]; then
    echo "ERROR: Unexpected initial folder path: ${FIRST_PATH}"
    exit 1
  fi
  echo "Verification passed: Workspace currently contains ONLY /home/user/src"
else
  echo "WARNING: jq not found; skipping JSON verification."
fi

# 5. Task hint
echo "Add BOTH '/home/user/src' and '/home/user/tests' to this workspace." \
  > /home/user/.task_info.txt

# 6. Open VS Code with the workspace
echo "Launching VS Code ..."
code "/home/user/project.code-workspace" &

echo "Initial setup complete. VS Code is ready."
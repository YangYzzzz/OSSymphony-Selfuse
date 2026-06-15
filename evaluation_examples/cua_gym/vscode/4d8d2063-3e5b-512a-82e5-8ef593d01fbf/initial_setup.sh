#!/usr/bin/env bash
# initial_setup.sh
# Purpose: Prepare a JS workspace that still needs a Jest test file to be written
set -euo pipefail

echo "==============================================="
echo " VS Code Jest Task – Initial Setup"
echo "==============================================="

# --------------------------------------------------------------------
# 1. Workspace skeleton
# --------------------------------------------------------------------
WORKSPACE="$HOME/vscode_jest_task"
echo "Creating (or refreshing) workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"

# --------------------------------------------------------------------
# 2. Simple application code
# --------------------------------------------------------------------
cat > "$WORKSPACE/src/index.js" <<'EOF'
/**
 * Very small sample function so we have something to test.
 */
function add(a, b) {
  return a + b;
}

module.exports = { add };
EOF
echo "Created sample source file: src/index.js"

# --------------------------------------------------------------------
# 3. Node / Jest scaffolding
# --------------------------------------------------------------------
cat > "$WORKSPACE/package.json" <<'EOF'
{
  "name": "jest-sample-project",
  "version": "1.0.0",
  "description": "Demo workspace for VS Code Jest Runner task",
  "main": "src/index.js",
  "scripts": {
    "test": "jest"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}
EOF
echo "Created package.json (Jest declared as devDependency)"

# --------------------------------------------------------------------
# 4. VS Code configuration & extension recommendation
# --------------------------------------------------------------------
mkdir -p "$WORKSPACE/.vscode"
cat > "$WORKSPACE/.vscode/extensions.json" <<'EOF'
{
  "recommendations": ["firsttris.vscode-jest-runner"]
}
EOF
echo "Added .vscode/extensions.json (recommends Jest Runner)"

# Optionally tweak Jest Runner settings (not required, but realistic)
cat > "$WORKSPACE/.vscode/settings.json" <<'EOF'
{
  "jest.runAllTestsFirst": false,
  "jest.autoRun": "off"
}
EOF
echo "Added .vscode/settings.json"

# --------------------------------------------------------------------
# 5. Task marker for learner
# --------------------------------------------------------------------
cat > "$WORKSPACE/.task_info.txt" <<'EOF'
TASK: Inside the workspace create a new folder "src/__tests__"
      Add a file "sample.test.js" containing at least two basic Jest tests.
      Example template is in the README.
EOF

cat > "$WORKSPACE/README.md" <<'EOF'
# VS Code Jest Runner Task

Your goal:

1. Create `src/__tests__/sample.test.js`
2. Add **two** Jest test cases that call the `add` function from `src/index.js`.

Example:
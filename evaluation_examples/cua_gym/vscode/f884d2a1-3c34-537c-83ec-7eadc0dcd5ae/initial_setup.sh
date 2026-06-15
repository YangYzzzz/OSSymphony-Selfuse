#!/usr/bin/env bash
# 01_initial_setup.sh
# Purpose: Create a workspace that still uses console.log so the user must replace it with print.
set -euo pipefail

echo "==============   INITIAL TASK SETUP   =============="

# Absolute workspace path specified in the task
WORKSPACE="/home/user/workspace"
UTILS_FILE="$WORKSPACE/utils.js"

echo "Preparing fresh workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE"

echo "Creating utils.js that contains console.log statements..."
cat > "$UTILS_FILE" << 'EOF'
/**
 * Utility helpers
 */

function greet(name) {
  console.log('Hello ' + name);
}

function sum(a, b) {
  console.log('Calculating sum...');
  return a + b;
}

// Trigger immediately
console.log('Utils loaded');
EOF

echo "Creating a minimal README.md..."
cat > "$WORKSPACE/README.md" << 'EOF'
# VS Code Task – Find & Replace
Follow the instruction in `.task_info.txt`.
EOF

echo "Writing task instruction marker (.task_info.txt)..."
echo "Replace every instance of console.log with print in utils.js" > "$WORKSPACE/.task_info.txt"

echo "Verifying initial state (utils.js should contain console.log)..."
if grep -q "console.log" "$UTILS_FILE"; then
  echo "✅  Verification passed – console.log found."
else
  echo "❌  Verification failed – console.log NOT found."
  exit 1
fi

echo "Opening VS Code..."
code "$WORKSPACE" &

echo "Workspace is ready. Perform the replacement in VS Code."
sleep 2
#!/usr/bin/env bash
set -euo pipefail

echo "=== VS Code npm-debug task – Initial state ==="

# 1) Create workspace skeleton -------------------------------------------------
WORKSPACE="$HOME/npm_debug_task"
echo "Creating/refreshing workspace at: $WORKSPACE"
rm -rf  "$WORKSPACE"
mkdir -p "$WORKSPACE/src" "$WORKSPACE/.vscode"

# 2) Populate project files ----------------------------------------------------
cat > "$WORKSPACE/src/server.js" << 'EOF'
const http = require('http');
const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  res.end('Hello World – hit a breakpoint here!');
});

server.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
EOF

cat > "$WORKSPACE/package.json" << 'EOF'
{
  "name": "debug-sample",
  "version": "1.0.0",
  "description": "Minimal Node.js server for VS Code debug task",
  "main": "src/server.js",
  "scripts": {
    "dev": "node src/server.js"
  },
  "author": "VS Code Task Generator",
  "license": "MIT"
}
EOF

# 3) Workspace hint file (optional) -------------------------------------------
echo "Add .vscode/launch.json that launches npm -> dev so F5 hits breakpoints" \
     > "$WORKSPACE/TODO_add_launch_json.txt"

# 4) Verification --------------------------------------------------------------
echo "Verifying initial state …"
if [[ ! -f "$WORKSPACE/.vscode/launch.json" ]]; then
  echo "✓ launch.json intentionally missing (task yet to be done)"
else
  echo "✗ launch.json already exists (should not for initial state)" && exit 1
fi

# 5) Open VS Code --------------------------------------------------------------
echo "Opening VS Code in initial task state …"
code "$WORKSPACE" &>/dev/null &
sleep 2
echo "Initial state ready – create launch.json via VS Code GUI."
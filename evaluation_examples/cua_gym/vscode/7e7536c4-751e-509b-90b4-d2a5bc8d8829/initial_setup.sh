#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial Setup Script
# Purpose  : Simulate a freshly-pulled mono-repo that contains “frontend/”
#            and “backend/”.  VS Code will open at the repo root so the user
#            still has to drill down and open /home/user/workspace/frontend.
###############################################################################

echo "==> Preparing initial VS Code task environment…"

# 1. Verify VS Code CLI is available
if ! command -v code >/dev/null 2>&1; then
    echo "ERROR: The 'code' CLI command was not found in PATH." >&2
    exit 1
fi

# 2. Create realistic mono-repo structure
REPO_ROOT="/home/user/workspace"
FRONTEND_DIR="$REPO_ROOT/frontend"
BACKEND_DIR="$REPO_ROOT/backend"

echo "==> Creating repo directory: $REPO_ROOT"
# Remove any pre-existing directory to guarantee a clean start
rm -rf "$REPO_ROOT"
mkdir -p "$FRONTEND_DIR" "$BACKEND_DIR"

# 3. Populate FRONTEND with starter UI code
cat > "$FRONTEND_DIR/index.html" <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Fresh UI</title>
</head>
<body>
    <div id="root"></div>
    <script src="main.js"></script>
</body>
</html>
EOF

cat > "$FRONTEND_DIR/main.js" <<'EOF'
console.log('Welcome to the fresh UI!');
EOF

# 4. Populate BACKEND with a simple API stub
cat > "$BACKEND_DIR/server.js" <<'EOF'
const http = require('http');
http.createServer((_, res) => {
    res.end('API running');
}).listen(8000, () => console.log('Server on :8000'));
EOF

# 5. Optional README to make repo look real
cat > "$REPO_ROOT/README.md" <<'EOF'
# Sample Monorepo

- frontend/ → UI code
- backend/  → API code
EOF

# 6. Task marker to remind the human what to do
echo "Open the /home/user/workspace/frontend folder in VS Code" \
    > "$REPO_ROOT/.task_info.txt"

# 7. Open VS Code **at repo root** (NOT yet inside frontend)
echo "==> Launching VS Code at $REPO_ROOT (root of repo)…"
code "$REPO_ROOT" &

echo "==> Initial environment ready.  VS Code is open at the repo root."
echo "   - Your task: use the GUI to open the 'frontend' folder."
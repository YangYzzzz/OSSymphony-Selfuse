#!/usr/bin/env bash
# ------------------------------------------------------------------
# Initial Setup Script
#   - Creates a realistic website workspace at /home/user/web
#   - Leaves out the required css/styles.css file
#   - Opens VS Code so the user can add the missing stylesheet
# ------------------------------------------------------------------
set -euo pipefail

echo "[INIT] Preparing initial workspace..."

WORKSPACE="/home/user/web"
CSS_DIR="$WORKSPACE/css"
STYLESHEET="$CSS_DIR/styles.css"

# 1. Clean-slate workspace ----------------------------------------------------
if [ -d "$WORKSPACE" ]; then
    echo "[INIT] Removing existing workspace at $WORKSPACE"
    rm -rf "$WORKSPACE"
fi

# 2. Re-create project structure ---------------------------------------------
echo "[INIT] Creating project directories..."
mkdir -p "$CSS_DIR"            # css folder (empty for now)
mkdir -p "$WORKSPACE/js"       # js folder for realism
mkdir -p "$WORKSPACE/.vscode"  # VS Code workspace settings folder

# 3. Populate starter files ---------------------------------------------------
echo "[INIT] Generating starter HTML and JS..."
cat > "$WORKSPACE/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My New Website</title>
    <!-- Stylesheet intentionally missing -->
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <h1>Welcome to my new site!</h1>
    <script src="js/main.js"></script>
</body>
</html>
EOF

cat > "$WORKSPACE/js/main.js" << 'EOF'
console.log("Website JS loaded. Style me up!");
EOF

# 4. Add a task marker so the user sees what to do ----------------------------
echo "TODO: Create css/styles.css inside /home/user/web/css" > "$WORKSPACE/.task_info.txt"

# 5. Verification -------------------------------------------------------------
echo "[INIT] Verifying that stylesheet does NOT exist..."
if [ ! -f "$STYLESHEET" ]; then
    echo "[INIT] Verification passed: $STYLESHEET is absent (as expected)."
else
    echo "[INIT] Unexpected: $STYLESHEET already exists!"
    exit 1
fi

# 6. Open the workspace in VS Code -------------------------------------------
echo "[INIT] Opening VS Code..."
code "$WORKSPACE" &

echo "[INIT] Setup complete. VS Code is ready for you to create styles.css."
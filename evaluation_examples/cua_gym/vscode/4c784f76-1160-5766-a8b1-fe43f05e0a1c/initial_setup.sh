#!/usr/bin/env bash
set -euo pipefail

echo "=== Initial VS Code task setup: CSS indent fix ==="

# -----------------------------------------------------------------------------
# 1. Create the exact workspace path
# -----------------------------------------------------------------------------
WORKSPACE="/home/user/portfolio"
CSS_FILE="$WORKSPACE/style.css"

echo "Creating workspace directory: $WORKSPACE"
mkdir -p "$WORKSPACE"

# -----------------------------------------------------------------------------
# 2. Generate a CSS file whose first five lines sit flush-left (no indent)
#    while the remainder of the file is already indented with three spaces.
# -----------------------------------------------------------------------------
cat > "$CSS_FILE" << 'EOF'
body {
background-color: #f0f0f0;
color: #333;
font-family: 'Helvetica', sans-serif;
margin: 0;
   padding: 0;
   display: flex;
   justify-content: center;
   align-items: center;
   height: 100vh;
}
EOF
echo "Created CSS file with mixed indentation: $CSS_FILE"

# -----------------------------------------------------------------------------
# 3. Quick verification – show line numbers & leading spaces count
# -----------------------------------------------------------------------------
echo ">>> Showing first 10 lines with visible spaces"
nl -ba "$CSS_FILE" | sed -e 's/ /·/g' | head -10

# -----------------------------------------------------------------------------
# 4. Open VS Code pointed at the workspace
# -----------------------------------------------------------------------------
echo "Opening VS Code..."
code "$WORKSPACE" &

echo "=== Initial setup complete ==="
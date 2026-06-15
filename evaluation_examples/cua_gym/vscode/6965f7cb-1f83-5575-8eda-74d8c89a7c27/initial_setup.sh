#!/usr/bin/env bash
# Purpose: Prepare workspace so the user needs to create /assets/css/styles.css with brand colours
set -euo pipefail

echo "========== Initial Live-Server CSS Task Setup =========="

# ------------------------------------------------------------------
# 1. Create a brand-new workspace
# ------------------------------------------------------------------
WORKSPACE="$HOME/live_server_css_task"
echo "Creating workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/assets/css"          # directory exists, file does NOT

# ------------------------------------------------------------------
# 2. Seed project files
# ------------------------------------------------------------------
cat > "$WORKSPACE/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Brand Colours Demo</title>

  <!-- Live Server will auto-refresh when /assets/css/styles.css is created/edited -->
  <link rel="stylesheet" href="assets/css/styles.css" />

  <script>
    // Quick visual indicator to prove a reload happens
    document.addEventListener('DOMContentLoaded', () =>
      console.log('Page loaded at', new Date().toLocaleTimeString())
    );
  </script>
</head>
<body>
  <h1>Welcome to the brand!</h1>
  <p>Open with Live Server and add your brand colours in <code>styles.css</code>.</p>
</body>
</html>
EOF
echo "index.html created"

# ------------------------------------------------------------------
# 3. Recommend the Live Server extension
# ------------------------------------------------------------------
mkdir -p "$WORKSPACE/.vscode"
cat > "$WORKSPACE/.vscode/extensions.json" << 'EOF'
{
  "recommendations": ["ritwickdey.LiveServer"]
}
EOF
echo "Extension recommendation added"

# ------------------------------------------------------------------
# 4. Leave a task hint
# ------------------------------------------------------------------
cat > "$WORKSPACE/.task_info.txt" << 'EOF'
TASK: In VS Code create /assets/css/styles.css with:

:root {
  --primary: #0d6efd;
  --secondary: #6c757d;
  --accent: #f39c12;
}

Save the file. If Live Server is running the browser should auto-refresh.
EOF
echo "Task hint written"

# ------------------------------------------------------------------
# 5. Quick verification of initial state
# ------------------------------------------------------------------
if [ -f "$WORKSPACE/assets/css/styles.css" ]; then
  echo "ERROR: styles.css already exists — should not be present" >&2
  exit 1
else
  echo "Verification OK: styles.css is NOT present (as expected)"
fi

# ------------------------------------------------------------------
# 6. Launch VS Code
# ------------------------------------------------------------------
echo "Opening VS Code…"
code "$WORKSPACE" &>/dev/null &

echo "Setup complete — user can now start Live Server (Alt+L Alt+O) and create styles.css."
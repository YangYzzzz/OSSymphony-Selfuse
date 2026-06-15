#!/usr/bin/env bash
# File: setup_initial.sh
set -euo pipefail

echo "=== VS Code Task (Initial State) ==="
echo "Goal for the learner: 1) Switch VS Code to French. 2) Create /home/user/web/styles/theme.css"
echo

###############################################################################
# 1. Sanity checks
###############################################################################
if ! command -v code >/dev/null 2>&1 ; then
  echo "ERROR: VS Code CLI ('code') not found in PATH."
  exit 1
fi

###############################################################################
# 2. Prepare workspace content
###############################################################################
WORKSPACE_PATH="/home/user/web"
STYLE_DIR="$WORKSPACE_PATH/styles"
THEME_FILE="$STYLE_DIR/theme.css"

echo "Creating workspace directory: $WORKSPACE_PATH"
mkdir -p "$STYLE_DIR"

# Remove theme.css if it already exists so the learner must create it.
if [ -f "$THEME_FILE" ]; then
  echo "Removing pre-existing theme.css so the task is required…"
  rm -f "$THEME_FILE"
fi

# Simple HTML scaffold
cat > "$WORKSPACE_PATH/index.html" <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sample Website</title>
    <link rel="stylesheet" href="styles/theme.css">
</head>
<body>
    <h1>Welcome</h1>
</body>
</html>
EOF
echo "Created index.html"

###############################################################################
# 3. Force VS Code interface to English
###############################################################################
VSCODE_USER_DIR="$HOME/.config/Code/User"
LOCALE_FILE="$VSCODE_USER_DIR/locale.json"
mkdir -p "$VSCODE_USER_DIR"

cat > "$LOCALE_FILE" <<'EOF'
{
    "locale": "en"
}
EOF
echo "Locale set to English (en) in $LOCALE_FILE"

###############################################################################
# 4. Task hint file inside workspace (purely informational)
###############################################################################
echo "TASK: Switch VS Code interface to French and create /home/user/web/styles/theme.css" \
  > "$WORKSPACE_PATH/.task_info.txt"

###############################################################################
# 5. Verify initial state
###############################################################################
echo "Verifying initial state…"
grep -q '"locale": "en"' "$LOCALE_FILE" && echo "✓ Locale is English"
[ ! -f "$THEME_FILE" ] && echo "✓ theme.css does NOT exist yet"
echo

###############################################################################
# 6. Launch VS Code
###############################################################################
echo "Opening VS Code…"
code "$WORKSPACE_PATH" &

echo "Initial setup complete – VS Code should appear in English and without theme.css."
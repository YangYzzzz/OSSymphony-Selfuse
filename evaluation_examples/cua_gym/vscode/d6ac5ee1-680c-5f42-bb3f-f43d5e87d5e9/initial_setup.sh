#!/usr/bin/env bash
# =============================================================================
# VS Code Display-Language Task : INITIAL STATE
# -----------------------------------------------------------------------------
# Creates a workspace with VS Code currently set to English.  
# The user’s task will be to switch the display language to Spanish.
# =============================================================================
set -euo pipefail

echo "🔧  Preparing initial VS Code language configuration task ..."

# ----------------------------------------------------------------------------- 
# 1. Define paths
# -----------------------------------------------------------------------------
WORKSPACE="$HOME/vscode_language_task"
VSCODE_USER_DIR="$HOME/.config/Code/User"       # Linux & WSL default
LOCALE_FILE="$VSCODE_USER_DIR/locale.json"

# ----------------------------------------------------------------------------- 
# 2. Clean up any previous runs
# -----------------------------------------------------------------------------
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE"
mkdir -p "$VSCODE_USER_DIR"

# ----------------------------------------------------------------------------- 
# 3. Create sample project content
# -----------------------------------------------------------------------------
cat > "$WORKSPACE/README.md" << 'EOF'
# Language Switch Demo

Open VS Code and change the entire UI language to Spanish ("Español").
EOF

# ----------------------------------------------------------------------------- 
# 4. Force VS Code locale to English (initial state)
# -----------------------------------------------------------------------------
cat > "$LOCALE_FILE" << 'EOF'
{
  "locale": "en"
}
EOF
echo "✅  locale.json set to English: $LOCALE_FILE"

# ----------------------------------------------------------------------------- 
# 5. Make sure Spanish language pack is NOT installed (optional clean-up)
# -----------------------------------------------------------------------------
if code --list-extensions | grep -qi 'MS-CEINTL.vscode-language-pack-es'; then
  echo "⚠️  Spanish language pack found – removing for clean start ..."
  code --uninstall-extension MS-CEINTL.vscode-language-pack-es || true
fi

# ----------------------------------------------------------------------------- 
# 6. Write a task hint file for the user
# -----------------------------------------------------------------------------
echo "Task: Switch VS Code interface to Spanish" > "$WORKSPACE/.task_info.txt"

# ----------------------------------------------------------------------------- 
# 7. Verification of initial state
# -----------------------------------------------------------------------------
if grep -q '"locale": "en"' "$LOCALE_FILE"; then
  echo "✅  Verification passed – locale is EN."
else
  echo "❌  Verification failed – locale is NOT EN." >&2
  exit 1
fi

# ----------------------------------------------------------------------------- 
# 8. Launch VS Code
# -----------------------------------------------------------------------------
echo "🚀  Opening workspace in VS Code ..."
code "$WORKSPACE" &

echo "🏁  Initial setup complete – VS Code should start in English."
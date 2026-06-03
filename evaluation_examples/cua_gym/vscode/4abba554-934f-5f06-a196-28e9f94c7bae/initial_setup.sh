#!/usr/bin/env bash
# Purpose : Prepare a VS Code workspace where the UI language is explicitly set to English.
# The learner’s task will be to switch the editor’s display language to Italian.
set -euo pipefail

echo "========================"
echo "VS Code Language Task  – Initial Setup"
echo "========================"

# --------------------------------------------------
# 1. Detect the correct VS Code user-settings path
# --------------------------------------------------
if [[ "$OSTYPE" == "darwin"* ]]; then
  CODE_USER_DIR="$HOME/Library/Application Support/Code/User"
else
  CODE_USER_DIR="$HOME/.config/Code/User"
fi
mkdir -p "$CODE_USER_DIR"

# --------------------------------------------------
# 2. Force the UI locale to English
# --------------------------------------------------
cat > "$CODE_USER_DIR/locale.json" << 'EOF'
{
  "locale": "en"
}
EOF
echo "locale.json written with locale = 'en'  ➜ $CODE_USER_DIR/locale.json"

# --------------------------------------------------
# 3. Make sure the Italian Language Pack is NOT installed
#    (ignore errors if it was never installed)
# --------------------------------------------------
if command -v code >/dev/null 2>&1 ; then
  code --uninstall-extension MS-CEINTL.vscode-language-pack-it --force || true
  echo "Ensured Italian language pack is uninstalled."
else
  echo "ERROR: 'code' CLI not found in PATH."
  exit 1
fi

# --------------------------------------------------
# 4. Create a small workspace so the user has something to open
# --------------------------------------------------
WORKSPACE="$HOME/vscode_language_task"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE"
cat > "$WORKSPACE/README.md" << 'EOF'
# VS Code Language Task

You need to change the editor's display language from English to *Italiano*.
EOF
echo "Workspace prepared at $WORKSPACE"

# --------------------------------------------------
# 5. Verification – confirm locale is currently EN
# --------------------------------------------------
CURRENT_LOCALE=$(jq -r '.locale' "$CODE_USER_DIR/locale.json")
if [[ "$CURRENT_LOCALE" == "en" ]]; then
  echo "Verification passed – UI is currently set to English."
else
  echo "Verification failed – expected 'en' but found '${CURRENT_LOCALE}'."
  exit 1
fi

# --------------------------------------------------
# 6. Open VS Code for the learner
# --------------------------------------------------
echo "Opening VS Code in ENGLISH…"
code "$WORKSPACE" &

echo "Initial setup complete. ✔"
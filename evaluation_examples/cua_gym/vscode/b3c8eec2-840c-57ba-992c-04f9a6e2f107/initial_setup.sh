#!/usr/bin/env bash
# -------------------------------------------------
#  VS Code Task – Initial State
#  Goal: Require user to switch VS Code UI to Russian
# -------------------------------------------------
set -euo pipefail

echo "-------------------------------------------------"
echo " Setting-up initial VS Code language task ..."
echo "-------------------------------------------------"

# 1.  Create a small workspace the user can open
WORKSPACE="$HOME/vscode_russian_locale_task"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE"
cat > "$WORKSPACE/README.md" <<'EOF'
# VS Code Language Task

Your new teammate only speaks Russian.
Switch the entire VS Code interface to **Russian**.
EOF

# 2.  Ensure USER settings force English (so the task is needed)
VSCODE_USER_DIR="$HOME/.config/Code/User"
mkdir -p "$VSCODE_USER_DIR"

# VS Code reads locale from User/locale.json (NOT settings.json)
cat > "$VSCODE_USER_DIR/locale.json" <<'EOF'
{
  "locale": "en"
}
EOF
echo "locale.json forced to English."

# 3.  Remove Russian language pack if it exists (best-effort)
if code --list-extensions | grep -q "MS-CEINTL.vscode-language-pack-ru"; then
    echo "Russian language pack already installed – removing for initial state."
    code --uninstall-extension "MS-CEINTL.vscode-language-pack-ru" || true
else
    echo "Russian language pack not present – OK."
fi

# 4.  Create a task marker for review purposes
echo "ACTION REQUIRED: Switch VS Code display language to Russian." \
     > "$WORKSPACE/.task_info.txt"

# 5.  Verification of initial state
echo "--------- Verification (Initial) ---------"
jq '.' "$VSCODE_USER_DIR/locale.json"
echo "Currently installed language packs:"
code --list-extensions | grep "language-pack" || echo "(none)"
echo "------------------------------------------"

# 6.  Launch VS Code
echo "Opening VS Code in EN locale – user must change to RU ..."
code "$WORKSPACE" &

echo "Initial environment ready."
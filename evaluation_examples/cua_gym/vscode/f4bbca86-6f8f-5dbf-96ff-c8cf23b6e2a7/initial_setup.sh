#!/usr/bin/env bash
# Purpose: Prepare a VS Code workspace whose current state
#          does NOT meet the style-guide requirement.
#          Theme = “Light+”, NO Python ruler.
#          Opens VS Code so the user can make the requested change.

set -euo pipefail

echo "=== VS Code Style-Guide Task – INITIAL STATE ==="

# 1) Define paths -------------------------------------------------------------
WORKSPACE="$HOME/vscode_styleguide_task"
CODE_USER_DIR="$HOME/.config/Code/User"           # Linux / WSL / container default
SETTINGS_FILE="$CODE_USER_DIR/settings.json"

# 2) Re-create a clean workspace ---------------------------------------------
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"
echo "print('This script violates our 100-column rule…')" > "$WORKSPACE/src/example.py"

# 3) Ensure VS Code user settings directory exists ---------------------------
mkdir -p "$CODE_USER_DIR"

# 4) Create a settings.json whose values FAIL the requirement ----------------
#    (Theme = Light+, no language-specific ruler)
cat > "$SETTINGS_FILE" <<'EOF'
{
  // --- Initial state created by setup_initial.sh ---
  "workbench.colorTheme": "Light+",
  "editor.fontSize": 15,
  "files.autoSave": "off"
}
EOF

echo "Created initial user settings:"
cat "$SETTINGS_FILE"

# 5) Verification ------------------------------------------------------------
echo "Verifying initial state..."
grep -q '"workbench.colorTheme": "Light+"' "$SETTINGS_FILE" && \
  echo "   ✔ Theme is Light+  (NOT the requested Dark+)" || \
  (echo "   ✘ Expected Light+, but found a different theme"; exit 1)

! grep -q '"\\[python\\]"' "$SETTINGS_FILE" && \
  echo "   ✔ No Python-specific ruler set (as expected)" || \
  (echo "   ✘ Python rulers already exist – this should not happen"; exit 1)

echo "Initial verification successful."

# 6) Open VS Code -------------------------------------------------------------
echo "Opening VS Code in: $WORKSPACE"
code "$WORKSPACE" &

echo "=== Ready – User must: 1) change theme to Dark+, 2) add a 100-column ruler for Python ==="
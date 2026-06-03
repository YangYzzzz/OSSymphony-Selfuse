#!/usr/bin/env bash
# ------------------------------------------------------------------
#  VS Code Theme Switch Task – Initial State
# ------------------------------------------------------------------
# 1. Creates a small workspace the learner will open in VS Code
# 2. Forces the editor to use the *Default Dark+* theme
# 3. Ensures the Atom One Dark theme extension is NOT enabled
# 4. Drops a task hint file
# 5. Opens VS Code so the user can carry out the task manually
# ------------------------------------------------------------------
set -euo pipefail

echo "----------------------------------------------------"
echo "Setting up INITIAL state for Atom One Dark task ..."
echo "----------------------------------------------------"

# ---------- 1. Create a simple workspace ----------
WORKSPACE="$HOME/vscode_atom_onedark_task"
if [[ -d "$WORKSPACE" ]]; then
    echo "Cleaning existing workspace: $WORKSPACE"
    rm -rf "$WORKSPACE"
fi
mkdir -p "$WORKSPACE/src"
echo 'print("Hello VS Code")' > "$WORKSPACE/src/main.py"

# ---------- 2. Force theme to something else ----------
USER_SETTINGS_DIR="$HOME/.config/Code/User"
mkdir -p "$USER_SETTINGS_DIR"

SETTINGS_FILE="$USER_SETTINGS_DIR/settings.json"
# Create default settings if file is missing
if [[ ! -f "$SETTINGS_FILE" ]]; then
    echo "{}" > "$SETTINGS_FILE"
fi

# Switch theme to VS Code “Default Dark+”
if command -v jq >/dev/null 2>&1; then
    # Use jq to modify (safe for existing content)
    tmp="$(mktemp)"
    jq '.["workbench.colorTheme"]="Default Dark+"' "$SETTINGS_FILE" > "$tmp"
    mv "$tmp" "$SETTINGS_FILE"
else
    # Fallback: rewrite minimal settings
    cat > "$SETTINGS_FILE" <<'EOF'
{
  "workbench.colorTheme": "Default Dark+"
}
EOF
fi
echo "User settings forced to workbench.colorTheme = \"Default Dark+\""

# ---------- 3. Uninstall Atom One Dark extension if present ----------
THEME_EXTENSION="akamud.vscode-theme-onedark"
if code --list-extensions | grep -q "$THEME_EXTENSION"; then
    echo "Removing existing Atom One Dark extension ..."
    code --uninstall-extension "$THEME_EXTENSION" || true
fi

# ---------- 4. Drop a learner hint ----------
echo "Change VS Code theme to: Atom One Dark" > "$WORKSPACE/.task_instructions.txt"

# ---------- 5. Verification ----------
echo "Verifying initial state ..."
CURRENT_THEME=$(jq -r '."workbench.colorTheme"' "$SETTINGS_FILE")
if [[ "$CURRENT_THEME" == "Default Dark+" ]]; then
    echo "✓ Theme is correctly set to Default Dark+"
else
    echo "✗ Theme is NOT set to Default Dark+ (found '$CURRENT_THEME')" >&2
    exit 1
fi

if code --list-extensions | grep -q "$THEME_EXTENSION"; then
    echo "✗ Atom One Dark extension is still installed" >&2
    exit 1
else
    echo "✓ Atom One Dark extension is NOT installed"
fi

# ---------- 6. Open VS Code ----------
echo "Opening VS Code.  Perform the theme switch inside the UI ..."
code "$WORKSPACE" & disown
#!/usr/bin/env bash
# Purpose : Prepare a Python-editing workspace *before* the user adds the
#           Ctrl+D duplication keybinding and the 80-column ruler.
# Author  : VS-Code-Automation Bot
# Usage   : bash initial_setup.sh
# ----------------------------------------------
set -euo pipefail

echo "-------------------------------------------------"
echo " VS Code Duplication/Ruler Task – Initial State "
echo "-------------------------------------------------"

# 1. Create a realistic workspace with a long Python file
WORKSPACE="$HOME/vscode_dup_line_task"
echo "Creating workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"
cat > "$WORKSPACE/src/long_script.py" <<'PY'
#!/usr/bin/env python3
"""
This module intentionally contains long lines that exceed
the recommended PEP-8 line length so the user can see the
benefit of an 80 column ruler.
"""
def very_long_function_name(parameter_one, parameter_two, parameter_three, parameter_four):
    print("This is a very long line that should probably be wrapped, "
          "but for demonstration purposes we will keep it unwrapped.")
PY

# 2. Ensure user keybindings & settings exist but WITHOUT the required changes
VSC_USER_DIR="$HOME/.config/Code/User"
mkdir -p "$VSC_USER_DIR"

# keybindings.json  (leave default behaviour in place)
if [ ! -f "$VSC_USER_DIR/keybindings.json" ]; then
  echo "[]" > "$VSC_USER_DIR/keybindings.json"
fi

# settings.json  (remove any rulers if they exist)
if [ ! -f "$VSC_USER_DIR/settings.json" ]; then
  echo "{}" > "$VSC_USER_DIR/settings.json"
fi
# Strip editor.rulers from settings (if any)
if command -v jq >/dev/null 2>&1; then
  jq 'del(.["editor.rulers"])' "$VSC_USER_DIR/settings.json" > "$VSC_USER_DIR/settings.tmp" || true
  mv "$VSC_USER_DIR/settings.tmp" "$VSC_USER_DIR/settings.json"
fi

# 3. Add task instructions for the learner
echo "Add keybinding: Ctrl+D → duplicate current line"  > "$WORKSPACE/.task_info.txt"
echo "Add editor ruler at column 80 (PEP-8 compliance)" >> "$WORKSPACE/.task_info.txt"

# 4. Verification – show that the requested configuration does NOT exist yet
echo "Verifying initial absence of keybinding & ruler..."
grep -q '"ctrl+d"' "$VSC_USER_DIR/keybindings.json" && \
  echo "Unexpected Ctrl+D keybinding present! (Should be absent)" && exit 1 || \
  echo "✓ Ctrl+D keybinding NOT present (as expected)"

grep -q '"editor.rulers"' "$VSC_USER_DIR/settings.json" && \
  echo "Unexpected editor.rulers present! (Should be absent)" && exit 1 || \
  echo "✓ No editor.rulers found (as expected)"

# 5. Open VS Code
echo "Opening VS Code..."
code "$WORKSPACE" &

echo "Initial setup complete – VS Code should open momentarily."
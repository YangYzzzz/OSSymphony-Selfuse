#!/usr/bin/env bash
###############################################################################
# VS Code – Overtype / Overwrite Mode Task (INITIAL STATE)
# Creates a small workspace with docs/OVRsample.txt so the learner
# can practise switching VS Code into OVERWRITE mode and typing “HELLO”.
###############################################################################
set -euo pipefail

echo "==========  VS CODE OVERTYPE TASK – INITIAL SETUP  =========="

# ----------------------------------------------------------------------
# 1. Define useful paths
# ----------------------------------------------------------------------
WORKSPACE="$HOME/projects"                 # -> ~/projects
FILE_RELATIVE="docs/OVRsample.txt"         # relative path inside workspace
FILE_PATH="$WORKSPACE/$FILE_RELATIVE"      # full path to the file we’ll edit
VSCODE_DIR="$WORKSPACE/.vscode"

# ----------------------------------------------------------------------
# 2. Re-create workspace from scratch for idempotency
# ----------------------------------------------------------------------
echo "[+] Preparing workspace directory:  $WORKSPACE"
rm -rf  "$WORKSPACE"
mkdir -p "$WORKSPACE/docs"
mkdir -p "$VSCODE_DIR"

# ----------------------------------------------------------------------
# 3. Seed the text file with initial content
# ----------------------------------------------------------------------
cat > "$FILE_PATH" <<'EOF'
The quick brown fox jumps over the lazy dog.
EOF
echo "[✓] File created: $FILE_PATH"

# ----------------------------------------------------------------------
# 4. (Optional) seed a README so the Explorer is not empty
# ----------------------------------------------------------------------
echo "# VS Code Overtype Task" > "$WORKSPACE/README.md"

# ----------------------------------------------------------------------
# 5. Leave a task hint for the learner
# ----------------------------------------------------------------------
cat > "$WORKSPACE/.task_info.txt" <<EOF
=========================================
TASK
=========================================
1. Open $FILE_RELATIVE.
2. Switch the editor from INSERT to OVERWRITE mode
   - Press the Insert key, or
   - Click "INS" in the Status Bar (bottom-right).
3. With the caret at the very start (line 1, column 1)
   type: HELLO
4. Save the file.  Result should be:
   HELLO quick brown fox jumps over the lazy dog.
=========================================
EOF

# ----------------------------------------------------------------------
# 6. Minimal workspace settings (nothing special here)
# ----------------------------------------------------------------------
cat > "$VSCODE_DIR/settings.json" <<'EOF'
{
  // You may optionally pre-toggle overwrite mode here:
  // "editor.accessibilitySupport": "off"
}
EOF

echo "[✓] Workspace settings written."

# ----------------------------------------------------------------------
# 7. Verification – ensure the first 5 chars are NOT “HELLO”
# ----------------------------------------------------------------------
FIRST_FIVE="$(head -c 5 "$FILE_PATH")"
if [[ "$FIRST_FIVE" == "HELLO" ]]; then
    echo "[✗] Verification failed – file already in final state!"
    exit 1
fi
echo "[✓] Verification passed – file still needs editing."

# ----------------------------------------------------------------------
# 8. Launch VS Code, opening the target file directly
# ----------------------------------------------------------------------
echo "[→] Launching VS Code…"
code --goto "$FILE_PATH":1:1  &

echo "==========  SETUP COMPLETE – Ready for learner action  =========="
#!/usr/bin/env bash
###############################################################################
# vendor-prefix_task_init.sh
#
# Purpose  : Prepare a VS Code workspace that displays CSS vendor-prefix
#            warnings so the user can practise turning them off.
# Creates  :  $HOME/vscode_css_vendor_prefix_task/  (workspace)
# Opens    :  VS Code on that workspace
###############################################################################
set -euo pipefail

echo "─────────────────────────────────────────────────────────────"
echo "Setting up initial state for CSS vendor-prefix warning task…"
echo "─────────────────────────────────────────────────────────────"

# ------------------------------------------------------------------
# 1. Workspace layout
# ------------------------------------------------------------------
WORKSPACE="$HOME/vscode_css_vendor_prefix_task"
if [ -d "$WORKSPACE" ]; then
  echo "Removing any existing workspace at $WORKSPACE"
  rm -rf "$WORKSPACE"
fi

echo "Creating workspace: $WORKSPACE"
mkdir -p "$WORKSPACE/.vscode"

# ------------------------------------------------------------------
# 2. Sample legacy stylesheet that triggers vendor-prefix warnings
# ------------------------------------------------------------------
cat > "$WORKSPACE/style.css" <<'EOF'
/* Legacy flexbox example – VS Code will warn on the prefixed rules */
.container {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}
EOF
echo "Created sample stylesheet with vendor-prefixed properties."

# ------------------------------------------------------------------
# 3. Workspace settings (INTENTIONALLY keep default vendor-prefix lint) 
# ------------------------------------------------------------------
cat > "$WORKSPACE/.vscode/settings.json" <<'EOF'
{
  // CSS lint settings left to default so that warnings appear
  "editor.tabSize": 2
}
EOF
echo "Workspace settings.json generated (vendorPrefix lint not disabled)."

# ------------------------------------------------------------------
# 4. Verification – ensure vendorPrefix NOT set to \"ignore\"
# ------------------------------------------------------------------
if grep -q '"css.lint.vendorPrefix"' "$WORKSPACE/.vscode/settings.json"; then
  VALUE=$(jq -r '.["css.lint.vendorPrefix"]' "$WORKSPACE/.vscode/settings.json")
  if [ "$VALUE" == "ignore" ]; then
    echo "ERROR: vendorPrefix lint is already disabled – aborting setup."
    exit 1
  fi
fi
echo "Verified: vendorPrefix lint is NOT disabled yet."

# ------------------------------------------------------------------
# 5. Task instructions marker
# ------------------------------------------------------------------
cat > "$WORKSPACE/TASK_INSTRUCTIONS.txt" <<'EOF'
VS Code currently warns about vendor-prefixed CSS properties (e.g. -webkit-box).
Task: Turn OFF these warnings by setting
      "css.lint.vendorPrefix": "ignore"
You may do this via:
  • File → Preferences → Settings  (search "vendor prefix")
  • Or by editing .vscode/settings.json directly
EOF
echo "Task instructions written to TASK_INSTRUCTIONS.txt."

# ------------------------------------------------------------------
# 6. Launch VS Code
# ------------------------------------------------------------------
echo "Opening VS Code…"
code "$WORKSPACE" &

echo "Initial workspace ready.  Look for squiggly warnings under -webkit-*."
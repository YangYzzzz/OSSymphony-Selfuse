#!/usr/bin/env bash
set -euo pipefail
#
# initial_activity_bar_setup.sh
# -----------------------------
# Creates a workspace whose Activity Bar background is *not* red so the
# learner has to change it to pure red (#ff0000) via
# workbench.colorCustomizations in .vscode/settings.json.
#

echo "==> Preparing initial Activity Bar color task …"

# --------------------------------------------------------------------
# 1. Create a clean workspace skeleton
# --------------------------------------------------------------------
WORKSPACE="$HOME/activity_bar_red_task"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/.vscode"

# A tiny README just to make the folder look real
cat > "$WORKSPACE/README.md" <<'EOF'
# VS Code Color Customization Task
Change the Activity Bar background to pure red using workspace settings!
EOF

# --------------------------------------------------------------------
# 2. Seed workspace settings with a *non-red* Activity Bar background
# --------------------------------------------------------------------
cat > "$WORKSPACE/.vscode/settings.json" <<'EOF'
{
  // Current theme & colours (needs fixing!)
  "workbench.colorTheme": "Default Dark+",
  "workbench.colorCustomizations": {
    "activityBar.background": "#333333",
    "activityBar.foreground": "#ffffff"
  }
}
EOF
echo "   • settings.json written with activityBar.background = #333333"

# --------------------------------------------------------------------
# 3. Verification – make sure we really DIDN'T start with red
# --------------------------------------------------------------------
if jq -e '.["workbench.colorCustomizations"]["activityBar.background"] == "#ff0000"' \
      "$WORKSPACE/.vscode/settings.json" >/dev/null; then
  echo "ERROR: The workspace was accidentally initialised with a red Activity Bar!"
  exit 1
fi
echo "   • Verification passed – background is NOT red (good)."

# --------------------------------------------------------------------
# 4. Launch VS Code so the learner can perform the task
# --------------------------------------------------------------------
echo "==> Opening VS Code.  Task: edit .vscode/settings.json so that"
echo "    \"activityBar.background\" becomes \"#ff0000\"."
code "$WORKSPACE" & disown
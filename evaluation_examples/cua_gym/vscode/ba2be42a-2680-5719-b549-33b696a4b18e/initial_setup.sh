#!/usr/bin/env bash
###############################################################################
# VS Code Task – Initial Setup
# Creates a workspace that does NOT yet override the color theme.
# The user’s personal theme will still be active in this repo.
###############################################################################
set -euo pipefail

echo "[Init] Preparing workspace that needs a repo-specific theme override …"

# ---------------------------------------------------------------------------
# 1. Define workspace location
# ---------------------------------------------------------------------------
WORKSPACE="$HOME/github_theme_task"
echo "[Init] Workspace will be at: $WORKSPACE"
rm -rf "$WORKSPACE"         # start fresh every time the script is run
mkdir -p "$WORKSPACE/.vscode"

# ---------------------------------------------------------------------------
# 2. Populate a realistic repo
# ---------------------------------------------------------------------------
cat > "$WORKSPACE/README.md" <<'EOF'
# GitHub Theme Demo Repo

This repository is used for a VS Code task showing how to set a workspace-
specific color theme (GitHub Light Modern).
EOF

cat > "$WORKSPACE/app.js" <<'EOF'
console.log('Hello from the GitHub Theme demo repo');
EOF

# ---------------------------------------------------------------------------
# 3. Provide an *incomplete* .vscode/settings.json
#    (does not yet contain workbench.colorTheme)
# ---------------------------------------------------------------------------
cat > "$WORKSPACE/.vscode/settings.json" <<'EOF'
{
  // Workspace settings go here.
  // The color theme override is intentionally MISSING.
  "editor.tabSize": 2
}
EOF
echo "[Init] Created .vscode/settings.json WITHOUT a colorTheme override."

# ---------------------------------------------------------------------------
# 4. Verification – prove that the colorTheme key is missing
# ---------------------------------------------------------------------------
if command -v jq >/dev/null 2>&1; then
  THEME_VALUE=$(jq -r '.["workbench.colorTheme"] // empty' \
                "$WORKSPACE/.vscode/settings.json")
  if [[ -z "$THEME_VALUE" ]]; then
    echo "[Init] Verification OK: workbench.colorTheme is NOT set in workspace."
  else
    echo "[Init] Unexpected: theme was already set to $THEME_VALUE"
  fi
else
  echo "[Init] jq not found – skipping JSON verification."
fi

# ---------------------------------------------------------------------------
# 5. Open the workspace in VS Code
# ---------------------------------------------------------------------------
echo "[Init] Opening VS Code …"
code "$WORKSPACE" &

echo "[Init] Setup complete.  In VS Code, note that your *global* theme is still active."
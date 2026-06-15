#!/usr/bin/env bash
# ------------------------------------------------------------------
# setup_initial.sh
# ------------------------------------------------------------------
# Creates a workspace where IntelliSense is ON inside Python strings.
# The learner's job: change settings so that ONLY Python strings lose
# quick suggestions while other languages/contexts are unaffected.
# ------------------------------------------------------------------
set -euo pipefail

echo "⬛  VS Code Quick-Suggestions Task – Initial State"

# ------------------------------------------------------------------
# 1) Workspace skeleton
# ------------------------------------------------------------------
WORKSPACE="$HOME/python_intellisense_task"
VSCODE_DIR="$WORKSPACE/.vscode"

rm -rf  "$WORKSPACE"
mkdir -p "$VSCODE_DIR"

# ------------------------------------------------------------------
# 2) Sample Python code that triggers IntelliSense in an f-string
# ------------------------------------------------------------------
cat > "$WORKSPACE/main.py" <<'EOF'
name = "Ada"
project = "Babbage Engine"
# Type after the dot in the f-string below; suggestions will pop up.
print(f"{project.upper(). }")
EOF

# ------------------------------------------------------------------
# 3) Workspace settings – quickSuggestions ENABLED everywhere
# ------------------------------------------------------------------
cat > "$VSCODE_DIR/settings.json" <<'EOF'
{
  // Global default – everything ON (the nuisance state)
  "editor.quickSuggestions": {
    "other": true,
    "comments": true,
    "strings": true
  },

  // Explicitly demonstrate that we haven't overridden Python yet
  "[python]": {}
}
EOF

# ------------------------------------------------------------------
# 4) Extension recommendations (optional but realistic)
# ------------------------------------------------------------------
cat > "$VSCODE_DIR/extensions.json" <<'EOF'
{
  "recommendations": [
    "ms-python.python"
  ]
}
EOF

# ------------------------------------------------------------------
# 5) Provide user instructions / task marker
# ------------------------------------------------------------------
cat > "$WORKSPACE/TASK.md" <<'EOF'
# VS Code Task – Disable Suggestions Inside Python Strings

Problem: While typing inside Python string literals (for example,
inside an f-string), IntelliSense pops up and is distracting.

Goal:
1. Keep quick suggestions ON globally (other, comments, etc.).
2. Turn quick suggestions OFF **only for strings in Python**.

Hint: Use a language-specific override in `.vscode/settings.json`
similar to:
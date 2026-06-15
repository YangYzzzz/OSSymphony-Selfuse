#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# VS Code Task: Install “Markdown All in One” Extension
# This script prepares the workspace in a state where the extension is *not*
# installed and a Markdown–heavy project makes the need obvious.
###############################################################################

echo "=== Preparing initial workspace ==="

# 1. Create a realistic workspace ------------------------------------------------
WORKSPACE="$HOME/markdown_docs_project"
rm -rf  "$WORKSPACE"
mkdir -p "$WORKSPACE/docs"
mkdir -p "$WORKSPACE/.vscode"

#   Sample Markdown files
cat > "$WORKSPACE/README.md" <<'EOF'
# Project Documentation

We maintain all docs in Markdown.
To improve productivity, consider installing helpful extensions!
EOF

cat > "$WORKSPACE/docs/usage.md" <<'EOF'
## Usage Guide

| Command | Description |
| ------- | ----------- |
| build   | Builds the project |
| test    | Runs all tests |

<!-- Typing tables & headings is cumbersome without shortcuts :( -->
EOF

#   Extension recommendations file (suggest but NOT installed)
cat > "$WORKSPACE/.vscode/extensions.json" <<'EOF'
{
  "recommendations": [
    "yzhang.markdown-all-in-one"
  ]
}
EOF
echo "Workspace created at $WORKSPACE"

# 2. Ensure the target extension is NOT installed --------------------------------
echo "=== Verifying extension is NOT installed ==="
if code --list-extensions | grep -q '^yzhang.markdown-all-in-one$'; then
  echo "Extension already present – removing to create initial state..."
  code --uninstall-extension yzhang.markdown-all-in-one --force
fi
if code --list-extensions | grep -q '^yzhang.markdown-all-in-one$'; then
  echo "ERROR: Failed to uninstall Markdown All in One" >&2
  exit 1
fi
echo "Verified: Markdown All in One is not installed."

# 3. Add a task-info hint file ---------------------------------------------------
cat > "$WORKSPACE/.task_info.txt" <<'EOF'
TASK: Install the “Markdown All in One” extension to speed-up editing headings,
tables, and more.  (Publisher: yzhang.markdown-all-in-one)
EOF

# 4. Open VS Code on the workspace ----------------------------------------------
echo "Opening VS Code... (The user should now install the extension)"
code "$WORKSPACE" &

echo "=== Initial setup completed ==="
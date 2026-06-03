#!/usr/bin/env bash
###############################################################################
# node_readme_task_init.sh
# -------------------------------------------------
# 1. Creates a Node.js workspace that lacks docs/README.md
# 2. Installs “Markdown All in One” v3.5.1
# 3. Opens VS Code so the learner can add the README from the Command Palette
###############################################################################
set -euo pipefail

echo "🔧  Preparing initial VS Code Markdown task environment …"

# ------------------------------------------------------------------ #
# Configuration
# ------------------------------------------------------------------ #
WORKSPACE="$HOME/vscode_node_md_task"      # Feel free to change location
EXTENSION_ID="yzhang.markdown-all-in-one"
EXT_VERSION="3.5.1"

# ------------------------------------------------------------------ #
# Clean slate & project skeleton
# ------------------------------------------------------------------ #
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"

echo "📁  Creating minimal Node.js project …"
npm init -y >/dev/null 2>&1

echo "📁  Creating placeholder docs directory (README will be added later) …"
mkdir -p docs

echo "🛠  Making VS Code workspace configuration …"
mkdir -p .vscode
cat > .vscode/extensions.json <<'EOF'
{
  "recommendations": [
    "yzhang.markdown-all-in-one"
  ]
}
EOF

# ------------------------------------------------------------------ #
# Install required extension (specific version)
# ------------------------------------------------------------------ #
echo "🔌  Installing Markdown All in One @${EXT_VERSION} …"
code --install-extension "${EXTENSION_ID}@${EXT_VERSION}" --force >/dev/null 2>&1

# ------------------------------------------------------------------ #
# Task instructions for the learner
# ------------------------------------------------------------------ #
cat > .task_info.txt <<'EOF'
================ VS Code Task Instructions ================
Goal: Create docs/README.md with three level-1 headers:
  # Description
  # Installation
  # Usage

Steps (GUI):
1. Press Ctrl+Shift+P (⇧⌘P on macOS) to open the Command Palette.
2. Type “Markdown All in One: New Document” and hit Enter.
3. Save the untitled file as docs/README.md.
4. Replace the template text so the file looks like:

# Description

# Installation

# Usage

5. Save the file (Ctrl+S). Done!
============================================================
EOF

# Make sure README is NOT present yet
if [ -f docs/README.md ]; then
  echo "⚠️  docs/README.md already exists unexpectedly – removing it."
  rm docs/README.md
fi

# ------------------------------------------------------------------ #
# Fire up VS Code
# ------------------------------------------------------------------ #
echo "🚀  Opening workspace in VS Code – perform the task now!"
code "$WORKSPACE" &

echo "✅  Initial setup complete: $WORKSPACE"
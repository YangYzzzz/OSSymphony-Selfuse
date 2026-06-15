#!/usr/bin/env bash
# ------------------------------------------------------------------
# Initial Setup for “Add a 60-Character Ruler” VS Code Task
# ------------------------------------------------------------------
set -euo pipefail

echo "🔧  Preparing initial workspace for Markdown ruler task..."

# 1. Workspace location
WORKSPACE="$HOME/vscode_markdown_ruler_task"
echo "📁  Workspace path: $WORKSPACE"

# 2. Start fresh every run
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/docs" "$WORKSPACE/.vscode"

# 3. Create a sample Markdown file with long lines (> 60 chars)
cat > "$WORKSPACE/docs/guide.md" << 'EOF'
# Project Documentation Guide

This sentence intentionally exceeds sixty characters so that the lack of a ruler becomes visually obvious while editing.

## Contributing

When you add new content, please keep each line under sixty characters for improved readability and cleaner diffs.
EOF
echo "📝  Created sample Markdown file: docs/guide.md"

# 4. Create initial workspace settings WITHOUT a ruler
cat > "$WORKSPACE/.vscode/settings.json" << 'EOF'
{
  // Markdown editing settings (no ruler yet)
  "[markdown]": {
    "editor.wordWrap": "off",
    "editor.renderWhitespace": "boundary"
  }
}
EOF
echo "⚙️  Initial .vscode/settings.json created (no ruler defined)."

# 5. Task instructions for the human user
cat > "$WORKSPACE/TASK_INSTRUCTIONS.txt" << 'EOF'
VS Code Task: Add a 60-character ruler for Markdown files.

Goal:
  Update .vscode/settings.json so that Markdown editors show a vertical ruler at 60 characters.

Hint:
  Settings UI ➜ Search “rulers” ➜ Add 60 under “[markdown]” scope
  OR edit JSON:
  "[markdown]": {
      "editor.rulers": [60]
  }
EOF
echo "🗒️  Task instructions added."

# 6. Verification (should NOT find 60 in settings)
if grep -q '"editor.rulers"' "$WORKSPACE/.vscode/settings.json"; then
    echo "❌  Ruler already present! Cleaning up and exiting."
    exit 1
else
    echo "✅  Verified: No ruler exists yet (expected)."
fi

# 7. Open the workspace in VS Code
echo "🚀  Launching VS Code..."
code "$WORKSPACE" &
sleep 2

echo "✅  Initial setup complete. Ready for the user to add a 60-character ruler."
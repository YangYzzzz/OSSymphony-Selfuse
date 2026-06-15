#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
# VS Code Task – Initial State
# Goal: Prepare /home/user/docs WITHOUT a README.md so the user’s job is to add it
# -----------------------------------------------------------------------------

echo "🔧  Preparing initial VS Code task environment..."

DOCS_DIR="/home/user/docs"

# 1. Create the docs directory and some sample files
echo "• Creating directory: $DOCS_DIR"
mkdir -p "$DOCS_DIR"

echo "• Populating sample documentation files"
echo "# Project Documentation Overview"   > "$DOCS_DIR/overview.md"
echo "## Outstanding Tasks"              > "$DOCS_DIR/todo.md"

# 2. Ensure README.md does NOT exist
if [ -f "$DOCS_DIR/README.md" ]; then
    echo "• Removing pre-existing README.md to enforce task scenario"
    rm -f "$DOCS_DIR/README.md"
fi

# 3. Verification – README.md should be missing
if [ -f "$DOCS_DIR/README.md" ]; then
    echo "❌  Verification failed: README.md still present!"
    exit 1
else
    echo "✅  Verification passed: README.md is absent (expected)."
fi

# 4. Provide a small task hint file (optional for graders)
echo "Create a new README.md with basic project info." > "$DOCS_DIR/.task_info.txt"

# 5. Open VS Code pointed at the docs folder
echo "🚀  Launching VS Code…"
code "$DOCS_DIR" &

echo "🎉  Initial environment ready. The user must add README.md."
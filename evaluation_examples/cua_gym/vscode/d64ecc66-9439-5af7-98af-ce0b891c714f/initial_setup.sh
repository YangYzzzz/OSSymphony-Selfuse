#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial Setup Script
# Purpose : Create a realistic workspace that still contains the word
#           “button” so the user can replace it with “btn”.
###############################################################################

echo "🔧  Setting up initial VS Code task environment..."

# ---------------------------------------------------------------------------
# 1. Create the required workspace and file
# ---------------------------------------------------------------------------
WORKSPACE="/home/user/docs"
FILE="$WORKSPACE/components.md"

mkdir -p "$WORKSPACE"

cat > "$FILE" << 'EOF'
# UI Components Guide

Our primary interactive element is the button. Every button should be clearly labeled.
When designing a primary call-to-action, consider using a large, prominent button.

## Accessibility

Make sure each button has an aria-label attribute.
Avoid disabling a button purely for visual reasons.

## States

A button can be in one of the following states:
1. Default button
2. Hovered button
3. Focused button
4. Disabled button
5. Loading button
EOF

echo "📄  Created file: $FILE"

# ---------------------------------------------------------------------------
# 2. Add a task hint for the user
# ---------------------------------------------------------------------------
echo "Replace every instance of the word 'button' with 'btn' in components.md" \
  > "$WORKSPACE/.task_info.txt"
echo "📝  Task instruction file written to $WORKSPACE/.task_info.txt"

# ---------------------------------------------------------------------------
# 3. Verification – ensure the word 'button' exists before task starts
# ---------------------------------------------------------------------------
if grep -q "button" "$FILE"; then
  echo "✅  Verification passed: 'button' occurrences found in $FILE"
else
  echo "❌  Verification failed: No 'button' found in $FILE" >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# 4. Launch VS Code so the user can perform the task
# ---------------------------------------------------------------------------
echo "🚀  Launching VS Code..."
code "$WORKSPACE" & disown
echo "🟢  VS Code launched with workspace: $WORKSPACE"
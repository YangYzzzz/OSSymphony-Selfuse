#!/usr/bin/env bash
# Purpose : Prepare a legacy PHP project that shows validation errors.
# Action   : Creates workspace, adds PHP file with an obvious syntax error,
#            enables PHP validation (default) so red-squiggles appear.

set -euo pipefail

echo "================  Initial VS Code PHP validation task setup ================"

# 1. Workspace path ----------------------------------------------------------------
WORKSPACE="$HOME/php_legacy_project"
echo "Workspace will be: $WORKSPACE"

# 2. Fresh workspace ----------------------------------------------------------------
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/.vscode"

# 3. Create a PHP file with a deliberate syntax error ------------------------------
cat > "$WORKSPACE/index.php" << 'EOF'
<?php
// Legacy code with an obvious syntax issue (missing semicolon):
echo "Hello legacy world!"
EOF
echo "Created PHP file with a syntax error: $WORKSPACE/index.php"

# 4. Enable (or leave default) PHP validation --------------------------------------
#    Explicitly set php.validate.enable = true so the squiggles certainly appear.
cat > "$WORKSPACE/.vscode/settings.json" << 'EOF'
{
  "php.validate.enable": true
}
EOF
echo "Created workspace settings that keep validation ON (red squiggles expected)."

# 5. Task marker for the learner ----------------------------------------------------
echo "Turn OFF PHP syntax validation (set \"php.validate.enable\": false)" \
  > "$WORKSPACE/.task_info.txt"

# 6. Open the workspace in VS Code --------------------------------------------------
code "$WORKSPACE" &

# 7. Verification -------------------------------------------------------------------
#    We just show the current setting value to prove it is TRUE.
sleep 2
echo "Current php.validate.enable setting:"
if command -v jq >/dev/null 2>&1; then
  jq '.["php.validate.enable"]' "$WORKSPACE/.vscode/settings.json"
else
  grep -Po '"php.validate.enable"\s*:\s*\K(true|false)' \
        "$WORKSPACE/.vscode/settings.json" || true
fi

echo "================  Initial setup complete – red squiggles should be visible."
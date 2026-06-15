#!/usr/bin/env bash
# ============================================================
#  VS Code SQL schema scaffolding – INITIAL STATE
#  ------------------------------------------------------------
#  This script prepares a workspace that is missing the
#  /database/schema.sql file.  The learner will be expected
#  to add it using SQLTools v0.27.2 + IntelliSense.
# ============================================================
set -euo pipefail

echo "🛠  Preparing initial SQL tooling task ..."

# ------------------------------------------------------------
# 1. Workspace skeleton
# ------------------------------------------------------------
WORKSPACE="$HOME/vscode_sql_task"
DB_DIR="$WORKSPACE/database"
VSCODE_DIR="$WORKSPACE/.vscode"

echo "📂 Creating workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$DB_DIR" "$VSCODE_DIR"

# dummy application file so the workspace isn’t empty
cat > "$WORKSPACE/README.md" <<'EOF'
# VS Code SQL Tools Task

Your goal:  
Create `database/schema.sql` containing CREATE TABLE
statements for `users` and `posts` exactly as described
in the task instructions.  
Use the SQLTools extension (v0.27.2) for IntelliSense.
EOF

# ------------------------------------------------------------
# 2. VS Code configuration
# ------------------------------------------------------------
# Extension recommendations
cat > "$VSCODE_DIR/extensions.json" <<'EOF'
{
  "recommendations": [
    "mtxr.sqltools"
  ]
}
EOF

# Settings – turn on SQLTools suggestions even without a live DB
cat > "$VSCODE_DIR/settings.json" <<'EOF'
{
  "sqltools.useNodeRuntime": "bundled",
  "sqltools.format.aligned": true,
  "sqltools.experimental.serverMode": "OFF"
}
EOF

# ------------------------------------------------------------
# 3. Install required extension (specific version if available)
# ------------------------------------------------------------
echo "🔌 Ensuring SQLTools v0.27.2 is installed ..."
if code --list-extensions | grep -q "mtxr.sqltools@0.27.2"; then
  echo "   • Correct version already installed."
else
  if code --install-extension "mtxr.sqltools@0.27.2" --force; then
    echo "   • SQLTools v0.27.2 installed."
  else
    echo "   ⚠️  Could not pin exact version, installed latest instead."
    code --install-extension "mtxr.sqltools" --force
  fi
fi

# ------------------------------------------------------------
# 4. Verification of initial state
# ------------------------------------------------------------
echo "🔎 Verifying that schema.sql does NOT yet exist ..."
if [ -f "$DB_DIR/schema.sql" ]; then
  echo "❌  schema.sql already present – aborting to keep task valid."
  exit 1
fi
echo "✅  Validation OK – learner still needs to create schema.sql."

# ------------------------------------------------------------
# 5. Open VS Code
# ------------------------------------------------------------
echo "🚀 Opening VS Code ..."
code "$WORKSPACE" &>/dev/null &

echo "✅  Initial setup complete.  VS Code launched."
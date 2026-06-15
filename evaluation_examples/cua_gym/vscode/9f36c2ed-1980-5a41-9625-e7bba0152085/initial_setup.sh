#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# 01_init_autosave_task.sh
# -----------------------------------------------------------------------------
# Prepares a TypeScript workspace where autosave is OFF.
# Your job (in VS Code) will be to turn it ON with a 3-second delay.
# -----------------------------------------------------------------------------
set -euo pipefail

echo "🔧  Preparing TypeScript autosave task ..."

# --------------------------------------------------------------------------- #
# Workspace & file skeleton
# --------------------------------------------------------------------------- #
WORKSPACE="$HOME/vscode_ts_autosave_task"
echo "📁  Creating workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src" "$WORKSPACE/.vscode"

# tsconfig.json -------------------------------------------------------------- #
cat > "$WORKSPACE/tsconfig.json" <<'EOF'
{
  "compilerOptions": {
    "target": "ES2019",
    "module": "commonjs",
    "outDir": "dist",
    "strict": true
  },
  "include": ["src"]
}
EOF

# Sample TypeScript file ----------------------------------------------------- #
cat > "$WORKSPACE/src/index.ts" <<'EOF'
function greet(name: string) {
  return `Hello, ${name}!`;
}

console.log(greet("World"));
EOF

# VS Code settings (autosave disabled) -------------------------------------- #
cat > "$WORKSPACE/.vscode/settings.json" <<'EOF'
{
  // Autosave is currently disabled. Your task: enable it
  // so VS Code automatically saves after 3 seconds of inactivity.
  "files.autoSave": "off"
}
EOF

# --------------------------------------------------------------------------- #
# Verification of initial state
# --------------------------------------------------------------------------- #
echo "🔍  Verifying initial autosave setting ..."
INIT_OK=false
if command -v jq >/dev/null 2>&1; then
  jq -e '.["files.autoSave"]=="off"' "$WORKSPACE/.vscode/settings.json" >/dev/null && INIT_OK=true
else
  grep -q '"files.autoSave": "off"' "$WORKSPACE/.vscode/settings.json" && INIT_OK=true
fi

if $INIT_OK; then
  echo "✅  Initial verification passed: autosave is OFF"
else
  echo "❌  Initial verification FAILED"
  exit 1
fi

# --------------------------------------------------------------------------- #
# Launch VS Code
# --------------------------------------------------------------------------- #
echo "🚀  Opening workspace in VS Code ..."
code "$WORKSPACE" &

cat <<'EONOTE'

===============================================================================
 TASK IN VS CODE
===============================================================================
1. Open Settings (Ctrl+,) or use the Command Palette.
2. Search for "Auto Save".
3. Change:
     files.autoSave       = afterDelay
     files.autoSaveDelay  = 3000   (milliseconds)
4. Save the settings.
===============================================================================
EONOTE
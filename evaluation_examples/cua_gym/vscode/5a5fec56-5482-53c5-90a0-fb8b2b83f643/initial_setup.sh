#!/usr/bin/env bash
# -----------------------------------------------------------------------------
#  VS Code Task – Initial Setup
#  Goal: Prepare a TypeScript workspace WITHOUT the “Error Lens” extension
#        so the user can install it manually from the VS Code GUI.
# -----------------------------------------------------------------------------
set -euo pipefail

echo "──────────────────────────────────────────────"
echo "📦  Setting up INITIAL state for Error Lens task"
echo "──────────────────────────────────────────────"

# ------------------------------------------------------------------
# 1. Workspace preparation
# ------------------------------------------------------------------
WORKSPACE="$HOME/error_lens_ts_project"
echo "👉 Creating fresh workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"

# ------------------------------------------------------------------
# 2. Create realistic TypeScript files with obvious errors
# ------------------------------------------------------------------
cat > "$WORKSPACE/tsconfig.json" << 'EOF'
{
  "compilerOptions": {
    "target": "es6",
    "module": "commonjs",
    "strict": true,
    "outDir": "dist"
  },
  "include": ["src/**/*"]
}
EOF

cat > "$WORKSPACE/src/main.ts" << 'EOF'
// Intentional type errors for demonstration
function add(a: number, b: number): number {
  return a + b;
}

const result: number = add(5, "10");   // ❌ Should be number, not string
console.log("Result is", result);

someUndefinedFunction();               // ❌ Call to unknown function
EOF

# ------------------------------------------------------------------
# 3. Make sure “Error Lens” is NOT installed
# ------------------------------------------------------------------
EXTENSION_ID="usernamehw.errorlens"
if code --list-extensions | grep -q "$EXTENSION_ID"; then
  echo "🔧 Removing existing Error Lens extension to reproduce starting state…"
  code --uninstall-extension "$EXTENSION_ID" || true
fi

# Double-check
if code --list-extensions | grep -q "$EXTENSION_ID"; then
  echo "⚠️  Failed to uninstall Error Lens – aborting."
  exit 1
else
  echo "✅ Verified Error Lens is NOT installed."
fi

# ------------------------------------------------------------------
# 4. Drop a task hint file (optional, visible in VS Code Explorer)
# ------------------------------------------------------------------
cat > "$WORKSPACE/README_TASK.md" << 'EOF'
# VS Code Task – Install “Error Lens”

Open the Extensions sidebar (Ctrl+Shift+X) and install:
   • Error Lens (usernamehw.errorlens)

You should then see TypeScript errors displayed inline.
EOF

# ------------------------------------------------------------------
# 5. Open VS Code with this workspace
# ------------------------------------------------------------------
echo "🚀 Launching VS Code…"
code "$WORKSPACE" &

echo "🎉 Initial setup complete. VS Code opened without Error Lens."
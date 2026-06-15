#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# VS Code “global search / Search Editor” task – INITIAL STATE
#
# Creates a miniature TypeScript monorepo that contains several occurrences
# of the word “refactor”.  The user’s job (to be done manually in VS Code) is:
#   1. Run a global search for “refactor”
#   2. Open the results in a Search Editor
#   3. Save that Search Editor to “.vscode/reports/refactor.code-search”
###############################################################################

echo "⏳  Creating initial workspace …"

WORKSPACE="$HOME/vscode_refactor_audit"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/packages"   # root dir

################################################################################
# 1) Minimal monorepo structure with a few refs to ‘refactor’
################################################################################
for PKG in core api web ; do
    mkdir -p "$WORKSPACE/packages/$PKG/src"
done

cat > "$WORKSPACE/packages/core/src/index.ts" <<'EOF'
export function coreFn() {
  // TODO: refactor this core logic next sprint
  return 'core';
}
EOF

cat > "$WORKSPACE/packages/api/src/router.ts" <<'EOF'
import { coreFn } from '../../core/src/index';
// FIXME: refactor router handling once auth layer lands
export const router = coreFn();
EOF

cat > "$WORKSPACE/packages/web/src/App.tsx" <<'EOF'
import React from 'react';
// NOTE: refactor UI component when new design system ships
export const App = () => <div>Hello</div>;
EOF

################################################################################
# 2) Root package.json so VS Code recognises a TypeScript workspace
################################################################################
cat > "$WORKSPACE/package.json" <<'EOF'
{
  "name": "ts-monorepo",
  "private": true,
  "workspaces": ["packages/*"]
}
EOF

################################################################################
# 3) VS Code config directory (no Search Editor yet!)
################################################################################
mkdir -p "$WORKSPACE/.vscode"
cat > "$WORKSPACE/.vscode/settings.json" <<'EOF'
{
  "typescript.tsdk": "node_modules/typescript/lib",
  "search.exclude": {
    "**/node_modules": true
  }
}
EOF

################################################################################
# 4) Task-instruction marker so reviewers know what to do
################################################################################
cat > "$WORKSPACE/.task_info.txt" <<'EOF'
VS Code Task:
  • Press   Ctrl+Shift+F   and type: refactor
  • Click the tiny »🔍» arrow (or open Command Palette ▶ “Search Editor: Open New Search Editor”
    to load the results into a Search Editor)
  • Save the Search Editor as ⇒ .vscode/reports/refactor.code-search
EOF

################################################################################
# 5) Verification – prove the Search Editor file does NOT exist yet
################################################################################
if [ -e "$WORKSPACE/.vscode/reports/refactor.code-search" ]; then
  echo "❌   Unexpected search-editor file already present"
  exit 1
fi
echo "✅  Initial verification complete – no .code-search file present"

################################################################################
# 6) Launch VS Code
################################################################################
echo "🚀  Opening VS Code …"
code "$WORKSPACE" &

echo "🟢  Initial setup finished – perform the task in VS Code now."
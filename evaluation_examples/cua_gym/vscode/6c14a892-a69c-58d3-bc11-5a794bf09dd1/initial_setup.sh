#!/usr/bin/env bash
###############################################################################
# VS Code React-lazy-load TASK – Initial learner state
###############################################################################
set -euo pipefail

echo "🛠  Preparing initial React-lazy-load task workspace …"

WORKSPACE="$HOME/react_lazyload_task"
VSCODE_DIR="$WORKSPACE/.vscode"

# (Re)create a clean workspace
rm -rf  "$WORKSPACE"
mkdir -p "$WORKSPACE/src/components" "$WORKSPACE/src/utils" "$VSCODE_DIR"

###############################################################################
# 1) Minimal React-18 project scaffold
###############################################################################
cat > "$WORKSPACE/package.json" <<'EOF'
{
  "name": "react-lazyload-demo",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "scripts": {
    "start": "echo \"Run a bundler of your choice here\""
  }
}
EOF

cat > "$WORKSPACE/src/components/App.jsx" <<'EOF'
import React from "react";

export default function App() {
  return (
    <main>
      <h1>Lazy-load demo</h1>

      {/* Images reference their real source in data-src.  */}
      <img data-src="https://picsum.photos/seed/1/600/400" alt="demo-1" width="600" height="400" />
      <img data-src="https://picsum.photos/seed/2/600/400" alt="demo-2" width="600" height="400" />
    </main>
  );
}
EOF

# Placeholder – utils folder exists but the required file does not.
echo "// TODO: create lazyLoad.js here" > "$WORKSPACE/src/utils/README.md"

###############################################################################
# 2) VS Code settings – NO Prettier or auto-format yet
###############################################################################
cat > "$VSCODE_DIR/settings.json" <<'EOF'
{
  "files.autoSave": "off",
  "editor.formatOnSave": false
}
EOF

cat > "$VSCODE_DIR/extensions.json" <<'EOF'
{
  "recommendations": []
}
EOF

###############################################################################
# 3) Task instructions for the learner
###############################################################################
cat > "$WORKSPACE/.task_info.txt" <<'EOF'
★ TASK STEPS ★
1. Create src/utils/lazyLoad.js exporting a `lazyLoad` function that uses IntersectionObserver
   to swap `data-src` → `src` when elements enter the viewport.
2. Install / enable Prettier extension (esbenp.prettier-vscode v9.16.0).
3. Update workspace settings so that:
     "files.autoSave": "onFocusChange",
     "editor.defaultFormatter": "esbenp.prettier-vscode",
     "editor.formatOnSave": true
4. Verify Ctrl+Shift+I formats lazyLoad.js.
EOF

###############################################################################
# 4) Open VS Code
###############################################################################
echo "🚀  Launching VS Code in initial state ..."
code "$WORKSPACE" &

###############################################################################
# 5) Quick sanity check
###############################################################################
if [[ -f "$VSCODE_DIR/settings.json" ]]; then
  echo "✅  Initial workspace ready: $WORKSPACE"
else
  echo "❌  settings.json not found — setup failed" >&2
  exit 1
fi
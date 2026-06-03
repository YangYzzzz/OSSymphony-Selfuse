#!/usr/bin/env bash
set -euo pipefail
#
# VS Code REACT STATE-MANAGER TASK  ─  INITIAL STATE
#

echo "► Creating initial workspace …"

WORKSPACE="$HOME/react_state_manager_task"
rm -rf  "$WORKSPACE"
mkdir -p "$WORKSPACE/src"
cd       "$WORKSPACE"

###############################################################################
# 1. Minimal React-style project skeleton
###############################################################################
cat > package.json <<'EOF'
{
  "name": "react-state-manager-task",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
EOF

cat > src/index.js <<'EOF'
import React       from 'react';
import {createRoot} from 'react-dom/client';
import App         from './App';

const root = createRoot(document.getElementById('root'));
root.render(<App />);
EOF

cat > src/App.js <<'EOF'
export default function App() {
  return <h1>Hello React</h1>;
}
EOF

# This file is what the user must finish.
cat > src/store.js <<'EOF'
// TODO ----------------------------------------------------------------------
// Implement a lightweight store exposing:
//   • subscribe
//   • unsubscribe
//   • dispatch
//   • getState
// ---------------------------------------------------------------------------
EOF

###############################################################################
# 2. VS Code configuration (needs fixing by user)
###############################################################################
mkdir -p .vscode
cat > .vscode/settings.json <<'EOF'
{
  // Enable after you finish store.js
  "editor.formatOnSave": false
}
EOF

cat > .vscode/extensions.json <<'EOF'
{
  "recommendations": ["esbenp.prettier-vscode"]
}
EOF

###############################################################################
# 3. Task instructions
###############################################################################
cat > .task_info.txt <<'EOF'
TASK STEPS
1. Open src/store.js and implement a lightweight state manager exposing:
      • subscribe
      • unsubscribe
      • dispatch
      • getState
2. Turn on automatic formatting on save by setting
      "editor.formatOnSave": true
   in .vscode/settings.json (workspace level).

Prettier (esbenp.prettier-vscode) is already in extension recommendations.
EOF

###############################################################################
# 4. Quick verification of initial state
###############################################################################
if grep -q '"editor.formatOnSave": false' .vscode/settings.json \
   && grep -q 'TODO' src/store.js ; then
   echo "✓ Initial state verified – workspace needs user action."
else
   echo "✗ Initial verification failed!" && exit 1
fi

###############################################################################
# 5. Open VS Code
###############################################################################
echo "► Launching VS Code …"
code "$WORKSPACE" &

echo "Initial environment ready: $WORKSPACE"
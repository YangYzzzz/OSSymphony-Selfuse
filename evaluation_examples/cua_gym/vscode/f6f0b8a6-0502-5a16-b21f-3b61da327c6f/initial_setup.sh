#!/usr/bin/env bash
# initial_setup.sh
# Purpose: Create a React-style workspace with Auto Save **disabled**
# so the user can enable "afterDelay" with a 5-second delay.

set -euo pipefail

echo "========== React Auto-Save Task: Initial Setup =========="

# 1. Create the workspace ----------------------------------------------------
WORKSPACE="$HOME/vscode_react_auto_save"
echo "Creating (or refreshing) workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src/components"
mkdir -p "$WORKSPACE/.vscode"

# 2. Populate the project with realistic files -------------------------------
cat > "$WORKSPACE/package.json" << 'EOF'
{
  "name": "react-auto-save-demo",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "scripts": {
    "start": "echo 'Pretend React dev server'"
  }
}
EOF

cat > "$WORKSPACE/src/index.js" << 'EOF'
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './components/App';

const root = createRoot(document.getElementById('root'));
root.render(<App />);
EOF

cat > "$WORKSPACE/src/components/App.jsx" << 'EOF'
import React from 'react';

export default function App() {
  return <h1>Hello, VS Code!</h1>;
}
EOF

# 3. VS Code settings – Auto Save OFF ----------------------------------------
cat > "$WORKSPACE/.vscode/settings.json" << 'EOF'
{
  // Auto Save currently disabled – user must enable
  "files.autoSave": "off"
}
EOF
echo "Initial VS Code settings written (Auto Save OFF)."

# 4. Task instructions for the learner ---------------------------------------
cat > "$WORKSPACE/.task_info.txt" << 'EOF'
VS Code Task:
Turn ON Auto Save "afterDelay" with a 5-second delay.

Required settings:
  "files.autoSave": "afterDelay"
  "files.autoSaveDelay": 5000
EOF

# 5. Verification of initial state -------------------------------------------
echo "- Verifying initial state ..."
if grep -q '"files.autoSave": "off"' "$WORKSPACE/.vscode/settings.json"; then
    echo "  ✔ Auto Save is OFF as expected."
else
    echo "  ✘ Auto Save not set to OFF!"; exit 1
fi

# 6. Open VS Code -------------------------------------------------------------
echo "Opening VS Code…"
code "$WORKSPACE" &

echo "========== Initial setup complete. =========="
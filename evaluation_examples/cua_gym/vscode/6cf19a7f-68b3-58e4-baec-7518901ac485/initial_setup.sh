#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# VS Code React-refactor TASK ‑ INITIAL STATE
# 1. Creates a React-like workspace missing src/utils/api.js
# 2. Supplies ESLint (v2.4.0) & Prettier (v10.0.0) configs
# 3. Leaves “editor.formatOnSave” DISABLED – user must enable it
# 4. Opens VS Code ready for the refactor task
###############################################################################

echo "🚀  Initialising React refactor task workspace …"

# --------------------------------------------------------------------------- #
# 1. Workspace skeleton
# --------------------------------------------------------------------------- #
WORKSPACE="$HOME/react_refactor_task"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src/utils"  # utils folder exists but api.js missing

# Basic React entry so import will fail / lint
cat > "$WORKSPACE/src/App.jsx" << 'EOF'
/* eslint-disable no-console */
import React from 'react';
import { fetchWithRetry } from './utils/api'; // <-- MISSING FILE ON PURPOSE

export default function App() {
  React.useEffect(() => {
    fetchWithRetry('/ping')
      .then((res) => console.log(res))
      .catch((err) => console.error(err));
  }, []);

  return <h1>Hello React Refactor Task</h1>;
}
EOF

# Minimal index file
cat > "$WORKSPACE/src/index.jsx" << 'EOF'
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

createRoot(document.getElementById('root')).render(<App />);
EOF

# README that explains the task
cat > "$WORKSPACE/README.md" << 'EOF'
# React Refactor Task
Create `src/utils/api.js` that wraps *window.fetch* with retries, timeouts,
and detailed error handling. The new file must pass ESLint **v2.4.0**
and Prettier **v10.0.0** and the workspace should auto-format on save.
EOF

# --------------------------------------------------------------------------- #
# 2. Tooling configuration
# --------------------------------------------------------------------------- #

# package.json – only declares deps (no install / network done here)
cat > "$WORKSPACE/package.json" << 'EOF'
{
  "name": "react-refactor-task",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "lint": "eslint .",
    "format": "prettier --check ."
  },
  "devDependencies": {
    "eslint": "2.4.0",
    "prettier": "10.0.0",
    "eslint-plugin-react": "3.16.1"
  }
}
EOF

# ESLint config that should accept modern ES6/React code
cat > "$WORKSPACE/.eslintrc.json" << 'EOF'
{
  "parserOptions": {
    "ecmaVersion": 2020,
    "sourceType": "module",
    "ecmaFeatures": { "jsx": true }
  },
  "plugins": ["react"],
  "extends": ["eslint:recommended", "plugin:react/recommended"],
  "rules": {
    "react/react-in-jsx-scope": "off"
  }
}
EOF

# Prettier config
cat > "$WORKSPACE/.prettierrc" << 'EOF'
{
  "singleQuote": true,
  "semi": true,
  "trailingComma": "es5",
  "printWidth": 80
}
EOF

# --------------------------------------------------------------------------- #
# 3. VS Code workspace settings (NO auto-format on save yet)
# --------------------------------------------------------------------------- #
mkdir -p "$WORKSPACE/.vscode"

cat > "$WORKSPACE/.vscode/settings.json" << 'EOF'
{
  "editor.tabSize": 2,
  "editor.formatOnSave": false,
  "files.eol": "\n",
  "javascript.validate.enable": false
}
EOF

# Task marker
echo "TODO: 1) Create src/utils/api.js with fetch wrapper  2) Enable Format on Save" \
  > "$WORKSPACE/.task_info.txt"

# --------------------------------------------------------------------------- #
# 4. Verification
# --------------------------------------------------------------------------- #
if [ -f "$WORKSPACE/src/utils/api.js" ]; then
  echo "❌  api.js unexpectedly exists – aborting."
  exit 1
fi
echo "✅  Workspace prepared – api.js is intentionally missing."

# --------------------------------------------------------------------------- #
# 5. Launch VS Code
# --------------------------------------------------------------------------- #
echo "🖥️  Opening VS Code …"
code "$WORKSPACE" &> /dev/null &

echo "🏁  Initial setup complete.  Follow the instructions inside VS Code."
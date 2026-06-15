#!/usr/bin/env bash
# 01-initial-setup.sh
# -----------------------------------------------
# Prepares a React workspace that is missing
# src/utils/formUtils.js so the user can create it.
# -----------------------------------------------
set -euo pipefail

echo "🔧  Creating initial VS Code task workspace …"

# ---------- CONFIG ----------
WORKSPACE="$HOME/react_form_task"
VSCODE_DIR="$WORKSPACE/.vscode"
UTILS_DIR="$WORKSPACE/src/utils"
# ----------------------------

# Fresh workspace
rm -rf "$WORKSPACE"
mkdir -p "$UTILS_DIR"

# ---- Basic React-ish scaffold (no CRA to keep it light) ----
cat > "$WORKSPACE/package.json" << 'EOF'
{
  "name": "react-form-task",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "prettier": "^3.0.0"
  },
  "scripts": {
    "start": "echo 'Dev server stub'"
  }
}
EOF

mkdir -p "$WORKSPACE/src"
cat > "$WORKSPACE/src/App.js" << 'EOF'
import React, { useState } from "react";

export default function App() {
  const [data, setData] = useState({});

  // TODO: import { serializeForm, getFormData } from "./utils/formUtils";
  // Then call setData(getFormData(event));

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        // setData(getFormData(e));
      }}
    >
      <input name="firstName" placeholder="First name" />
      <input name="lastName" placeholder="Last name" />
      <button type="submit">Submit</button>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </form>
  );
}
EOF

# --------- VS Code configuration ---------
mkdir -p "$VSCODE_DIR"
cat > "$VSCODE_DIR/settings.json" << 'EOF'
{
  // Ensure Prettier auto-formatting is active
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "prettier.singleQuote": true,
  "prettier.trailingComma": "all"
}
EOF

cat > "$VSCODE_DIR/extensions.json" << 'EOF'
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint"
  ]
}
EOF

# ---------- Task Marker ----------
cat > "$WORKSPACE/.task_info.txt" << 'EOF'
TASK: Create src/utils/formUtils.js that exports:
  • serializeForm(formElement)
  • getFormData(event)
Both should return a plain object representing the form input values.
EOF

# ---------- Verification ----------
if [[ ! -e "$UTILS_DIR/formUtils.js" ]]; then
  echo "✅ Verified: src/utils/formUtils.js does NOT exist yet (expected)."
else
  echo "⚠️  Unexpected: src/utils/formUtils.js already exists." >&2
  exit 1
fi

# ---------- Open VS Code ----------
echo "🚀 Opening VS Code.  Follow .task_info.txt instructions."
code "$WORKSPACE" &>/dev/null &

echo "🏁 Initial setup complete."
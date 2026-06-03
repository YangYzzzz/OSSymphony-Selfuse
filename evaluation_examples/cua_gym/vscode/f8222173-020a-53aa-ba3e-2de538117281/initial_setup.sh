#!/usr/bin/env bash
#-----------------------------------------------
# initial_setup.sh
#
# Creates a React/TypeScript workspace **without**
# a proper .editorconfig so the user must add it.
#-----------------------------------------------
set -euo pipefail

echo "🔧  Preparing initial React/TypeScript workspace …"

# ---------- VARIABLES ----------
WORKSPACE="$HOME/react_ts_editorconfig_task"
VSCODE_DIR="$WORKSPACE/.vscode"
PROJECT_NAME="react-ts-sample"
EXT_RECOMMENDATION="EditorConfig.EditorConfig"      # publisher.extensionId

# ---------- CLEAN START ----------
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE" "$VSCODE_DIR"

# ---------- SAMPLE PROJECT CONTENT ----------
npx --yes create-react-app "$WORKSPACE/$PROJECT_NAME" --template typescript >/dev/null 2>&1 || {
  echo "⚠️  create-react-app not available (offline?). Creating minimal placeholder project."
  mkdir -p "$WORKSPACE/$PROJECT_NAME/src"
  cat > "$WORKSPACE/$PROJECT_NAME/src/index.tsx" <<'EOF'
import React from "react";
import ReactDOM from "react-dom/client";
const root = ReactDOM.createRoot(document.getElementById("root")!);
root.render(<h1>Hello World!</h1>);
EOF
  cat > "$WORKSPACE/$PROJECT_NAME/tsconfig.json" <<'EOF'
{
  "compilerOptions": { "strict": true, "jsx": "react" }
}
EOF
  echo '{ "name": "placeholder" }' > "$WORKSPACE/$PROJECT_NAME/package.json"
}

# ---------- VSCODE CONFIG ----------
# Extension recommendation so the user sees the correct extension.
cat > "$VSCODE_DIR/extensions.json" <<EOF
{
  "recommendations": [
    "$EXT_RECOMMENDATION"
  ]
}
EOF

# Workspace settings purposely set different indentation to show the problem
cat > "$VSCODE_DIR/settings.json" <<'EOF'
{
  "editor.insertSpaces": false,
  "editor.tabSize": 4
}
EOF

# ---------- TASK MARKER ----------
cat > "$WORKSPACE/README_TASK.md" <<'EOF'
# VS Code Task – Add .editorconfig

Create a `.editorconfig` at the **repository root** with:
- space indents (size = 2)
- UTF-8 charset
- automatic trimming of trailing whitespace

Use the “EditorConfig for VS Code” extension (v0.16.4).  
EOF

# ---------- VERIFICATION ----------
echo "✅  Workspace created at: $WORKSPACE"
echo "   - .editorconfig DOES NOT exist (expected for task)"
echo "   - Open VS Code now …"

# ---------- OPEN VSCODE ----------
code "$WORKSPACE" & disown
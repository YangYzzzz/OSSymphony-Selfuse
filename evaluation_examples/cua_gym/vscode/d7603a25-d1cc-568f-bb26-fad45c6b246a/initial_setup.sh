#!/usr/bin/env bash
# File: initial_setup.sh
# Purpose: Prepare a JS/TS repo that still needs correct extension recommendations
set -euo pipefail

echo "=== VS Code Extension-Recommendation Task – Initial Setup ==="

# -------------------------------------------------------------
# 1. Create workspace skeleton
# -------------------------------------------------------------
WORKSPACE="$HOME/js_ts_repo"
echo "Creating workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/.vscode"

# Example project files so VS Code recognizes a JS/TS project
cat > "$WORKSPACE/package.json" <<'EOF'
{
  "name": "js-ts-repo",
  "version": "1.0.0",
  "scripts": {
    "lint": "eslint .",
    "format": "prettier --write ."
  },
  "devDependencies": {
    "eslint": "^8.0.0",
    "prettier": "^2.0.0",
    "typescript": "^5.0.0"
  }
}
EOF

cat > "$WORKSPACE/tsconfig.json" <<'EOF'
{
  "compilerOptions": {
    "target": "es2020",
    "module": "commonjs",
    "strict": true
  }
}
EOF

mkdir -p "$WORKSPACE/src"
echo "export const hello = () => console.log('Hello');" > "$WORKSPACE/src/index.ts"

# -------------------------------------------------------------
# 2. Incomplete extensions.json (needs fixing by user)
# -------------------------------------------------------------
cat > "$WORKSPACE/.vscode/extensions.json" <<'EOF'
{
  // TODO: Add missing recommendations with exact versions
  "recommendations": [
    "dbaeumer.vscode-eslint"
  ]
}
EOF
echo "Created placeholder .vscode/extensions.json (not correct yet)."

# -------------------------------------------------------------
# 3. Task hint for the user
# -------------------------------------------------------------
cat > "$WORKSPACE/.task_info.txt" <<'EOF'
👉 Task: Open .vscode/extensions.json and replace it with the exact JSON:
{
  "recommendations": [
    "dbaeumer.vscode-eslint@2.4.0",
    "esbenp.prettier-vscode@9.12.0",
    "eamodio.gitlens@14.4.1"
  ]
}
EOF
echo "Task instructions placed in $WORKSPACE/.task_info.txt"

# -------------------------------------------------------------
# 4. Launch VS Code
# -------------------------------------------------------------
code "$WORKSPACE" &
echo "VS Code opened with initial workspace. Ready for user action."
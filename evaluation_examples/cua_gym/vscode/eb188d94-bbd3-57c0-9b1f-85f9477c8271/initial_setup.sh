#!/usr/bin/env bash
# -------------------------------
#  VS Code Task – Initial Setup
# -------------------------------
# Goal: Provide a Node workspace that is missing
#       1) src/utils/validation.js
#       2) ESLint auto-fix-on-save setting
# Learner will add those manually inside VS Code.
# -------------------------------

set -euo pipefail

echo "🔧  Preparing initial VS Code workspace…"

# ------------------------------------------------
# 1. Build a fresh workspace skeleton
# ------------------------------------------------
WORKSPACE="$HOME/node_validator_task"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"

# sample application file (references validators that don’t yet exist)
cat > "$WORKSPACE/src/index.js" << 'EOF'
/* TODO: implement validators in src/utils/validation.js */

const { email, phoneNumber, requiredField } = require('./utils/validation');

console.log(
  email('user@example.com'),
  phoneNumber('+15551234567'),
  requiredField('some value')
);
EOF

# basic Node package & ESLint configuration
cat > "$WORKSPACE/package.json" << 'EOF'
{
  "name": "validator-demo",
  "version": "1.0.0",
  "type": "commonjs",
  "scripts": {
    "lint": "eslint ."
  },
  "devDependencies": {
    "eslint": "^8.56.0"
  }
}
EOF

cat > "$WORKSPACE/.eslintrc.json" << 'EOF'
{
  "env": { "node": true, "es2021": true },
  "extends": "eslint:recommended",
  "rules": {
    "semi": ["error", "always"],
    "quotes": ["error", "single"]
  }
}
EOF

# ------------------------------------------------
# 2. VS Code configuration (missing auto-fix!)
# ------------------------------------------------
mkdir -p "$WORKSPACE/.vscode"
cat > "$WORKSPACE/.vscode/settings.json" << 'EOF'
{
  // ESLint extension present (dbaeumer.vscode-eslint)
  "eslint.validate": ["javascript"],
  "editor.codeActionsOnSave": {
    // learner must add: "source.fixAll.eslint": true
  }
}
EOF

# ------------------------------------------------
# 3. Task instructions for the learner
# ------------------------------------------------
cat > "$WORKSPACE/README_TASK.md" << 'EOF'
### Your Task in VS Code

1. Inside **src/utils/** create **validation.js** that exports:
   • email  
   • phoneNumber  
   • requiredField  

2. In **.vscode/settings.json** enable ESLint auto-fix on save:
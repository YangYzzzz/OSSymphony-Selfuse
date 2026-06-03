#!/usr/bin/env bash
###############################################################################
# initial_setup.sh
#
# 1. Creates a small React-style workspace
# 2. Installs the “ESLint” VS Code extension
# 3. DISABLES that extension (simulating the user’s mistake)
# 4. Opens VS Code so the learner can re-enable ESLint
###############################################################################
set -euo pipefail

echo "=== VS Code ESLint re-enable task – Initial Setup ==="

# ----------------------------------------------------------------------
# 0. Variables
# ----------------------------------------------------------------------
WORKSPACE="$HOME/react_eslint_task"
VSC_USER_SETTINGS="$HOME/.config/Code/User/settings.json"
EXT_ID="dbaeumer.vscode-eslint"

# ----------------------------------------------------------------------
# 1. Prepare clean workspace
# ----------------------------------------------------------------------
echo "Creating React-style workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"

cat > "$WORKSPACE/src/App.js" <<'EOF'
import React from 'react';

export default function App() {
  const unused = 42          // <-- ESLint should normally complain
  return <h1>Hello, ESLint!</h1>;
}
EOF

cat > "$WORKSPACE/.eslintrc.js" <<'EOF'
module.exports = {
  env: { browser: true, es2021: true },
  extends: ['eslint:recommended', 'react-app'],
  rules: { 'no-unused-vars': 'warn' }
};
EOF

echo "{}" > "$WORKSPACE/package.json"

# ----------------------------------------------------------------------
# 2. Ensure ESLint extension is INSTALLED
# ----------------------------------------------------------------------
echo "Installing ESLint extension (if not already present)…"
code --install-extension "$EXT_ID" --force

# ----------------------------------------------------------------------
# 3. Disable ESLint extension
# ----------------------------------------------------------------------
echo "Disabling ESLint extension to reproduce the problem…"
code --disable-extension "$EXT_ID"

# ----------------------------------------------------------------------
# 4. Explicitly turn ESLint OFF in user settings as an extra safeguard
# ----------------------------------------------------------------------
echo "Writing temporary user setting \"eslint.enable\": false"
mkdir -p "$(dirname "$VSC_USER_SETTINGS")"
if command -v jq >/dev/null 2>&1; then
  # merge or create setting
  if [[ -f "$VSC_USER_SETTINGS" ]]; then
    jq '. + {"eslint.enable": false}' "$VSC_USER_SETTINGS" > "${VSC_USER_SETTINGS}.tmp"
    mv "${VSC_USER_SETTINGS}.tmp" "$VSC_USER_SETTINGS"
  else
    echo '{ "eslint.enable": false }' > "$VSC_USER_SETTINGS"
  fi
else
  # fall-back (overwrites file)
  cat > "$VSC_USER_SETTINGS" <<'JSON'
{
  "eslint.enable": false
}
JSON
fi

# ----------------------------------------------------------------------
# 5. Verification
# ----------------------------------------------------------------------
echo "Verifying ESLint extension is disabled…"
if code --list-extensions | grep -q "^${EXT_ID}$"; then
  echo "   ✓ ESLint extension is installed (good)"
else
  echo "   ✗ ESLint extension failed to install"; exit 1
fi

if code --status | grep -q "$EXT_ID.*disabled" || grep -q '"eslint.enable": false' "$VSC_USER_SETTINGS"; then
  echo "   ✓ ESLint appears disabled – task scenario ready"
else
  echo "   ✗ ESLint was not disabled correctly"; exit 1
fi

# ----------------------------------------------------------------------
# 6. Open VS Code
# ----------------------------------------------------------------------
echo "Opening VS Code – your job: RE-ENABLE the ESLint extension!"
code "$WORKSPACE" &

echo "=== Setup complete – happy debugging! ==="